"""Independent, read-only Wave 11/12 probes. Requires numpy and scipy.

Run: python3 -B probe.py --repo PATH --output evidence.json
The repository is read-only. Output records relative names and source hashes.
"""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


def load_module(path):
    manifest = json.loads((path.parent / 'manifest.json').read_text())
    expected = next(item['sha256'] for item in manifest['files'] if item['path'] == path.name)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Pinned source hash mismatch: ' + path.name)
    ns = {'__name__': 'read_only_probe', '__file__': str(path)}
    exec(compile(path.read_text(), str(path.name), 'exec'), ns)
    return ns


def spectrum(ns, nk, kmax):
    tree = ast.parse(Path(ns['__file__']).read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
              and n.name == 'build_sigma_r_evaluator')
    found = [0, 0]
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'n_k' for t in node.targets):
            assert node.value.value == 1200
            node.value = ast.Constant(nk)
            found[0] += 1
        if isinstance(node, ast.Constant) and node.value == 5.0e4:
            node.value = kmax
            found[1] += 1
    assert found == [1, 1]
    copy = ns.copy()
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), '<grid-variant>', 'exec'), copy)
    return copy['build_sigma_r_evaluator']()


def collapse(ns, sigma, z, growth_override=None):
    growth = ns['growth_factor_norm'](z)
    factor = growth_override / growth if growth_override else 1.0
    residual = lambda r: sigma(r, z) * factor - 1.686
    lo, hi = 1e-4, 1.0
    if residual(lo) * residual(hi) >= 0:
        return {'z': z, 'status': 'no_root_in_native_bracket',
                'endpoint_residuals': [residual(lo), residual(hi)]}
    r = brentq(residual, lo, hi, xtol=1e-15)
    mass = 4 * math.pi / 3 * (r * ns['MPC'])**3 * ns['OMEGA_M'] * ns['RHO_CRIT0']
    hz = ns['H0_SI'] * ns['e_hubble'](z)
    v200 = (10 * ns['G'] * mass * hz)**(1/3)
    r200 = ns['G'] * mass / v200**2
    sig = v200 / math.sqrt(2) / 1000
    return {'z': z, 'status': 'root', 'R_Mpc': r, 'Mstar_Msun': mass / ns['M_SUN'],
            'sigma_kms': sig, 'R200_pc': r200 / ns['PC'],
            'compactness': 2 * ns['G'] * mass / (r200 * ns['C_SI']**2),
            'baryon_budget_Msun': mass / ns['M_SUN'] * ns['OMEGA_B'] / ns['OMEGA_M'],
            'Tvir_neutral_K': 1.22 * ns['M_P'] * v200**2 / (2 * 1.380649e-23),
            'ftrap_host250_over_sqrt2': max(0, 1 - (sig / (250 / math.sqrt(2)))**2),
            'growth_factor_used': growth * factor}


def integrated_growth(ns, z):
    om, ol = ns['OMEGA_M'], ns['OMEGA_L']
    E = lambda a: math.sqrt(om / a**3 + ol)
    raw = lambda a: E(a) * quad(lambda x: 1 / (x * E(x))**3, 0, a, epsabs=1e-13, epsrel=1e-11)[0]
    return raw(1 / (1 + z)) / raw(1)


def growth_probe(ns):
    edd = ns['SIGMA_T'] * ns['C_SI'] / (4 * math.pi * ns['G'] * ns['M_P']) / ns['MYR']
    dt = ns['cosmic_age_myr'](ns['Z_PAIR']) - ns['cosmic_age_myr'](20)
    eps_schwarzschild = 1 - math.sqrt(8 / 9)
    rows = []
    for eps in [eps_schwarzschild, 0.10, 0.20]:
        for composition, opacity_factor in [('pure_H', 1.0), ('primordial_fully_ionized', 1 - 0.245/2)]:
            t = math.log(1.5e9 / 100) * edd * opacity_factor * eps / (1 - eps)
            rows.append({'epsilon': eps, 'composition': composition,
                         'time_Myr_at_lambda1': t, 'required_duty_z20_lambda1': t/dt,
                         'required_duty_z20_lambda1p23': t/dt/1.23})
    return {'window_z20_Myr': dt, 'rows': rows,
            'critical_epsilon_for_duty1_pureH_lambda1': dt/(dt + edd*math.log(1.5e9/100)),
            'note': 'Constant efficiency, no delay or mergers, retained fuel, and time-averaged lambda*duty are assumed. Current lambda is not a history.'}


def infall_probe(ns, ftrap):
    # Solve radial free fall from rest in a fixed point-mass field using
    # y=r/r0 and dimensionless t=sqrt(r0/gb0) tau. This directly integrates
    # r''=-g(r); no Newtonian prefactor is imposed on MOND.
    r0, mb = 30*ns['KPC'], 5e10*ns['M_SUN']
    gb = ns['G']*mb/r0**2
    tunit = math.sqrt(r0/gb)/ns['MYR']
    hz = ns['H0_SI']*ns['e_hubble'](ns['Z_PAIR'])
    cases = [('Newton_baryon', None, 0), ('MOND_const_a0', ns['A0_EMP'], 0),
             ('MOND_Hubble_a0', ns['C_SI']*hz/(2*math.pi), 0),
             ('two_branch_const_a0', ns['A0_EMP'], ns['OMEGA_C']/ns['OMEGA_B']*ftrap)]
    rows = []
    for name, a0, extra in cases:
        def force(y):
            gnewt = 1/y**2
            return (gnewt if a0 is None else gnewt/(-math.expm1(-math.sqrt(gb/a0)/y))) + extra*gnewt
        def stop(t, v): return v[0]-1e-7
        stop.terminal = True
        stop.direction = -1
        def rhs(t, v): return [v[1], -force(max(v[0], 1e-9))]
        sol = solve_ivp(rhs, [0, 2], [1, 0], rtol=2e-11, atol=1e-13, events=stop, max_step=0.002)
        assert len(sol.t_events[0]) == 1
        exact = sol.t_events[0][0]*tunit
        shortcut = math.pi/(2*math.sqrt(2*force(1)))*tunit
        rows.append({'model': name, 'direct_radial_time_Myr': exact,
                     'Wave12_outer_acceleration_shortcut_Myr': shortcut,
                     'shortcut_fractional_error': shortcut/exact-1})
    return {'assumptions': 'Static point baryon mass, initially resting radial test particle, fixed a0, no angular momentum, pressure, expansion, feedback, or external field. Counterexample to exactness, not a realistic gas solution.',
            'rows': rows, 'deep_MOND_exact_over_shortcut': 2/math.sqrt(math.pi)}


def future_probe(ns11):
    # Alternative matches CPL on every observed past scale factor a<=1,
    # matches w and dw/da at a=1, then turns toward -1.
    w0, wa = -0.75, -0.85
    w_alt = lambda a: -1 + (0.25 + 1.10*(a-1))*math.exp(-(a-1))
    # The integrand is negligible beyond 100. Capping avoids a large-domain
    # quadrature missing the contribution close to a=1.
    rho = lambda a: math.exp(-3*quad(lambda x: (1+w_alt(x))/x, 1, min(a,100), epsabs=1e-11)[0])
    rows = []
    for a in [1, 1.3897, 2, 31.52, 78.8, 315.18, 1000]:
        h2 = ns11['OMEGA_M']/a**3 + ns11['OMEGA_L']*rho(a) - .004/a**2
        acceleration = ns11['OMEGA_M']/a**3 + ns11['OMEGA_L']*rho(a)*(1+3*w_alt(a))
        rows.append({'a': a, 'w_alt': w_alt(a), 'rho_DE_over_rho0': rho(a),
                     'H2_over_H02_Omega_k_minus0p004': h2,
                     'deceleration_sign_term': acceleration})
    grid = np.geomspace(1, 1e5, 3000)
    h2s = [ns11['OMEGA_M']/a**3 + ns11['OMEGA_L']*rho(a) - .004/a**2 for a in grid]
    return {'formula_for_a_greater_than_1': 'w=-1+[0.25+1.10(a-1)] exp[-(a-1)]',
            'for_a_at_most_1': 'identical to original CPL, hence identical past distances and expansion',
            'w_at_1': -.75, 'dw_da_at_1': .85, 'min_H2_on_1_to_1e5': min(h2s),
            'rows': rows, 'note': 'This deliberately mirrors the source Omega_L normalization; re-normalizing for curvature does not restore a turnaround.'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    ns=load_module(args.repo/'wave12_cosmic_dawn_quasar_collapse.py')
    ns11=load_module(args.repo/'wave11_machian_pairing_unification.py')
    grid=[]
    for nk,kmax in [(1200,5e4),(12800,5e4),(12800,1e5),(12800,300)]:
        sig=spectrum(ns,nk,kmax)
        entry={'nk':nk,'kmax_Mpc_inverse':kmax,'point':collapse(ns,sig,ns['Z_PAIR'])}
        if nk==12800 and kmax==1e5:
            entry['using_integrated_LCDM_growth']=collapse(ns,sig,ns['Z_PAIR'],integrated_growth(ns,ns['Z_PAIR']))
            entry['early_seed_epoch']=collapse(ns,sig,20)
        grid.append(entry)
    native=grid[0]['point']
    m1,m2=1.5e9,4e8
    chirp=(m1*m2)**.6/(m1+m2)**.2
    files=['wave12_cosmic_dawn_quasar_collapse.py','wave11_machian_pairing_unification.py',
           'formal/Wave12QuasarCollapse.lean','formal/Wave11MachianZeroEnergy.lean',
           'results/wave12_cosmic_dawn_quasar_certificates.json','results/wave11_machian_pairing_certificates.json']
    result={'source_commit':'70a1204a536b3dca0b3053d1a056daf22601ac00',
            'source_sha256':{f:hashlib.sha256((args.repo/f).read_bytes()).hexdigest() for f in files},
            'spectrum_grid':grid,'growth':growth_probe(ns),
            'infall':infall_probe(ns,native['ftrap_host250_over_sqrt2']),
            'chirp':{'Python_Msun':chirp,'left':19*647**5,'source_middle':15**3*4**2*10**10,
                     'right':19*648**5,'correct_middle':15**3*4**3*10**10,
                     'source_lower_bound_true':19*647**5<15**3*4**2*10**10,
                     'correct_bounds_true':19*647**5<15**3*4**3*10**10<19*648**5},
            'CPT':{'P_double_prime_at_u0_in_K2_over_Q02':-4,
                   'J_at_u0':0,'J_at_u1p000001':4*1.000001*(1.000001**2-1),
                   'kinetic_degeneracy_abs_u':1/math.sqrt(3),
                   'homogeneous_current_conservation':'a^3 P_Q=constant on each smooth source-free sheet'},
            'future_counterexample':future_probe(ns11)}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__': main()
