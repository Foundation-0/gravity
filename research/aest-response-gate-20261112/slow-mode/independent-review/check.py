#!/usr/bin/env python3
"""Independent review of the frozen slow-subspace preparation calculation.

The comparator uses the separately ADM-reviewed five-field evolution, not the
new four-state right-hand side. Author modules are imported without their mains.
Only this review directory receives output.
"""
from pathlib import Path
import hashlib, importlib.util, json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
BASE = SOURCE.parent / 'public-checkpoint'
if not BASE.is_dir():
    BASE = SOURCE.parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((SOURCE / 'checkpoint.json').read_text())
for item in manifest['files']:
    assert digest(SOURCE / item['path']) == item['sha256'], item['path']
assert digest(BASE / 'response.py') == 'e28c8f4ada1e41924e6317f8932de4d065307516cd57c5ff83a0cf23b72397ef'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

author = module('slow_author', SOURCE / 'probe.py')
original = module('original_fields', BASE / 'response.py')
record = json.loads((SOURCE / 'evidence.json').read_text())

# Transform the audited unnormalized conservation equations analytically.
# Rdot=-3HW; Wdot=-3HW(1+c_a^2). These background terms cannot be omitted.
a, k = sp.symbols('a k', positive=True)
d, th, ch, z = sp.symbols('delta theta chi Z', real=True)
q = sp.Rational(1, 100) / a**3
Q, Kp, R, W = 1+q, 4*q, 4*q+2*q*q, (1+q)*4*q
H = sp.sqrt(R/3)
r, ca = k*k/a**2, Kp/(4*Q)
D, m = R*d, W*th
Phi = -(D+3*H*m)/(2*r)
gamma = (D+r*z)/(4*Q)
p = Kp*gamma
Pd = -H*Phi+m/2
Dd = -3*H*(D+p)+3*W*Pd-r*m
md = -3*H*m+p+W*Phi
Qd = sp.diff(Q, a)*a*H
transformed = sp.Matrix([
    (Dd-sp.diff(R, a)*a*H*d)/R,
    (md-sp.diff(W, a)*a*H*th)/W,
    gamma+Q*z+(Qd/Q-Q)*ch-Qd*th,
    (-H+Q)*z+(Kp-3*Q)*ch,
])
M = transformed.jacobian([d, th, ch, z])
Mfun = sp.lambdify((a, k), M, 'numpy')
Mdafun = sp.lambdify((a, k), M.diff(a), 'numpy')
assert sp.simplify(sp.diff(R, a)*a*H+3*H*W) == 0
assert sp.simplify(sp.diff(W, a)*a*H+3*H*W*(1+ca)) == 0

def to_fields(scale, state, kval):
    qq, kp, _, rr, ww, hh = original.bg(scale, .01)
    radial = (kval/scale)**2
    delta, theta, chi, Z = state
    density, momentum = rr*delta, ww*theta
    phi = -(density+3*hh*momentum)/(2*radial)
    v = momentum/kp
    return np.array([v, (chi-v)/qq, Z-chi, phi,
                     (density+radial*Z)/(4*qq)])

def from_fields(grid, fields, kval):
    qq, kp, _, rr, ww, hh = original.bg(grid, .01)
    v, al, E, phi, gamma = fields.T
    chi = v+qq*al
    Z = E+chi
    density = 4*qq*gamma-(kval/grid)**2*Z
    return np.column_stack([density/rr, kp*v/ww, chi, Z])

def independent_field_fundamental(grid, kval):
    initial = np.column_stack([to_fields(1., np.eye(4)[:,i], kval) for i in range(4)])
    def derivative(scale, flat):
        field_matrix = flat.reshape(5, 4)
        columns = [original.rhs_fields(0., np.r_[scale, field_matrix[:,j]], kval, .01)[1:]
                   for j in range(4)]
        return (np.column_stack(columns)/(scale*original.bg(scale, .01)[-1])).ravel()
    solution = solve_ivp(derivative, (1., 2.), initial.ravel(), t_eval=grid,
                         method='DOP853', rtol=2e-12, atol=1e-17)
    assert solution.success
    return solution.y.T.reshape(len(grid), 5, 4)

def independent_closure(grid, kval, initial_retained, closure):
    _, _, _, rr, ww, _ = original.bg(1., .01)
    def derivative(scale, retained):
        qq, kp, _, rr, ww, hh = original.bg(scale, .01)
        D, m = retained
        radial = (kval/scale)**2
        phi = -(D+3*hh*m)/(2*radial)
        pressure = 0. if closure == 'zero' else kp/(4*qq)*D
        return np.array([-3*hh*(D+pressure)+3*ww*(-hh*phi+m/2)-radial*m,
                         -3*hh*m+pressure+ww*phi])/(scale*hh)
    solution = solve_ivp(derivative, (1., 2.), initial_retained*np.array([rr, ww]),
                         t_eval=grid, method='DOP853', rtol=2e-12, atol=1e-22)
    assert solution.success
    _, _, _, rr, ww, hh = original.bg(grid, .01)
    D, m = solution.y
    return np.array([D/rr, -(D+3*hh*m)/(kval/grid)**2])

output = {'reviewed_files': manifest['files'], 'base_response_sha256': digest(BASE/'response.py'),
          'method': 'Exact background-normalization transform; independently differentiate the generator; integrate the prior ADM-reviewed five-field equations and unnormalized conservation closures.',
          'points': []}
grid = np.linspace(1., 2., 2001)
for point in record['points']:
    kval = point['k']
    author.KVAL = kval
    matrix_error = max(np.max(abs(author.matrix(scale)-Mfun(scale, kval)))
                       for scale in np.linspace(1., 2., 31))
    assert matrix_error < 1e-9
    S0, contamination, diagnostics = author.modes()
    eig, V = np.linalg.eig(Mfun(1., kval))
    slow_indices = np.argsort(abs(eig.imag))[:2]
    fast_indices = np.argsort(abs(eig.imag))[2:]
    coordinates = np.linalg.solve(V, S0)
    initial_fast_norm = float(np.linalg.norm(coordinates[fast_indices]))
    assert initial_fast_norm < 1e-10
    assert np.allclose(S0[:2], [1., -original.bg(1., .01)[-1]/kval**2], rtol=1e-12)
    assert sum(eig.imag > 1e-8) == 2

    # Off-diagonal eigenvector motion follows by differentiating M v_j=lambda_j v_j.
    # No finite difference of eigenvectors or phase tracking is needed here.
    mix_to_fast, mix_to_slow = [], []
    for scale in np.linspace(1., 2., 201):
        ee, VV = np.linalg.eig(Mfun(scale, kval))
        ss = np.argsort(abs(ee.imag))[:2]
        ff = np.argsort(abs(ee.imag))[2:]
        Mdot = Mdafun(scale, kval)*scale*original.bg(scale, .01)[-1]
        transformed_Mdot = np.linalg.solve(VV, Mdot@VV)
        mix_to_fast.append(max(abs(transformed_Mdot[i,j])/abs(ee[j]-ee[i])**2 for i in ff for j in ss))
        mix_to_slow.append(max(abs(transformed_Mdot[i,j])/abs(ee[j]-ee[i])**2 for i in ss for j in ff))

    field_fund = independent_field_fundamental(grid, kval)
    new_fund = author.fundamental(grid, tol=2e-12)
    initial = 1e-5*S0
    reference = {c: independent_closure(grid, kval, initial[:2], c) for c in ('zero', 'adiabatic')}
    scales = np.max(abs(reference['zero']), axis=1)
    prepared = [(0., 0., initial)]
    for eta in (.001, .01, .1):
        prepared.extend((eta, phase, initial+1e-5*eta*w) for phase, w in contamination)
    state_errors, constraint_errors, error_differences, row_results = [], [], [], []
    retained_mismatch = 0.
    qq, kp, _, rr, ww, hh = original.bg(grid, .01)
    for eta, phase, x0 in prepared:
        retained_mismatch = max(retained_mismatch, float(np.max(abs(x0[:2]-initial[:2]))))
        field_values = np.einsum('tij,j->ti', field_fund, x0)
        state_values = from_fields(grid, field_values, kval)
        submitted_values = np.einsum('tij,j->ti', new_fund, x0)
        state_errors.append(float(np.max(abs(state_values-submitted_values))/1e-5))
        phi = field_values[:,3]
        constraint = rr*state_values[:,0]+2*(kval/grid)**2*phi+3*hh*ww*state_values[:,1]
        constraint_errors.append(float(np.max(abs(constraint))/(rr[0]*1e-5)))
        observables = np.array([state_values[:,0], 2*phi])
        for closure, prediction in reference.items():
            errors = np.max(abs(observables-prediction), axis=1)/scales
            submitted_row = next(row for row in point['rows'] if row['eta']==eta and row['phase']==phase and row['closure']==closure)
            error_differences.extend([abs(errors[0]-submitted_row['density_error']), abs(errors[1]-submitted_row['lensing_error'])])
            assert max(errors) > .01
            row_results.append({'eta': eta, 'phase': phase, 'closure': closure,
                                'density_error': float(errors[0]), 'lensing_error': float(errors[1])})
    assert max(state_errors) < 1e-7
    assert max(constraint_errors) < 1e-8
    assert max(error_differences) < 1e-7
    output['points'].append({'k': kval, 'generator_max_absolute_error': matrix_error,
        'initial_fast_coordinate_norm_independent_basis': initial_fast_norm,
        'max_retained_initial_mismatch': retained_mismatch,
        'exact_derivative_fast_from_slow_ratio': float(max(mix_to_fast)),
        'exact_derivative_slow_from_fast_ratio': float(max(mix_to_slow)),
        'finite_difference_fast_from_slow_ratio': diagnostics['max_fast_from_slow_mixing_over_gap'],
        'finite_difference_slow_from_fast_ratio': diagnostics['max_slow_from_fast_mixing_over_gap'],
        'five_field_state_discrepancy_per_delta_i': max(state_errors),
        'five_field_constraint_residual_per_initial_density': max(constraint_errors),
        'max_error_fraction_discrepancy': float(max(error_differences)), 'rows': row_results})
for item in manifest['files']:
    assert digest(SOURCE / item['path']) == item['sha256']
(HERE/'evidence.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps({key: value for key, value in output.items() if key!='points'}, indent=2))
for point in output['points']:
    print(json.dumps({key: value for key,value in point.items() if key!='rows'}, indent=2))
