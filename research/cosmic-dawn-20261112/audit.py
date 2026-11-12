"""Reproduce a bounded Wave 10 numerical audit, without running its catalogue code."""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'wave10_covariant_jeans_unification.py'
PIN = '8f904ba3aad22ce727e92b96bf0c12e229173f8f'
SHA256 = 'af8a2459aa8f5885250ab6b5914c50cc852bcc691982c8ef5cf692603bece927'


def factory(kmax, nk):
    """Extract only constants and the spectrum factory; adjust two AST literals in memory."""
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA256:
        raise ValueError('Wave 10 source hash differs from the audited source')
    tree = ast.parse(raw)
    constants = [n for n in tree.body if isinstance(n, ast.Assign)]
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == 'build_eh98_power_spectrum']
    if len(funcs) != 1:
        raise ValueError('Expected one spectrum factory')
    fn = funcs[0]
    replacements = [0, 0]
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'nk' for t in node.targets):
            if not isinstance(node.value, ast.Constant) or node.value.value != 1600:
                raise ValueError('Unexpected native nk')
            node.value = ast.Constant(nk)
            replacements[0] += 1
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'log' and len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == 300.0:
            node.args[0] = ast.Constant(kmax)
            replacements[1] += 1
    if replacements != [1, 1]:
        raise ValueError('Spectrum replacement count differs')
    module = ast.fix_missing_locations(ast.Module(body=constants + [fn], type_ignores=[]))
    ns = {'math': math}
    exec(compile(module, '<pinned-wave10-spectrum>', 'exec'), ns)
    return ns, ns['build_eh98_power_spectrum']()


def point(ns, spectrum, z):
    sigma, growth = spectrum
    target = ns['DELTA_C_SPH'] / growth(z)
    lo, hi = 1e-4, 25.0
    residuals = [sigma(lo) - target, sigma(hi) - target]
    result = {'z': z, 'growth': growth(z), 'bracket_Mpc': [lo, hi],
              'endpoint_residuals': residuals}
    if not residuals[0] >= 0 >= residuals[1]:
        return dict(result, status='no_root_in_bracket')
    for _ in range(55):
        mid = math.sqrt(lo * hi)
        if sigma(mid) > target:
            lo = mid
        else:
            hi = mid
    r = (lo + hi) / 2
    mass = 4 * math.pi / 3 * (r * ns['MPC']) ** 3 * ns['OMEGA_M'] * ns['RHO_CRIT0']
    ez2 = ns['OMEGA_M'] * (1 + z) ** 3 + ns['OMEGA_L']
    r200 = (3 * mass / (4 * math.pi * 200 * ns['RHO_CRIT0'] * ez2)) ** (1 / 3)
    dispersion = math.sqrt(ns['G'] * mass / (2 * r200)) / 1000
    return dict(result, status='root', R_star_Mpc=r, M_star_Msun=mass / ns['M_SUN'],
                sigma_star_kms=dispersion, compactness_2GM_Rc2=2 * ns['G'] * mass / (r200 * ns['C_SI'] ** 2),
                f_trap={str(h): max(0, 1 - (dispersion / h) ** 2) for h in [150, 176, 200]})


def generate():
    runs = []
    for kmax, nk in [(300.0, 1600), (300.0, 12800), (1e4, 12800), (1e5, 12800)]:
        ns, spectrum = factory(kmax, nk)
        runs.append({'kmax_Mpc_inverse': kmax, 'nk': nk,
                     'points': [point(ns, spectrum, z) for z in [0.0, 6.08, 7.0]]})
    return {'source_commit': PIN, 'source_sha256': SHA256,
            'inputs': {'kmin_Mpc_inverse': 1e-5, 'radius_bracket_Mpc': [1e-4, 25],
                       'root_iterations': 55, 'growth_steps': 1600,
                       'halo_sigma_kms_illustrative': [150, 176, 200]},
            'assumptions': ['Wave 10 Planck 2018 constants and EH98 cold dark matter approximation',
                            'sigma(R,0) D(z) = 1.686; total halo mass at mean matter density',
                            'R200 uses 200 times critical density; sigma_star squared = GM/(2 R200)',
                            'f_trap is an assumed law, not a horizon criterion'],
            'runs': runs}


def compare(actual, saved, path='results'):
    if type(actual) is not type(saved):
        raise ValueError(path + ': type changed')
    if isinstance(actual, dict):
        if actual.keys() != saved.keys():
            raise ValueError(path + ': keys changed')
        for key in actual:
            compare(actual[key], saved[key], path + '.' + key)
    elif isinstance(actual, list):
        if len(actual) != len(saved):
            raise ValueError(path + ': length changed')
        for i, (a, b) in enumerate(zip(actual, saved)):
            compare(a, b, path + '[' + str(i) + ']')
    elif isinstance(actual, float):
        if not (math.isfinite(actual) and math.isfinite(saved)
                and math.isclose(actual, saved, rel_tol=1e-9, abs_tol=1e-14)):
            raise ValueError(path + ': numerical value changed')
    elif actual != saved:
        raise ValueError(path + ': value changed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = generate()
    output = Path(__file__).with_name('results.json')
    if args.check:
        compare(result, json.loads(output.read_text()))
        print('Saved numerical values and statuses match regeneration.')
    else:
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
