#!/usr/bin/env python3
"""Action-derived AeST scalar benchmarks. Requires numpy, scipy and sympy.

No nonlinear collapse, observational fit or ultraviolet completion is used.
Run: python3 response.py --output results.json
"""
from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm


def symbolic_checks():
    k, a, H, q, Q, Kp, Kpp, lam, KB = sp.symbols(
        "k a H q Q Kp Kpp lam KB", nonzero=True, real=True
    )
    b = 2 - KB
    v, al, E, Phi, g = sp.symbols("v al E Phi gamma", real=True)
    r = k**2 / a**2
    ch = v + Q * al
    Z = KB * E + b * ch
    D = Q * Kpp * g - r * Z
    pres = Kp * g
    Qd = -3 * H * Kp / Kpp
    Hd = -Q * Kp / 2
    Phid = -H * Phi + Kp * v / 2
    vd = g + Q * Phi
    ald = E - Phi
    Ed = -H * E - b / KB * (g + Qd * al + (H + (1 + lam) * Q) * ch) + Kp / KB * ch
    gd = -3 * H * g + 3 * Kp / Kpp * Phid + r / Kpp * (b * E - b * (1 + lam) * ch + Kp * al)
    variables = [a, H, Q, Kp, v, al, E, Phi, g]
    derivatives = [a * H, Hd, Qd, -3 * H * Kp, vd, ald, Ed, Phid, gd]

    def dt(expr):
        return sp.expand(sum(sp.diff(expr, x) * dx for x, dx in zip(variables, derivatives)))

    energy_balance = sp.simplify(dt(D) + 3 * H * (D + pres) - 3 * Q * Kp * Phid + r * Kp * v)
    trace = sp.simplify(2 * (dt(Phid) + 4 * H * Phid + (2 * Hd + 3 * H**2) * Phi) - pres)
    C = D + 2 * r * Phi + 3 * H * Kp * v
    constraint_propagation = sp.simplify(dt(C) + 3 * H * C)
    # Compensated difference changes gamma and E, with all positions fixed.
    eps = sp.symbols("eps", real=True)
    comp = {v: 0, al: 0, Phi: 0, E: eps, g: r * KB * eps / (Q * Kpp)}
    comp_constraint = sp.simplify(C.subs(comp))
    comp_pressure = sp.factor(pres.subs(comp))
    # Minkowski reduced Hamiltonian in dimensionless Q0=1 units.
    x, p, P = sp.symbols("chi p P", real=True)
    h = p**2 / 16 + (p + P)**2 / (4 * k**2) - (p + P) * x + 3 * k**2 * x**2 - P**2 / (8 * k**2)
    hs = sp.hessian(h, (x, p, P))
    minors = [sp.factor(hs[:n, :n].det()) for n in (1, 2, 3)]
    # Quadratic action lapse variation, including background gravitational terms.
    Psi, Phid_s, vd_s, K = sp.symbols("Psi Phidot vdot K", real=True)
    gam = vd_s - Q * Psi
    Lg = a**3 * (-6 * Phid_s**2 - 12 * H * (Phi + Psi) * Phid_s - 9 * H**2 * (Phi + Psi)**2) + a * k**2 * (2 * Phi**2 - 4 * Phi * Psi)
    La = a**3 * (Kpp * gam**2 + (Q * Kp - K) * Psi**2 - 6 * Kp * Phi * gam - 6 * K * Psi * Phi + 3 * K * Phi**2)
    ad = sp.symbols("alphadot", real=True)
    La += a * k**2 * (KB * (ad + Psi)**2 + 2 * b * (ad + Psi) * ch - b * (1 + lam) * ch**2 + Kp * (2 * al * v + Q * al**2))
    lapse = sp.diff(Lg + La, Psi)
    target = -2 * a**3 * (6 * H * (Phid_s + H * Psi) + 2 * r * Phi + Q * Kpp * gam - r * (KB * (ad + Psi) + b * ch))
    lapse_check = sp.simplify((lapse - target).subs(K, Q * Kp - 3 * H**2))
    p_v = sp.factor(sp.diff(La, vd_s))
    p_a = sp.factor(sp.diff(La, ad))
    checks = {
        "energy_balance": energy_balance,
        "spatial_einstein_trace": trace,
        "constraint_propagation_dotC_plus_3HC": constraint_propagation,
        "compensated_hamiltonian_constraint": comp_constraint,
        "quadratic_action_lapse_constraint": lapse_check,
    }
    for name, value in checks.items():
        assert value == 0, (name, value)
    return {
        "identities": {name: str(value) for name, value in checks.items()},
        "compensated_pressure": str(comp_pressure),
        "momentum_varphi": str(p_v),
        "momentum_alpha": str(p_a),
        "minkowski_hessian_principal_minors": [str(x) for x in minors],
    }


def minkowski():
    rows = []
    for k in [3.0, 4.5, 6.0, 9.0, 12.0]:
        # state=(chi,p,alpha,P), canonical bracket {chi,p}={alpha,P}=1.
        A = np.array([
            [-1, 1 / 8 + 1 / (2 * k*k), 0, 1 / (2 * k*k)],
            [-6 * k*k, 1, 0, 1],
            [-1, 1 / (2 * k*k), 0, 1 / (4 * k*k)],
            [0, 0, 0, 0],
        ], dtype=float)
        omega = np.sqrt(0.75 * k*k + 2)
        initial = np.array([0.0, 8.0e-6, 0.0, 0.0])
        times = np.linspace(0, 20 * np.pi / omega, 201)
        exact = np.array([expm(A * t) @ initial for t in times]).T
        numerical = solve_ivp(lambda t, y: A @ y, (times[0], times[-1]), initial,
                              method="DOP853", t_eval=times, rtol=1e-11, atol=1e-17).y
        def energy(y):
            chi, p, alpha, P = y
            return p*p/16 + (p+P)**2/(4*k*k) - (p+P)*chi + 3*k*k*chi*chi - P*P/(8*k*k)
        energies = energy(exact)
        phis = exact[3] / (4 * k*k)
        gamma = exact[1] / 8
        Z = (exact[1] + exact[3]) / (2 * k*k)
        density = 4 * gamma - k*k*Z
        error = np.max(np.abs(numerical - exact)) / np.max(np.abs(exact))
        eigen = sorted(abs(z.imag) for z in np.linalg.eigvals(A) if abs(z.imag) > 1e-8)
        assert abs(eigen[0] - omega) < 1e-10
        assert np.max(np.abs(density)) < 1e-18
        assert error < 1e-8
        rows.append({
            "k_over_Q0": k, "omega_over_Q0": omega,
            "positive_hessian": bool(k*k > 8),
            "relative_integration_error": float(error),
            "relative_energy_drift": float(np.max(np.abs(energies / energies[0] - 1))),
            "max_abs_effective_density_scaled": float(np.max(np.abs(density))),
            "max_abs_metric_Phi": float(np.max(np.abs(phis))),
            "shift_density_initial": float(exact[1,0]),
            "shift_density_ten_periods": float(exact[1,-1]),
            "max_abs_chi": float(np.max(np.abs(exact[0]))),
        })
    return rows


def bg(a, qi):
    q = qi / a**3
    Q = 1 + q
    Kp, Kpp = 4*q, 4.0
    R = 2*(2*q + q*q)  # 8 pi G rho
    W = Q*Kp  # 8 pi G (rho+p)
    H = np.sqrt(R/3)
    return Q, Kp, Kpp, R, W, H


def background_time_to_scale(end_a, qi):
    # Exact a(t)^3 = 1 + 3 H_i t + 3 qi t^2, in Q0=1 units.
    Hi=bg(1.,qi)[-1]
    return 2*(end_a**3-1)/(3*Hi+np.sqrt(9*Hi*Hi+12*qi*(end_a**3-1)))


def rhs_fields(t, state, k, qi):
    """Independent five-field evolution; does not solve density constraint."""
    a, v, alpha, E, Phi, gamma = state
    Q, Kp, Kpp, R, W, H = bg(a, qi)
    r = (k/a)**2
    chi = v + Q*alpha
    Qdot = -3*H*Kp/Kpp
    Phidot = -H*Phi + Kp*v/2
    Edot = -H*E - (gamma + Qdot*alpha + (H + 2*Q)*chi) + Kp*chi
    gammadot = -3*H*gamma + 3*Kp/Kpp*Phidot + r/Kpp*(E - 2*chi + Kp*alpha)
    return np.array([a*H, gamma + Q*Phi, E-Phi, Edot, Phidot, gammadot])


def rhs_reduced(t, state, k, qi):
    """State=(a,D,m,chi,Z); D,m are scaled density and momentum potential."""
    a, D, m, chi, Z = state
    Q, Kp, Kpp, R, W, H = bg(a, qi)
    r = (k/a)**2
    gamma = (D + r*Z)/(Q*Kpp)
    pres = Kp*gamma
    Phi = -(D + 3*H*m)/(2*r)
    Phidot = -H*Phi + m/2
    Qdot = -3*H*Kp/Kpp
    Ddot = -3*H*(D+pres) + 3*W*Phidot - r*m
    mdot = -3*H*m + pres + W*Phi
    chidot = gamma + Q*Z + (Qdot/Q-Q)*chi - Qdot/(Q*Kp)*m
    Zdot = (-H+Q)*Z + (Kp-3*Q)*chi
    return np.array([a*H, Ddot, mdot, chidot, Zdot])


def physical_fields(a, fields, k, qi):
    v, alpha, E, Phi, gamma = fields
    Q, Kp, Kpp, R, W, H = bg(a, qi)
    chi = v + Q*alpha
    Z = E+chi
    D = Q*Kpp*gamma-(k/a)**2*Z
    m = Kp*v
    return np.array([D, m, chi, Z])


def solve_preparation(k, qi, kind, tol=1e-10, amplitude=1e-6, end_a=2.0):
    Q, Kp, Kpp, R, W, H = bg(1., qi)
    omega = np.sqrt(.75*k*k+2)
    if kind == "velocity":
        f0 = np.array([0, 0, Q*Kpp*amplitude/(k*k), 0, amplitude])
    elif kind == "phase":
        chi0 = amplitude/omega
        f0 = np.array([0, chi0/Q, -chi0, 0, 0])
    elif kind == "held_out_mix":
        chi0 = .37*amplitude/omega
        f0 = np.array([0, chi0/Q, -.61*Q*Kpp*amplitude/(k*k)-chi0, 0, -.61*amplitude])
    else:
        raise ValueError(kind)
    def event(t,y): return y[0] - end_a
    event.terminal, event.direction = True, 1
    span = (0, 10/H)
    sol = solve_ivp(lambda t,y:rhs_fields(t,y,k,qi),span,np.r_[1.,f0],
                    method="DOP853",rtol=tol,atol=tol*amplitude*1e-3,events=event,dense_output=True)
    assert sol.success and sol.t_events[0].size
    times = np.linspace(0,sol.t[-1],2001)
    full = sol.sol(times)
    red0 = physical_fields(1.,f0,k,qi)
    reduced = solve_ivp(lambda t,y:rhs_reduced(t,y,k,qi),(0,times[-1]),np.r_[1.,red0],
                        method="DOP853",t_eval=times,rtol=tol,atol=tol*amplitude*1e-3)
    assert reduced.success
    a = full[0]
    exact_a=(1+3*bg(1.,qi)[-1]*times+3*qi*times**2)**(1/3)
    background_error=float(np.max(abs(a-exact_a)))
    assert background_error<1e-11
    Q,Kp,Kpp,R,W,H = bg(a,qi)
    obs = physical_fields(a,full[1:],k,qi)
    D,m,chi,Z = obs
    Phi = full[4]
    pressure = Kp*full[5]
    C = D+2*(k/a)**2*Phi+3*H*m
    # Absolute residual normalized by actual field source terms, not tiny D alone.
    cnorm = np.max(np.abs(C))/max(amplitude,np.max(np.abs(Q*Kpp*full[5])),np.max(np.abs((k/a)**2*Z)))
    # Compare each physical state with a field-scale floor for near-zero values.
    denom = np.maximum(amplitude,np.max(np.abs(obs),axis=1))
    agreement = np.max(np.abs(obs-reduced.y[1:])/denom[:,None])
    assert cnorm < max(5e-8,100*tol), cnorm
    assert agreement < max(2e-7,300*tol), agreement
    # Gauge invariant nonadiabatic pressure, directly from action coefficients.
    nonad = pressure - Kp/(Q*Kpp)*D
    nonad_error = np.max(np.abs(nonad - Kp/(Q*Kpp)*(k/a)**2*Z))/amplitude
    assert nonad_error < 1e-12
    # Initial canonical constraint differences and auxiliary map.
    p_v = 2*bg(1.,qi)[2]*f0[4] - 6*bg(1.,qi)[1]*f0[3]
    p_al = 2*k*k*(f0[2]+f0[0]+bg(1.,qi)[0]*f0[1])
    canonical_comp = p_al-bg(1.,qi)[0]*p_v
    row = {
        "preparation":kind,"k_over_Q0":k,"q_initial_over_Q0":qi,
        "amplitude":amplitude,"rtol":tol,"a_end":float(a[-1]),
        "time_end_Q0":float(times[-1]),
        "initial_canonical_compensation":float(canonical_comp),
        "initial_delta_nu":float(4*f0[4]/bg(1.,qi)[0]**2),
        "max_constraint_residual_normalized":float(cnorm),
        "max_independent_formulation_error_normalized":float(agreement),
        "initial_pressure_per_amplitude":float(pressure[0]/amplitude),
        "max_abs_density_per_amplitude":float(np.max(np.abs(D))/amplitude),
        "max_abs_momentum_potential_per_amplitude":float(np.max(np.abs(m))/amplitude),
        "max_abs_pressure_per_amplitude":float(np.max(np.abs(pressure))/amplitude),
        "max_abs_lensing_sum_per_amplitude":float(np.max(np.abs(2*Phi))/amplitude),
        "final_density_per_amplitude":float(D[-1]/amplitude),
        "final_momentum_potential_per_amplitude":float(m[-1]/amplitude),
        "min_physical_k_over_Q0":float(k/a[-1]),
        "min_k_over_aH":float(np.min(k/(a*H))),
        "min_flat_gauge_scalar_kinetic_coefficient":float(np.min(2*a**3*Kpp)),
        "min_flat_gauge_vector_kinetic_coefficient":float(np.min(2*a*k*k)),
        "max_background_scale_factor_error":background_error,
        "max_abs_density_contrast":float(np.max(abs(D/R))),
        "max_abs_aether_spatial_amplitude":float(np.max(abs(k*full[2]/a))),
        "max_abs_deltaQ_over_Q":float(np.max(abs(full[5]/Q))),
        "max_abs_metric_Phi":float(np.max(abs(Phi))),
    }
    return row, times, full, obs, pressure


def small_density_limit():
    rows=[]
    k, eps = 6.,1e-6
    for qi in [1e-2,1e-3,1e-4,1e-5]:
        Q,Kp,Kpp,*_=bg(1,qi)
        f0=np.array([1,0,0,Q*Kpp*eps/k**2,0,eps])
        times=np.linspace(0,1,1001)
        s=solve_ivp(lambda t,y:rhs_fields(t,y,k,qi),(0,1),f0,method="DOP853",t_eval=times,rtol=1e-11,atol=1e-20)
        a=s.y[0]
        D,m,chi,Z=physical_fields(a,s.y[1:],k,qi)
        pressure=bg(a,qi)[1]*s.y[5]
        rows.append({"q_initial_over_Q0":qi,"time_end_Q0":1,
                     "max_abs_pressure_per_amplitude":float(np.max(abs(pressure))/eps),
                     "max_abs_density_per_amplitude":float(np.max(abs(D))/eps),
                     "max_abs_density_contrast_per_amplitude":float(np.max(abs(D/bg(a,qi)[3]))/eps),
                     "max_abs_lensing_sum_per_amplitude":float(np.max(abs(2*s.y[4]))/eps)})
    return rows


def approximation_control():
    """Unfitted p=0 and p=c_a^2 D closures against held-out hidden data."""
    qi, delta_i, threshold = .01,1e-5,.01
    Q,Kp,Kpp,R,W,H=bg(1,qi)
    endtime=background_time_to_scale(2.,qi)
    times=np.linspace(0,endtime,2001)
    rows=[]
    for k in [6.,9.,12.,18.,24.]:
        D0=R*delta_i
        m0=-W*H*delta_i/k**2
        closures={}
        for name in ["zero_pressure","adiabatic_pressure"]:
            def rhs(t,y):
                a,D,m=y
                Q,Kp,Kpp,R,W,H=bg(a,qi)
                r=(k/a)**2
                Phi=-(D+3*H*m)/(2*r)
                pressure=0 if name=="zero_pressure" else Kp/(Q*Kpp)*D
                return [a*H,-3*H*(D+pressure)+3*W*(-H*Phi+m/2)-r*m,
                        -3*H*m+pressure+W*Phi]
            s=solve_ivp(rhs,(0,endtime),[1,D0,m0],method="DOP853",t_eval=times,rtol=1e-11,atol=1e-21)
            a,D,m=s.y
            bgv=bg(a,qi)
            closures[name]=(D/bgv[3],-(D+3*bgv[5]*m)/(k/a)**2)
        scales=[np.max(abs(x)) for x in closures['zero_pressure']]
        for kind in ["velocity","phase"]:
            for eta in [0.,.01,.1,1.]:
                if eta==0 and kind=="phase":
                    continue  # Same zero-hidden-data preparation, counted once.
                # gamma hidden amplitude is eta*Q0*delta_i for velocity data.
                # chi hidden amplitude is eta*Q0*delta_i/omega for phase data.
                ch0=0 if kind=="velocity" else eta*delta_i/np.sqrt(.75*k*k+2)
                Z0=Q*Kpp*eta*delta_i/k**2 if kind=="velocity" else 0
                s=solve_ivp(lambda t,y:rhs_reduced(t,y,k,qi),(0,endtime),[1,D0,m0,ch0,Z0],
                            method="DOP853",t_eval=times,rtol=1e-11,atol=1e-21)
                a,D,m,chi,Z=s.y
                bgv=bg(a,qi)
                exact=(D/bgv[3],-(D+3*bgv[5]*m)/(k/a)**2)
                for name,predicted in closures.items():
                    errors=[float(np.max(abs(ex-pred))/scale) for ex,pred,scale in zip(exact,predicted,scales)]
                    rows.append({"k_over_Q0":k,"hidden_preparation":kind,"eta":eta,"closure":name,
                                 "density_error_fraction":errors[0],"lensing_error_fraction":errors[1],
                                 "max_abs_exact_density_contrast":float(np.max(abs(exact[0]))),
                                 "max_abs_exact_lensing_sum":float(np.max(abs(exact[1]))),
                                 "passes_1_percent":max(errors)<=threshold})
    return {"threshold_fraction":threshold,"delta_initial":delta_i,
            "normalization":"maximum of each observable in the zero-pressure reference",
            "rows":rows}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=Path(__file__).with_name("results.json"))
    args=ap.parse_args()
    results={"scope":"Linear classical AeST tracking benchmark; no collapse or observational fit",
             "environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__},
             "parameters":{"KB":1,"K2":2,"lambda_s":1,"Q0_unit":1,"q_initial_over_Q0":.01,"amplitude":1e-6},
             "symbolic":symbolic_checks(),"minkowski":minkowski(),"flrw":[]}
    solutions={}
    for k in [6.,9.,12.,18.,24.]:
        for kind in ["velocity","phase","held_out_mix"]:
            row,times,full,obs,pres=solve_preparation(k,.01,kind)
            results["flrw"].append(row)
            solutions[(k,kind)]=(times,full,obs,pres)
    # Superposition is checked on a common time grid, including the independent
    # phase preparation withheld from the compensated-velocity example.
    mix_errors=[]
    for k in [6.,9.,12.,18.,24.]:
        mix=solutions[(k,"held_out_mix")][2]
        expected=-.61*solutions[(k,"velocity")][2]+.37*solutions[(k,"phase")][2]
        mix_errors.append(float(np.max(np.abs(mix-expected))/1e-6))
    results["held_out_superposition_max_error_per_amplitude"]=max(mix_errors)
    assert max(mix_errors)<1e-7
    results["tolerance_control"]=[]
    for tol in [1e-8,1e-10,1e-12]:
        row,*_=solve_preparation(12.,.01,"velocity",tol)
        results["tolerance_control"].append(row)
    results["amplitude_control"]=[]
    for amp in [1e-7,1e-6,1e-5]:
        row,*_=solve_preparation(12.,.01,"velocity",amplitude=amp)
        results["amplitude_control"].append(row)
    ampkeys=["max_abs_density_per_amplitude","max_abs_pressure_per_amplitude","max_abs_lensing_sum_per_amplitude"]
    amp_error=max(float(np.ptp([r[key] for r in results['amplitude_control']])) for key in ampkeys)
    results['amplitude_control_max_normalized_response_spread']=amp_error
    assert amp_error<1e-8
    results["small_density_fixed_time_limit"]=small_density_limit()
    results["approximation_control"]=approximation_control()
    args.output.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps({"output":str(args.output),"flrw_preparations":len(results["flrw"]),
                      "max_constraint_residual":max(x["max_constraint_residual_normalized"] for x in results["flrw"]),
                      "max_formulation_difference":max(x["max_independent_formulation_error_normalized"] for x in results["flrw"]),
                      "all_assertions_passed":True},indent=2))


if __name__=="__main__": main()
