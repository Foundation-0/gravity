#!/usr/bin/env python3
"""Independent numerical and provenance controls for the frozen Wave corrections.

Usage: python3 check.py /path/to/reviewed/gravity/checkout
Only the directory containing this reviewer script receives output.
"""
from pathlib import Path
import hashlib, importlib.util, json, math, re, subprocess, sys
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
EXPECTED_HEAD = 'e5d7ee813e33de03c91857e48a2d55a0caf55506'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def sha(data):
    return hashlib.sha256(data).hexdigest()

git('cat-file', '-e', EXPECTED_HEAD+'^{commit}')
changed = git('diff', '--name-only', EXPECTED_HEAD+'^', EXPECTED_HEAD).decode().splitlines()
assert not any(name.startswith('formal/') for name in changed)
source_hashes = {name: sha((ROOT/name).read_bytes()) for name in changed}
for name, actual in source_hashes.items():
    assert actual == sha(git('show', EXPECTED_HEAD+':'+name)), name

def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/(name+'.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

w11 = module('wave11_machian_pairing_unification')
w12 = module('wave12_cosmic_dawn_quasar_collapse')

# Integrate an analytic potential using a different endpoint substitution from
# the submission. The RAR excess has an elementary antiderivative.
def exact_potential_time(mass, radius, a0=None, added=0.):
    g0 = w12.G*mass/radius**2
    q = None if a0 is None else math.sqrt(g0/a0)
    start_force = 1+added+(0. if q is None or q>700 else 1/math.expm1(q))
    def integrand(u):
        if u == 0.:
            return math.sqrt(2/start_force)
        if u == 1.:
            return 0.
        x = 1-u*u
        drop = (1+added)*u*u/x
        if q is not None and q < 700:
            drop += math.log1p(-math.expm1(-q*u*u/x)/math.expm1(q))/q
        return 2*u/math.sqrt(2*drop)
    value, err = quad(integrand, 0., 1., epsabs=2e-13, epsrel=2e-13, limit=500)
    return math.sqrt(radius/g0)*value, err

def radial_ode_time(mass, radius, a0=None, added=0.):
    g0 = w12.G*mass/radius**2
    q = None if a0 is None else math.sqrt(g0/a0)
    def derivative(t, state):
        x, vel = state
        enhancement = 1. if q is None else 1/(-math.expm1(-q/x))
        return [vel, -(enhancement+added)/(x*x)]
    def stop(t, state):
        return state[0]-1e-7
    stop.terminal = True
    stop.direction = -1
    sol = solve_ivp(derivative, (0., 2.), [1., 0.], events=stop, method='DOP853',
                    rtol=2e-12, atol=2e-14, max_step=.001)
    assert sol.success and len(sol.t_events[0]) == 1
    return math.sqrt(radius/g0)*sol.t_events[0][0]

mass, radius = 5e10*w12.M_SUN, 30*w12.KPC
g0 = w12.G*mass/radius**2
c32 = w12.audit_c32_two_branch_condensate_and_phonon_collapse()
# Reconstruct the unrounded trapping fraction from the submitted spectrum,
# because the certificate deliberately stores its rounded presentation value.
sigma = w12.build_sigma_r_evaluator()
scale = brentq(lambda r:sigma(r, w12.Z_PAIR)-1.686, 1e-4, 1., xtol=1e-15)
rho = w12.OMEGA_M*w12.RHO_CRIT0
mstar = 4*math.pi/3*(scale*w12.MPC)**3*rho
hz = w12.H0_SI*w12.e_hubble(w12.Z_PAIR)
dispersion = (10*w12.G*mstar*hz)**(1/3)/1000/math.sqrt(2)
fraction = 1-(dispersion/(250/math.sqrt(2)))**2
added = w12.OMEGA_C/w12.OMEGA_B*fraction
cases = [('Newton', None, 0.), ('constant_a0_RAR', w12.A0_EMP, 0.),
         ('Hubble_a0_RAR', w12.C_SI*hz/(2*math.pi), 0.),
         ('RAR_plus_assigned_mass', w12.A0_EMP, added)]
radial = []
for label, a0, extra in cases:
    exact, quadrature_error = exact_potential_time(mass, radius, a0, extra)
    submitted = w12.radial_point_mass_fall_time(mass, radius, a0, extra)
    ode = radial_ode_time(mass, radius, a0, extra)
    assert abs(submitted/exact-1) < 2e-10
    assert abs(ode/exact-1) < 1e-9
    radial.append({'case':label, 'analytic_potential_Myr':exact/w12.MYR,
                   'submitted_Myr':submitted/w12.MYR, 'radial_ODE_Myr':ode/w12.MYR,
                   'submitted_relative_error':submitted/exact-1,
                   'ODE_relative_error':ode/exact-1,
                   'dimensionless_outer_quadrature_error_estimate':quadrature_error})

newton = math.pi/(2*math.sqrt(2))*math.sqrt(radius**3/(w12.G*mass))
newton_controls=[]
for extra in (0., .1, 5.36, 20.):
    exact = newton/math.sqrt(1+extra)
    result = w12.radial_point_mass_fall_time(mass, radius, additive_mass_ratio=extra)
    assert abs(result/exact-1) < 2e-14
    newton_controls.append({'added_mass_ratio':extra,'relative_error':result/exact-1})
high_acceleration = w12.radial_point_mass_fall_time(mass, radius, g0/1e8)
assert abs(high_acceleration/newton-1) < 2e-14
deep=[]
for q0 in (.01, .001, .0001):
    a0 = g0/q0**2
    V = (w12.G*mass*a0)**.25
    deep_limit = math.sqrt(math.pi/2)*radius/V
    exact, _ = exact_potential_time(mass, radius, a0)
    numerical = w12.radial_point_mass_fall_time(mass, radius, a0, intervals=512)
    deep.append({'q0':q0,'RAR_over_exact_deep_MOND':exact/deep_limit,
                 'submitted_over_exact_RAR':numerical/exact,
                 'old_shortcut_over_exact_deep_MOND':math.sqrt(math.pi)/2})
assert abs(deep[-1]['RAR_over_exact_deep_MOND']-1) < 5e-4
assert all(abs(row['submitted_over_exact_RAR']-1) < 5e-7 for row in deep)

# Independent opacity and mass-energy derivation. kappa_HHe/kappa_H=1-Y/2.
tedd = w12.SIGMA_T*w12.C_SI/(4*math.pi*w12.G*w12.M_P)/w12.MYR
efolds = math.log(1.5e9/100)
growth=[]
for epsilon in (.1, 1-math.sqrt(8/9)):
    for label, opacity_ratio in [('pure_H',1.),('primordial_H_He',1-.245/2)]:
        time = efolds*epsilon/(1-epsilon)*tedd*opacity_ratio
        growth.append({'epsilon':epsilon,'composition':label,'time_Myr':time})
seed = w12.audit_c31_salpeter_seed_and_clustering_wall()['seed_duty_cycle_audit_for_J1602A_1p5e9_Msun']
assert abs(seed['popIII_100Msun_req_time_primordial_H_He_eps0p10_Myr']-growth[1]['time_Myr'])<.0005
assert abs(seed['popIII_100Msun_req_time_pure_H_Schwarzschild_Myr']-growth[2]['time_Myr'])<.0005
assert abs(seed['popIII_100Msun_req_time_primordial_H_He_Schwarzschild_Myr']-growth[3]['time_Myr'])<.0005
slim=[]
for mdot in (.1,1.,2.,3.,5.,10.):
    lam = mdot if mdot<=2 else 2*(1+math.log(mdot/2))
    retained = mdot-.1*lam
    exact = efolds*.1*tedd/retained
    submitted_lam, submitted_time = w12.slim_disk_growth_time_myr(efolds,mdot)
    assert abs(submitted_time/exact-1)<2e-15 and submitted_lam==lam
    slim.append({'mdot':mdot,'lambda':lam,'retained_dimensionless_rate':retained,'time_Myr':exact})

curvature=[]
for ok in (-.01,-.004,-.001,0.,.01):
    assert abs(w11.closed_cpl_hubble_squared(1.,ok)-1)<1e-14
    row={'Omega_k':ok,'H2_at_a1':w11.closed_cpl_hubble_squared(1.,ok)}
    if ok<0:
        turn=brentq(lambda aa:w11.closed_cpl_hubble_squared(aa,ok),2.,2000.)
        row['turnaround_scale_factor']=turn
        row['matter_curvature_limit']=w11.OMEGA_M/abs(ok)
    curvature.append(row)

u, K2, Q0, Q = sp.symbols('u K2 Q0 Q', positive=True)
P=K2*((Q/Q0)**2-1)**2
current=sp.diff(P,Q)
curvature_polynomial=sp.diff(P,Q,2)
assert sp.simplify(curvature_polynomial.subs(Q,0)+4*K2/Q0**2)==0
assert sp.simplify(curvature_polynomial.subs(Q,Q0/sp.sqrt(3)))==0
assert current.subs(Q,0)==0
assert sp.simplify(current.subs(Q,-Q)+current)==0
# For L=a^3 P(phidot), Euler-Lagrange gives d(a^3 P_Q)/dt=0.
# Derivative-only portals are unchanged by a constant shift of phi.

def manifest_map(data):
    return {line.split(None,1)[1]:line.split(None,1)[0] for line in data.decode().splitlines() if line.strip()}
current_manifest=manifest_map((ROOT/'SHA256SUMS').read_bytes())
parent_manifest=manifest_map(git('show',EXPECTED_HEAD+'^:SHA256SUMS'))
inherited_mismatches=[]
for name, expected in current_manifest.items():
    actual=sha((ROOT/name).read_bytes())
    if actual!=expected:
        assert name not in changed
        parent_actual=sha(git('show',EXPECTED_HEAD+'^:'+name))
        assert parent_actual==actual and parent_manifest[name]==expected
        inherited_mismatches.append(name)
for name in changed:
    if name!='SHA256SUMS': assert current_manifest[name]==source_hashes[name]

checks=[]
for args in [['-m','unittest','test_wave11_12_corrections.py'],
             ['wave11_machian_pairing_unification.py','--check'],
             ['wave12_cosmic_dawn_quasar_collapse.py','--check']]:
    result=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0
    stable_output = re.sub(r'Ran (\d+) tests? in [\d.]+s',
                           r'Ran \1 tests (elapsed time omitted)', result.stdout+result.stderr)
    checks.append({'command':'python3 '+' '.join(args),'returncode':result.returncode,
                   'output':stable_output})
for name, expected in source_hashes.items():assert sha((ROOT/name).read_bytes())==expected
evidence={'reviewed_commit':EXPECTED_HEAD,'source_sha256':source_hashes,
          'radial_comparisons':radial,'newtonian_controls':newton_controls,
          'high_acceleration_relative_error':high_acceleration/newton-1,
          'deep_MOND_controls':deep,'growth_counterexamples':growth,'slim_disk':slim,
          'curvature_controls':curvature,'polynomial_curvature':str(curvature_polynomial),
          'formal_files_unchanged':True,'inherited_global_manifest_mismatches':inherited_mismatches,
          'all_changed_manifest_entries_match':True,'author_checks':checks}
(HERE/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({key:value for key,value in evidence.items() if key not in ('source_sha256','author_checks')},indent=2))
