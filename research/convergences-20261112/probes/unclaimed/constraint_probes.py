#!/usr/bin/env python3
"""Known mechanics, wave-kinematics and stability counterexamples.

No astronomical data or new dynamical theory is fitted here. All units are
dimensionless. The wave snapshots take hbar = m = 1. Standard library only.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path


def smoothstep(u):
    return 10 * u**3 - 15 * u**4 + 6 * u**5


def smoothstep_derivative(u):
    return 30 * u**2 - 60 * u**3 + 30 * u**4


def positions_and_velocities(r, phi, theta, dr, dphi, dtheta, scale=1):
    """Inverse orthonormal Jacobi transform for three equal unit masses."""
    x = scale * cmath.exp(1j * theta)
    y = scale * r * cmath.exp(1j * (theta + phi))
    dx = 1j * dtheta * x
    dy = scale * (dr + 1j * r * (dtheta + dphi)) * cmath.exp(1j * (theta + phi))
    q = [-x / math.sqrt(2) - y / math.sqrt(6),
         x / math.sqrt(2) - y / math.sqrt(6),
         2 * y / math.sqrt(6)]
    dq = [-dx / math.sqrt(2) - dy / math.sqrt(6),
          dx / math.sqrt(2) - dy / math.sqrt(6),
          2 * dy / math.sqrt(6)]
    return q, dq


def side_lengths(q):
    return [abs(q[j] - q[i]) for i, j in [(0, 1), (0, 2), (1, 2)]]


def geometric_phase_probe():
    # Avoid collinear triangles: phi ranges from pi/4 to 3*pi/4.
    p0, sweep = math.pi / 4, math.pi / 2
    corners = [(1, p0), (1, p0 + sweep), (2, p0 + sweep), (2, p0), (1, p0)]
    theta = 0.0
    max_l, max_com, max_kinetic = 0.0, 0.0, 0.0
    q_initial, _ = positions_and_velocities(1, p0, 0, 0, 0, 0)
    for (ra, pa), (rb, pb) in zip(corners[:-1], corners[1:]):
        for i in range(201):
            u = i / 200
            s, ds = smoothstep(u), smoothstep_derivative(u)
            r, phi = ra + (rb - ra) * s, pa + (pb - pa) * s
            dr, dphi = (rb - ra) * ds, (pb - pa) * ds
            # On angular legs r is constant. On radial legs dphi=0.
            angle = theta - r*r / (1+r*r) * (phi-pa)
            dtheta = -r*r / (1+r*r) * dphi
            q, dq = positions_and_velocities(r, phi, angle, dr, dphi, dtheta)
            max_l = max(max_l, abs(sum((z.conjugate()*dz).imag for z, dz in zip(q, dq))))
            max_com = max(max_com, abs(sum(q) / 3))
            max_kinetic = max(max_kinetic, sum(abs(dz)**2 for dz in dq) / 2)
        theta -= rb*rb / (1+rb*rb) * (pb-pa)
    q_final, _ = positions_and_velocities(1, p0, theta, 0, 0, 0)
    shape_error = max(abs(a-b) for a, b in zip(side_lengths(q_initial), side_lengths(q_final)))
    rotation_error = max(abs(b-a*cmath.exp(1j*theta)) for a, b in zip(q_initial, q_final))
    predicted = (4/5 - 1/2) * sweep
    reverse = -sum(rb*rb/(1+rb*rb)*(pb-pa)
                   for (ra, pa), (rb, pb) in zip(corners[:0:-1], corners[-2::-1]))
    retraced = -(1/2)*sweep - (1/2)*(-sweep)
    assert abs(theta - predicted) < 1e-14
    assert abs(reverse + theta) < 1e-14
    assert retraced == 0
    assert max_l < 1e-13 and shape_error < 1e-13 and rotation_error < 1e-13
    return {
        "interpretation": "Prescribed internal actuation, not a free gravitational orbit; no net torque, positive kinetic energy.",
        "shape_loop": [{"r":r, "phi_rad":p} for r,p in corners],
        "net_orientation_degrees": math.degrees(theta),
        "reversed_loop_degrees": math.degrees(reverse),
        "retraced_one_parameter_loop_degrees": math.degrees(retraced),
        "maximum_total_angular_momentum_residual": max_l,
        "maximum_center_of_mass_residual": max_com,
        "maximum_kinetic_energy_for_unit_leg_duration": max_kinetic,
        "side_length_closure_error": shape_error,
        "rotation_reconstruction_error": rotation_error,
        "initial_points": [[z.real,z.imag] for z in q_initial],
        "final_points": [[z.real,z.imag] for z in q_final]
    }


def winding(field, center, radius, n=2048):
    vals = [field((center + radius*cmath.exp(2j*math.pi*k/n)).real,
                  (center + radius*cmath.exp(2j*math.pi*k/n)).imag) for k in range(n)]
    phase = math.fsum(cmath.phase(vals[k].conjugate()*vals[(k+1)%n]) for k in range(n))
    return phase/(2*math.pi)


def wave_probe():
    a, b, alpha = 2.0, 1.0, 0.5
    def shear(x,y):
        return cmath.exp(-0.5*((x/a)**2+(y/b)**2) + 1j*alpha*x*y)
    def pair(x,y):
        return cmath.exp(-0.5*(x*x+y*y)) * complex(x*x+y*y-1, 2*y)
    def pair_current(x,y):
        g = math.exp(-(x*x+y*y))
        return (-4*x*y*g, 2*(x*x-y*y-1)*g)
    # Midpoint quadrature also verifies angular momenta directly from currents.
    n, bound = 480, 12.0
    h = 2*bound/n
    shear_norm_terms, shear_l_terms, pair_norm_terms, pair_l_terms = [], [], [], []
    for i in range(n):
        x = -bound + (i+0.5)*h
        sn, sl, pn, pl = [], [], [], []
        for j in range(n):
            y = -bound + (j+0.5)*h
            rho_s = abs(shear(x,y))**2
            sn.append(rho_s)
            sl.append(rho_s*alpha*(x*x-y*y))
            pn.append(abs(pair(x,y))**2)
            jx,jy = pair_current(x,y)
            pl.append(x*jy-y*jx)
        shear_norm_terms.append(math.fsum(sn)*h*h)
        shear_l_terms.append(math.fsum(sl)*h*h)
        pair_norm_terms.append(math.fsum(pn)*h*h)
        pair_l_terms.append(math.fsum(pl)*h*h)
    sn,sl,pn,pl = map(math.fsum,[shear_norm_terms,shear_l_terms,pair_norm_terms,pair_l_terms])
    expected_shear_l = alpha*(a*a-b*b)/2
    w_plus, w_minus, w_both = winding(pair,1+0j,0.3), winding(pair,-1+0j,0.3), winding(pair,0j,1.5)
    w_shear = winding(shear,0j,1.5)
    assert abs(sl/sn-expected_shear_l) < 1e-12
    assert abs(sn-math.pi*a*b) < 1e-11
    assert abs(pn-3*math.pi) < 1e-11
    assert abs(pl/pn) < 1e-12
    assert abs(w_plus-1) < 1e-12 and abs(w_minus+1) < 1e-12
    assert abs(w_both) < 1e-12 and abs(w_shear) < 1e-12
    return {
        "interpretation": "Normalizable 2D wave snapshots; hbar=m=1; no evolution or halo equilibrium is asserted.",
        "curl_free_shear": {
            "field": "exp[-(x^2/a^2+y^2/b^2)/2 + i alpha x y]",
            "a":a, "b":b, "alpha":alpha,
            "velocity": ["alpha*y", "alpha*x"],
            "analytic_curl":0,
            "zeros":[],
            "enclosed_winding":w_shear,
            "angular_momentum_per_particle":sl/sn,
            "analytic_angular_momentum_per_particle":expected_shear_l,
            "normalization_integral":sn
        },
        "opposite_vortices": {
            "field": "exp[-(x^2+y^2)/2] * (x^2+y^2-1 + 2 i y)",
            "zeros":[[1,0],[-1,0]],
            "windings":[w_plus,w_minus],
            "winding_around_both":w_both,
            "angular_momentum_per_particle":pl/pn,
            "analytic_angular_momentum_per_particle":0,
            "normalization_integral":pn
        }
    }


def rk4_step(y,t,h,coefficient):
    def f(v,tm): return [v[1], -coefficient(tm)*v[0]]
    a=f(y,t)
    b=f([y[i]+h*a[i]/2 for i in range(2)],t+h/2)
    c=f([y[i]+h*b[i]/2 for i in range(2)],t+h/2)
    d=f([y[i]+h*c[i] for i in range(2)],t+h)
    return [y[i]+h*(a[i]+2*b[i]+2*c[i]+d[i])/6 for i in range(2)]


def monodromy(coefficient,period,n=2048):
    cols=[]
    for initial in ([1.,0.],[0.,1.]):
        y=initial[:]
        for k in range(n): y=rk4_step(y,k*period/n,period/n,coefficient)
        cols.append(y)
    a,c=cols[0]
    b,d=cols[1]
    trace,det=a+d,a*d-b*c
    discriminant=cmath.sqrt(trace*trace-4*det)
    eigen=[(trace+discriminant)/2,(trace-discriminant)/2]
    return {"trace":trace,"determinant":det,
            "multiplier_moduli":[abs(z) for z in eigen],
            "stable_linear_equation":abs(trace)<2 and abs(det-1)<1e-10}


def static_and_dynamic_probe():
    charges=[(math.cos(2*math.pi*k/3),math.sin(2*math.pi*k/3),0) for k in range(3)]
    hessian=[[math.fsum(3*q[i]*q[j]-(1 if i==j else 0) for q in charges)
              for j in range(3)] for i in range(3)]
    assert max(abs(hessian[i][j] - ([1.5,1.5,-3][i] if i==j else 0))
               for i in range(3) for j in range(3)) < 1e-14
    # U=cos(Omega*t)*(x^2+y^2-2z^2)/2, with kappa=1.
    cases={}
    for omega in (4.,2.):
        period=2*math.pi/omega
        x=monodromy(lambda t: math.cos(omega*t),period)
        z=monodromy(lambda t: -2*math.cos(omega*t),period)
        # A doubled-step check tests the only numerical dynamical calculation.
        z_fine=monodromy(lambda t: -2*math.cos(omega*t),period,4096)
        assert abs(z_fine['trace']-z['trace']) < 1e-9
        cases[str(omega)]={"x_and_y":x,"z":z,
                           "z_trace_step_halving_difference":abs(z_fine['trace']-z['trace'])}
    assert cases['4.0']['x_and_y']['stable_linear_equation'] and cases['4.0']['z']['stable_linear_equation']
    assert not cases['2.0']['z']['stable_linear_equation']
    static_period=2*math.pi/4
    static=monodromy(lambda t:-2,static_period)
    assert abs(static['trace']-2*math.cosh(math.sqrt(2)*static_period)) < 1e-11
    return {"three_fixed_positive_unit_charges": {
                "positions":charges,"test_charge_mass":1,"test_charge":1,
                "hessian_at_origin":hessian,"hessian_eigenvalues":[1.5,1.5,-3],
                "planar_small_oscillation_frequency":math.sqrt(1.5),
                "vertical_linear_growth_rate":math.sqrt(3)},
            "alternating_quadrupole":{
                "potential":"cos(Omega*t)*(x^2+y^2-2*z^2)/2",
                "laplacian_at_every_time":0,
                "one_period_floquet_results":cases,
                "static_saddle_vertical_monodromy":static,
                "scope":"Ideal linear imposed field. Finite electrodes, noise, nonlinear motion and many particles are omitted."}}


def main():
    results={"status":"Known-model analytical counterexamples with numerical checks; no observational discovery.",
             "geometric_phase":geometric_phase_probe(),
             "vorticity_and_angular_momentum":wave_probe(),
             "force_balance_and_support":static_and_dynamic_probe()}
    dest=Path(__file__).with_name('results.json')
    dest.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"output":str(dest),
                      "shape_loop_degrees":results['geometric_phase']['net_orientation_degrees'],
                      "curl_free_L_per_particle":results['vorticity_and_angular_momentum']['curl_free_shear']['angular_momentum_per_particle'],
                      "vortex_pair_L_per_particle":results['vorticity_and_angular_momentum']['opposite_vortices']['angular_momentum_per_particle'],
                      "quadrupole_omega4_stable":results['force_balance_and_support']['alternating_quadrupole']['one_period_floquet_results']['4.0']['z']['stable_linear_equation']}))


if __name__=='__main__':
    main()
