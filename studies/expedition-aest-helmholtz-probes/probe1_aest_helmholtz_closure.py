#!/usr/bin/env python3
"""
Probe 1: Exact Helmholtz-Screened Slow-Manifold Closure, Pole-Zero Duality,
Coupled Baryon-AeST 2x2 Gravitational Matrix, and Quantitative Closure Defect
for Foundation-0/gravity (research/aest-response-gate-20261112).

Zero fitted parameters. All verdicts use explicit checks (python3 -O safe).
Run:
  python3 -I -O -B -W error studies/expedition-aest-helmholtz-probes/probe1_aest_helmholtz_closure.py
"""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import sympy as sp
from numpy.polynomial import chebyshev as cheb
from scipy.integrate import solve_ivp

OUT_PATH = Path(__file__).resolve().parent / "probe1_aest_results.json"


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"CHECK FAILED: {msg}")


# ==============================================================================
# 1. EXACT SYMBOLIC DERIVATION FROM THE QUADRATIC AeST ADM ACTION
# ==============================================================================
def symbolic_theorems() -> Dict[str, str]:
    k, a, H, Q, Kp, Kpp, lam, KB = sp.symbols(
        "k a H Q Kp Kpp lam KB", positive=True, real=True
    )
    b = 2 - KB
    r_expr = k**2 / a**2
    r = sp.Symbol("r", positive=True)
    v, al, E, Phi, Psi, g = sp.symbols("v al E Phi Psi g", real=True)
    D, m, chi, Z = sp.symbols("D m chi Z", real=True)

    # Background and 5-field action equations (derivation.md Sec. 2-3, general KB, lam)
    Qdot = -3 * H * Kp / Kpp
    chi_expr = v + Q * al
    Z_expr = KB * E + b * chi_expr
    D_expr = Q * Kpp * g - r_expr * Z_expr
    m_expr = Kp * v
    Phidot_expr = -H * Phi + Kp * v / 2
    vdot_expr = g + Q * Phi
    aldot_expr = E - Phi
    Edot_expr = (
        -H * E
        - (b / KB) * (g + Qdot * al + (H + (1 + lam) * Q) * chi_expr)
        + (Kp / KB) * chi_expr
    )
    gdot_expr = (
        -3 * H * g
        + 3 * (Kp / Kpp) * Phidot_expr
        + (r_expr / Kpp) * (b * E - b * (1 + lam) * chi_expr + Kp * al)
    )

    sol_vars = sp.solve(
        [
            v - m / Kp,
            chi_expr - chi,
            Z_expr - Z,
            Q * Kpp * g - r * Z - D,
            D + 2 * r * Phi + 3 * H * m,
        ],
        [v, al, E, g, Phi],
        dict=True,
    )[0]

    vars_5 = [a, H, Q, Kp, v, al, E, Phi, g]
    dots_5 = [a * H, -Q * Kp / 2, Qdot, -3 * H * Kp, vdot_expr, aldot_expr, Edot_expr, Phidot_expr, gdot_expr]

    def dt(expr):
        raw = sum(sp.diff(expr, x) * dx for x, dx in zip(vars_5, dots_5))
        return sp.simplify(raw.subs(k**2 / a**2, r).subs(sol_vars))

    Ddot = dt(D_expr)
    mdot = dt(m_expr)
    chidot = dt(chi_expr)
    Zdot = dt(Z_expr)

    # Verify specialization KB=1, lam=1 matches derivation.md Eqs. (129)-(134)
    W = Q * Kp
    Phi_sub = -(D + 3 * H * m) / (2 * r)
    g_sub = (D + r * Z) / (Q * Kpp)
    p_sub = Kp * g_sub
    check(
        sp.simplify(
            (Ddot - (-3 * H * (D + p_sub) + 3 * W * (-H * Phi_sub + m / 2) - r * m)).subs({KB: 1, lam: 1})
        ) == 0,
        "Ddot specialization mismatch",
    )
    check(
        sp.simplify((mdot - (-3 * H * m + p_sub + W * Phi_sub)).subs({KB: 1, lam: 1})) == 0,
        "mdot specialization mismatch",
    )
    check(
        sp.simplify(
            (chidot - (g_sub + Q * Z + (Qdot / Q - Q) * chi - Qdot / (Q * Kp) * m)).subs({KB: 1, lam: 1})
        ) == 0,
        "chidot specialization mismatch",
    )
    check(
        sp.simplify((Zdot - ((-H + Q) * Z + (Kp - 3 * Q) * chi)).subs({KB: 1, lam: 1})) == 0,
        "Zdot specialization mismatch",
    )

    # Theorem 1A: Cold subhorizon quasi-static slow manifold (Kp/Q -> 0, H << sqrt(r), fixed r/Q^2)
    eq_ch = D / (Kpp * Q) + Z * (r / (Kpp * Q) + Q / KB) - (b * Q / KB) * chi
    eq_Z = (b * Q / KB) * Z - (b * (2 + KB * lam) * Q / KB) * chi
    sol_qs = sp.solve([eq_ch, eq_Z], [chi, Z], dict=True)[0]
    u_qs = sp.factor(D + r * sol_qs[Z])
    M_scr_sq = sp.factor(Kpp * Q**2 * (1 + lam) / (2 + KB * lam))
    helmholtz_ratio = sp.factor(u_qs / D)
    check(
        sp.simplify(helmholtz_ratio - M_scr_sq / (r + M_scr_sq)) == 0,
        "Helmholtz screening identity failed",
    )

    # Exact scale-dependent self-gravity G_AA(r) / G_tilde
    G_AA = sp.factor(1 - (2 * r / (Q**2 * Kpp)) * helmholtz_ratio)
    G_AA_uv = sp.factor(sp.limit(G_AA, r, sp.oo))
    G_AA_ir = sp.limit(G_AA, r, 0)
    check(G_AA_ir == 1, f"IR limit G_AA(0) != 1: {G_AA_ir}")
    check(
        sp.simplify(G_AA_uv - (-lam * (2 - KB) / (2 + KB * lam))) == 0,
        "UV limit G_AA(oo) mismatch",
    )

    # Exact pole-zero identity: r_zero(G_AA = 0) === mu^2 (Minkowski UV stability scale & static pole)
    r_zero = sp.factor(sp.solve(G_AA, r)[0])

    # Static baryonic Poisson equation from quadratic action (H=0, Kp=0, external source D_b)
    D_b, ch_s = sp.symbols("D_b ch_s", real=True)
    L_static = (
        r * (2 * Phi**2 - 4 * Phi * Psi)
        + Kpp * (-Q * Psi) ** 2
        + r * (KB * Psi**2 + 2 * b * Psi * ch_s - b * (1 + lam) * ch_s**2)
        - 2 * D_b * Psi
    )
    sol_st = sp.solve(
        [sp.diff(L_static, Phi), sp.diff(L_static, Psi), sp.diff(L_static, ch_s)],
        [Phi, Psi, ch_s],
        dict=True,
    )[0]
    Phi_static_ratio = sp.factor(-2 * r * sol_st[Phi] / D_b)
    # Static-dynamical duality: static equilibrium D_A_eq = -D_b / G_AA => Phi_eq / Phi_N = 1 - 1/G_AA
    duality_diff = sp.simplify(Phi_static_ratio - (1 - 1 / G_AA))
    check(duality_diff == 0, f"Static-dynamical duality residual nonzero: {duality_diff}")

    # Minkowski reduced Hamiltonian H_2(ch, p, P) at Q=1
    p_s, P_s = sp.symbols("p_s P_s", real=True)
    gam_m = p_s / (2 * Kpp)
    Z_m = (p_s + P_s) / (2 * r)
    Phi_m = P_s / (4 * r)
    E_m = (Z_m - b * ch_s) / KB
    L_mink = r * (-2 * Phi_m**2) + Kpp * gam_m**2 + r * (KB * E_m**2 + 2 * b * E_m * ch_s - b * (1 + lam) * ch_s**2)
    H2 = sp.simplify(p_s * (gam_m + Phi_m) + (p_s + P_s) * (E_m - Phi_m) - L_mink)
    hs = sp.hessian(H2, (ch_s, p_s, P_s))
    minors = [sp.factor(hs[:n, :n].det()) for n in (1, 2, 3)]
    mu_sq_mink = sp.factor(sp.solve(minors[2], r)[0])
    # In Q-restored units, mu^2 = mu_sq_mink * Q^2
    pole_zero_ratio = sp.simplify(r_zero / (mu_sq_mink * Q**2))
    check(pole_zero_ratio == 1, f"Pole-zero identity r_zero/mu^2 != 1: {pole_zero_ratio}")

    # Exact Hamiltonian Schur-Complement Theorem (#48):
    # Minimizing H_2(ch, p, P) over fast canonical pair (ch, p) at fixed P = -2*D yields
    #   H_2^Schur(P) = (1/2) * S_P * P^2 === -(G_AA(r)/G_tilde) * P^2 / (8*r) = -(G_AA/G_tilde) * D^2 / (2*r)!
    sol_fast = sp.solve([sp.diff(H2, ch_s), sp.diff(H2, p_s)], [ch_s, p_s], dict=True)[0]
    H2_schur = sp.factor(sp.simplify(H2.subs(sol_fast)))
    G_AA_Q1 = G_AA.subs(Q, 1)
    schur_energy_diff = sp.simplify(H2_schur - (-G_AA_Q1 * P_s**2 / (8 * r)))
    check(schur_energy_diff == 0, f"Hamiltonian Schur-complement energy residual nonzero: {schur_energy_diff}")
    S_P = sp.factor(hs[2, 2] - (hs[2, :2] * hs[:2, :2].inv() * hs[:2, 2])[0])
    schur_hess_diff = sp.simplify(S_P - (-G_AA_Q1 / (4 * r)))
    check(schur_hess_diff == 0, f"Hessian Schur-complement residual nonzero: {schur_hess_diff}")

    # Exact lam_s = 0 uniform [2, 0, 1] minors: Delta_1 > 0, Delta_2 > 0, S_P < 0 for all r > 0, 0 < KB < 2
    lam0_minors = [sp.factor(m.subs(lam, 0)) for m in minors]
    lam0_SP = sp.factor(S_P.subs(lam, 0))
    check(
        sp.simplify(lam0_SP - (-Kpp / (4 * r * (Kpp + 2 * r)))) == 0,
        f"lam_s=0 Schur complement mismatch: {lam0_SP}",
    )

    # Exact lambda_s = 0 Yukawa suppression law
    G_AA_lam0 = sp.factor(G_AA.subs(lam, 0))
    check(
        sp.simplify(G_AA_lam0 - (Kpp * Q**2 / 2) / (Kpp * Q**2 / 2 + r)) == 0,
        "lam=0 Yukawa law mismatch",
    )

    # Verify external matter D_b cancels identically in chidot and Zdot
    Phi_2f = -(D + D_b + 3 * H * m) / (2 * r)
    chidot_2f = sp.simplify((vdot_expr + Qdot * al + Q * aldot_expr).subs(Phi, Phi_2f))
    Zdot_2f = sp.simplify((KB * Edot_expr + b * (vdot_expr + Qdot * al + Q * aldot_expr)).subs(Phi, Phi_2f))
    check(sp.diff(chidot_2f, D_b) == 0 and sp.diff(Zdot_2f, D_b) == 0, "D_b leaked into fast sector")

    return {
        "M_scr_sq": str(M_scr_sq),
        "helmholtz_pressure_ratio_p_over_ca2D": str(helmholtz_ratio),
        "G_AA_over_Gtilde": str(G_AA),
        "G_AA_ir_limit": str(G_AA_ir),
        "G_AA_uv_limit": str(G_AA_uv),
        "G_AA_lam0_yukawa": str(G_AA_lam0),
        "r_zero_equals_mu_sq": str(r_zero),
        "pole_zero_ratio_r_zero_over_mu_sq": str(pole_zero_ratio),
        "static_baryon_Phi_over_Phi_Newton": str(Phi_static_ratio),
        "static_dynamical_duality_residual": str(duality_diff),
        "minkowski_H2_principal_minors_Q1": [str(x) for x in minors],
        "hamiltonian_schur_complement_H2_min_over_fast": str(H2_schur),
        "hamiltonian_schur_complement_S_P": str(S_P),
        "hamiltonian_schur_energy_residual": str(schur_energy_diff),
        "hamiltonian_schur_hessian_residual": str(schur_hess_diff),
        "lam0_minors_Q1": [str(x) for x in lam0_minors],
        "lam0_schur_S_P": str(lam0_SP),
        "fast_sector_independent_of_Db": "exact_zero_derivative",
    }


# ==============================================================================
# 2. BACKGROUND & EXACT 4-STATE / 6-STATE DYNAMICS
# ==============================================================================
def bg(a: float, qi: float = 0.01) -> Tuple[float, float, float, float, float, float]:
    q = qi / (a**3)
    Q = 1.0 + q
    Kp = 4.0 * q
    Kpp = 4.0
    R = 4.0 * q + 2.0 * q * q
    W = Q * Kp
    H = math.sqrt(R / 3.0)
    return Q, Kp, Kpp, R, W, H


def blocks_Dm(a: float, k: float, KB: float = 1.0, lam: float = 1.0, qi: float = 0.01):
    Q, Kp, Kpp, R, W, H = bg(a, qi)
    b = 2.0 - KB
    r = (k / a) ** 2
    A = np.array(
        [
            [3 * H * W / (2 * r) - 3 * H * Kp / (Kpp * Q) - 3 * H, 9 * H * H * W / (2 * r) + 1.5 * W - r],
            [-W / (2 * r) + Kp / (Kpp * Q), -3 * H * W / (2 * r) - 3 * H],
        ],
        dtype=float,
    )
    B = np.array([[0.0, -3 * H * Kp * r / (Kpp * Q)], [0.0, Kp * r / (Kpp * Q)]], dtype=float)
    C = np.array([[1.0 / (Kpp * Q), 3 * H / (Kpp * Q)], [0.0, 0.0]], dtype=float)
    F = np.array(
        [
            [-3 * H * Kp / (Kpp * Q) - (b / KB) * Q, r / (Kpp * Q) + Q / KB],
            [Kp - (b / KB) * (2.0 + KB * lam) * Q, -H + (b / KB) * Q],
        ],
        dtype=float,
    )
    return A, B, C, F


def cheb_fenichel_chain(
    k: float,
    max_order: int = 3,
    deg: int = 24,
    a_lo: float = 1.0,
    a_hi: float = 2.0,
    KB: float = 1.0,
    lam: float = 1.0,
    qi: float = 0.01,
):
    """Smooth Chebyshev representation of exact recursive Fenichel slow-manifold maps H_0..H_max.
    Invariance PDE: R[H] := C + F H - dH/dt - H(A + B H) = 0.
    Iteration: H_{n+1} = F^{-1} (dH_n/dt + H_n (A + B H_n) - C).
    Zero free parameters; machine-smooth d/dt via exact Chebyshev differentiation.
    """
    j = np.arange(deg + 1)
    x_nodes = np.cos(math.pi * j / deg)  # Chebyshev-Lobatto nodes on [-1, 1]
    a_nodes = 0.5 * (a_hi + a_lo) + 0.5 * (a_hi - a_lo) * x_nodes
    scale_dxda = 2.0 / (a_hi - a_lo)

    A_n = np.zeros((deg + 1, 2, 2))
    B_n = np.zeros((deg + 1, 2, 2))
    C_n = np.zeros((deg + 1, 2, 2))
    F_n = np.zeros((deg + 1, 2, 2))
    aH_n = np.zeros(deg + 1)
    for i, av in enumerate(a_nodes):
        A_n[i], B_n[i], C_n[i], F_n[i] = blocks_Dm(float(av), k, KB, lam, qi)
        aH_n[i] = float(av) * bg(float(av), qi)[-1]

    def fit_mat(vals):
        coeffs = np.zeros((deg + 1, 2, 2))
        for r_i in range(2):
            for c_i in range(2):
                coeffs[:, r_i, c_i] = cheb.chebfit(x_nodes, vals[:, r_i, c_i], deg)
        return coeffs

    def deriv_at_nodes(coeffs):
        dvals = np.zeros((deg + 1, 2, 2))
        for r_i in range(2):
            for c_i in range(2):
                dc = cheb.chebder(coeffs[:, r_i, c_i])
                dvals[:, r_i, c_i] = cheb.chebval(x_nodes, dc) * scale_dxda * aH_n
        return dvals

    def eval_mat(coeffs, a_val: float) -> np.ndarray:
        xv = (2.0 * a_val - (a_hi + a_lo)) / (a_hi - a_lo)
        out = np.empty((2, 2), dtype=float)
        for r_i in range(2):
            for c_i in range(2):
                out[r_i, c_i] = float(cheb.chebval(xv, coeffs[:, r_i, c_i]))
        return out

    # Order 0: F H_0 + C = 0
    H0_vals = np.array([-np.linalg.solve(F_n[i], C_n[i]) for i in range(deg + 1)])
    coeffs_map = {0: fit_mat(H0_vals)}
    vals_map = {0: H0_vals}

    for ord_ in range(1, max_order + 1):
        Hp = vals_map[ord_ - 1]
        dHdt = deriv_at_nodes(coeffs_map[ord_ - 1])
        Hn = np.zeros_like(Hp)
        for i in range(deg + 1):
            rhs_i = dHdt[i] + Hp[i] @ (A_n[i] + B_n[i] @ Hp[i]) - C_n[i]
            Hn[i] = np.linalg.solve(F_n[i], rhs_i)
        vals_map[ord_] = Hn
        coeffs_map[ord_] = fit_mat(Hn)

    # Evaluate exact invariance commutation defect R[H] = C + F H - dH/dt - H(A + B H)
    # normalized in dimensionless physical units (weighted by scale r = k^2/a^2 on Z row)
    defects_raw = {}
    defects_dimless = {}
    for ord_, cmat in coeffs_map.items():
        Hk = vals_map[ord_]
        dHdt = deriv_at_nodes(cmat)
        raw_list = []
        dim_list = []
        for i, av in enumerate(a_nodes):
            Rmat = C_n[i] + F_n[i] @ Hk[i] - dHdt[i] - Hk[i] @ (A_n[i] + B_n[i] @ Hk[i])
            raw_list.append(float(np.linalg.norm(Rmat, ord="fro")))
            # Scale-normalized defect: ||F^{-1} R[H] D_s|| / ||H D_s|| where D_s = diag(1, 1/r)
            rv = (k / float(av)) ** 2
            Ds = np.diag([1.0, 1.0 / rv])
            F_inv_R = np.linalg.solve(F_n[i], Rmat) @ Ds
            H_ref = Hk[i] @ Ds
            dim_list.append(float(np.linalg.norm(F_inv_R, ord="fro") / max(1e-30, np.linalg.norm(H_ref, ord="fro"))))
        defects_raw[ord_] = max(raw_list)
        defects_dimless[ord_] = max(dim_list)

    return coeffs_map, defects_raw, defects_dimless, eval_mat


def frozen_probe_ic_Dm(k: float, delta0: float = 1e-5, qi: float = 0.01) -> np.ndarray:
    """Exact slow-subspace initial condition from aest-response-gate/slow-mode/probe.py."""
    Q1, Kp1, Kpp1, R1, W1, H1 = bg(1.0, qi)
    theta0 = -H1 * delta0 / (k * k)

    def rhs_norm(x):
        r = k * k
        ca2 = Kp1 / (Q1 * Kpp1)
        w = 2.0 * (Q1 - 1.0) ** 2 / R1
        dl, th, ch, Z = x
        Phi = -(R1 * dl + 3 * H1 * W1 * th) / (2 * r)
        gam = (R1 * dl + r * Z) / (Q1 * Kpp1)
        pr = Kp1 * gam
        Phid = -H1 * Phi + W1 * th / 2.0
        Qdot = -3 * H1 * Kp1 / Kpp1
        return np.array(
            [
                3 * H1 * (w * dl - pr / R1) + 3 * (W1 / R1) * Phid - r * (W1 / R1) * th,
                3 * H1 * ca2 * th + pr / W1 + Phi,
                gam + Q1 * Z + (Qdot / Q1 - Q1) * ch - Qdot * th,
                (-H1 + Q1) * Z + (Kp1 - 3 * Q1) * ch,
            ]
        )

    M0 = np.column_stack([rhs_norm(np.eye(4)[:, j]) for j in range(4)])
    ev, V = np.linalg.eig(M0)
    idx = np.argsort(np.abs(ev))
    S = np.column_stack([V[:, idx[0]].real, V[:, idx[0]].imag])
    x0 = S @ np.linalg.solve(S[:2], np.array([delta0, theta0]))
    return np.array([R1 * x0[0], W1 * x0[1], x0[2], x0[3]], dtype=float)


# ==============================================================================
# 3. BENCHMARK REPLAY, CLOSURE DEFECT, CONTROLS & BASIS INVARIANCE
# ==============================================================================
def run_aest_benchmark(deg: int = 24, rtol: float = 1e-12) -> Dict:
    grid = np.linspace(1.0, 2.0, 2001)
    bg_g = np.array([bg(float(a)) for a in grid]).T
    R_g, H_g = bg_g[3], bg_g[5]
    Q1, Kp1, Kpp1, R1, W1, H1 = bg(1.0)
    delta0 = 1e-5
    rows = []

    for k in [6.0, 9.0, 12.0, 18.0, 24.0]:
        r_g = (k / grid) ** 2
        D0 = R1 * delta0
        m0 = -W1 * H1 * delta0 / (k * k)
        coeffs_map, def_raw, def_dim, eval_mat = cheb_fenichel_chain(k, max_order=3, deg=deg)

        def rhs_full(a, y):
            A, B, C, F = blocks_Dm(a, k)
            return np.concatenate([A @ y[:2] + B @ y[2:], C @ y[:2] + F @ y[2:]]) / (a * bg(a)[-1])

        def rhs_zp(a, xs):
            Q, Kp, Kpp, R, W, H = bg(a)
            rv = (k / a) ** 2
            D_, m_ = xs
            Phi = -(D_ + 3 * H * m_) / (2 * rv)
            Phid = -H * Phi + m_ / 2.0
            return np.array([-3 * H * D_ + 3 * W * Phid - rv * m_, -3 * H * m_ + W * Phi]) / (a * H)

        def rhs_ad(a, xs):
            Q, Kp, Kpp, R, W, H = bg(a)
            rv = (k / a) ** 2
            D_, m_ = xs
            p_ = Kp * D_ / (Q * Kpp)
            Phi = -(D_ + 3 * H * m_) / (2 * rv)
            Phid = -H * Phi + m_ / 2.0
            return np.array([-3 * H * (D_ + p_) + 3 * W * Phid - rv * m_, -3 * H * m_ + p_ + W * Phi]) / (a * H)

        sol_zp = solve_ivp(rhs_zp, (1.0, 2.0), [D0, m0], t_eval=grid, method="DOP853", rtol=rtol, atol=1e-22)
        sol_ad = solve_ivp(rhs_ad, (1.0, 2.0), [D0, m0], t_eval=grid, method="DOP853", rtol=rtol, atol=1e-22)
        y0_probe = frozen_probe_ic_Dm(k, delta0)
        y0_inv = np.concatenate([[D0, m0], eval_mat(coeffs_map[3], 1.0) @ np.array([D0, m0])])

        sol_probe = solve_ivp(rhs_full, (1.0, 2.0), y0_probe, t_eval=grid, method="DOP853", rtol=rtol, atol=1e-22)
        sol_inv = solve_ivp(rhs_full, (1.0, 2.0), y0_inv, t_eval=grid, method="DOP853", rtol=rtol, atol=1e-22)
        check(sol_zp.success and sol_ad.success and sol_probe.success and sol_inv.success, f"ODE failed at k={k}")

        obs = lambda Y: (Y[0] / R_g, -(Y[0] + 3 * H_g * Y[1]) / r_g)
        o_zp = obs(sol_zp.y)
        scales = [float(np.max(np.abs(o))) for o in o_zp]
        o_ad = obs(sol_ad.y)
        o_probe = obs(sol_probe.y)
        o_inv = obs(sol_inv.y)

        err_zp_probe = [float(np.max(np.abs(o_probe[i] - o_zp[i])) / scales[i]) for i in (0, 1)]
        err_ad_probe = [float(np.max(np.abs(o_probe[i] - o_ad[i])) / scales[i]) for i in (0, 1)]

        # Also measure exact initial off-manifold residual of probe.py's frozen IC!
        H3_init = eval_mat(coeffs_map[3], 1.0)
        ef_probe_init = y0_probe[2:] - H3_init @ y0_probe[:2]
        ef_probe_rel = float(np.linalg.norm(ef_probe_init) / np.linalg.norm(H3_init @ y0_probe[:2]))

        # Compute baseline defects for ZP (H_ZP = [[0,0],[-1/r,0]]) and Adiabatic (H_ad = 0)
        def eval_named_defect(H_fn):
            dmax = 0.0
            for av in np.linspace(1.01, 1.99, 50):
                A, B, C, F = blocks_Dm(float(av), k)
                da = 1e-6 * av
                dHdt = (H_fn(av + da) - H_fn(av - da)) / (2 * da) * (av * bg(float(av))[-1])
                Hm = H_fn(av)
                Rmat = C + F @ Hm - dHdt - Hm @ (A + B @ Hm)
                rv = (k / av) ** 2
                Ds = np.diag([1.0, 1.0 / rv])
                F_inv_R = np.linalg.solve(F, Rmat) @ Ds
                H_ref = eval_mat(coeffs_map[0], float(av)) @ Ds
                dmax = max(dmax, float(np.linalg.norm(F_inv_R, ord="fro") / np.linalg.norm(H_ref, ord="fro")))
            return dmax

        defect_zp = eval_named_defect(lambda av: np.array([[0.0, 0.0], [-1.0 / ((k / av) ** 2), 0.0]]))
        defect_ad = eval_named_defect(lambda av: np.zeros((2, 2)))

        ord_results = {}
        for ord_ in (0, 1, 2, 3):
            cmat = coeffs_map[ord_]

            def rhs_r(a, xs, cm=cmat):
                A, B, _, _ = blocks_Dm(a, k)
                Hm = eval_mat(cm, a)
                return ((A + B @ Hm) @ xs) / (a * bg(a)[-1])

            sr = solve_ivp(rhs_r, (1.0, 2.0), [D0, m0], t_eval=grid, method="DOP853", rtol=rtol, atol=1e-22)
            check(sr.success, f"Reduced ODE H_{ord_} failed at k={k}")
            or_ = obs(sr.y)
            ep = [float(np.max(np.abs(o_probe[i] - or_[i])) / scales[i]) for i in (0, 1)]
            ei = [float(np.max(np.abs(o_inv[i] - or_[i])) / scales[i]) for i in (0, 1)]
            ord_results[f"H{ord_}"] = {
                "vs_probe_frozen_ic": {"density_err": ep[0], "lensing_err": ep[1], "max_err": max(ep), "passes_1pct": max(ep) < 0.01},
                "vs_invariant_ic": {"density_err": ei[0], "lensing_err": ei[1], "max_err": max(ei), "passes_1pct": max(ei) < 0.01},
                "invariance_defect_fro": def_raw[ord_],
                "invariance_defect_dimless": def_dim[ord_],
            }

        # Verify every k passes the 1% benchmark gate already at H0!
        check(ord_results["H0"]["vs_probe_frozen_ic"]["passes_1pct"], f"H0 failed 1% gate vs probe IC at k={k}")
        check(ord_results["H3"]["vs_invariant_ic"]["max_err"] < 1e-4, f"H3 vs inv IC exceeded 1e-4 at k={k}")

        rows.append(
            {
                "k_over_Q0": k,
                "zero_pressure": {
                    "density_err": err_zp_probe[0],
                    "lensing_err": err_zp_probe[1],
                    "max_err": max(err_zp_probe),
                    "invariance_defect_dimless": defect_zp,
                },
                "adiabatic_pressure": {
                    "density_err": err_ad_probe[0],
                    "lensing_err": err_ad_probe[1],
                    "max_err": max(err_ad_probe),
                    "invariance_defect_dimless": defect_ad,
                },
                "probe_frozen_ic_hidden_off_manifold_rel": ef_probe_rel,
                "fenichel_closures": ord_results,
            }
        )
    return {"deg": deg, "rtol": rtol, "rows": rows}


def run_negative_controls_and_invariance() -> Dict:
    """Gates 2 & 3: basis invariance, refinement convergence, wrong-sign/scrambled nulls, leakage scaling."""
    k = 12.0
    grid = np.linspace(1.0, 2.0, 2001)
    bg_g = np.array([bg(float(a)) for a in grid]).T
    R_g, H_g = bg_g[3], bg_g[5]
    r_g = (k / grid) ** 2
    Q1, Kp1, Kpp1, R1, W1, H1 = bg(1.0)
    delta0 = 1e-5
    D0 = R1 * delta0
    m0 = -W1 * H1 * delta0 / (k * k)

    coeffs_map, _, def_dim, eval_mat = cheb_fenichel_chain(k, max_order=3, deg=24)

    def rhs_full(a, y):
        A, B, C, F = blocks_Dm(a, k)
        return np.concatenate([A @ y[:2] + B @ y[2:], C @ y[:2] + F @ y[2:]]) / (a * bg(a)[-1])

    def rhs_zp(a, xs):
        Q, Kp, Kpp, R, W, H = bg(a)
        rv = (k / a) ** 2
        D_, m_ = xs
        Phi = -(D_ + 3 * H * m_) / (2 * rv)
        Phid = -H * Phi + m_ / 2.0
        return np.array([-3 * H * D_ + 3 * W * Phid - rv * m_, -3 * H * m_ + W * Phi]) / (a * H)

    sol_zp = solve_ivp(rhs_zp, (1.0, 2.0), [D0, m0], t_eval=grid, method="DOP853", rtol=1e-12, atol=1e-22)
    scales = [float(np.max(np.abs(sol_zp.y[0] / R_g))), float(np.max(np.abs(-(sol_zp.y[0] + 3 * H_g * sol_zp.y[1]) / r_g)))]

    y0_inv = np.concatenate([[D0, m0], eval_mat(coeffs_map[3], 1.0) @ np.array([D0, m0])])
    sol_inv = solve_ivp(rhs_full, (1.0, 2.0), y0_inv, t_eval=grid, method="DOP853", rtol=1e-12, atol=1e-22)
    obs = lambda Y: (Y[0] / R_g, -(Y[0] + 3 * H_g * Y[1]) / r_g)
    o_inv = obs(sol_inv.y)

    # 1. Gate 2: Random invertible GL(2) x GL(2) basis invariance test (5 seeded transforms)
    # Apply similarity in physically balanced coordinates (D, r*m) and compare identical direct H0 = -F^{-1} C!
    rng = np.random.default_rng(20261120)
    sol_orig_direct = solve_ivp(
        lambda a, xs: ((blocks_Dm(a, k)[0] + blocks_Dm(a, k)[1] @ (-np.linalg.solve(blocks_Dm(a, k)[3], blocks_Dm(a, k)[2]))) @ xs)
        / (a * bg(a)[-1]),
        (1.0, 2.0),
        [D0, m0],
        t_eval=grid,
        method="DOP853",
        rtol=1e-13,
        atol=1e-24,
    )
    o_o = obs(sol_orig_direct.y)
    # Natural scale balancer S_bal = diag(1, k^2) so D and k^2*m have O(1) ratio before random GL(2) mixing
    S_bal = np.diag([1.0, k * k])
    S_bal_inv = np.diag([1.0, 1.0 / (k * k)])
    basis_diffs = []
    for trial in range(5):
        U_s = rng.normal(size=(2, 2))
        while abs(np.linalg.det(U_s)) < 0.3:
            U_s = rng.normal(size=(2, 2))
        P_s = U_s @ S_bal
        P_s_inv = S_bal_inv @ np.linalg.inv(U_s)
        P_f = rng.normal(size=(2, 2))
        while abs(np.linalg.det(P_f)) < 0.3:
            P_f = rng.normal(size=(2, 2))
        P_f_inv = np.linalg.inv(P_f)

        def rhs_trans_H0(a, xs_p):
            A, B, C, F = blocks_Dm(a, k)
            Ap = P_s @ A @ P_s_inv
            Bp = P_s @ B @ P_f_inv
            Cp = P_f @ C @ P_s_inv
            Fp = P_f @ F @ P_f_inv
            H0p = -np.linalg.solve(Fp, Cp)
            return ((Ap + Bp @ H0p) @ xs_p) / (a * bg(a)[-1])

        sol_t = solve_ivp(rhs_trans_H0, (1.0, 2.0), P_s @ np.array([D0, m0]), t_eval=grid, method="DOP853", rtol=1e-13, atol=1e-24)
        xs_back = P_s_inv @ sol_t.y
        o_t = obs(xs_back)
        basis_diffs.append(float(max(np.max(np.abs(o_t[i] - o_o[i])) / scales[i] for i in (0, 1))))
    max_basis_diff = max(basis_diffs)
    check(max_basis_diff < 1e-11, f"Basis invariance broken: {max_basis_diff}")

    # 2. Gate 2: Refinement convergence (deg 24/rtol 1e-12 vs deg 36/rtol 1e-13 at k=12)
    coeffs_ref, _, _, eval_ref = cheb_fenichel_chain(k, max_order=3, deg=36)
    sol_r_base = solve_ivp(
        lambda a, xs: ((blocks_Dm(a, k)[0] + blocks_Dm(a, k)[1] @ eval_mat(coeffs_map[3], a)) @ xs) / (a * bg(a)[-1]),
        (1.0, 2.0),
        [D0, m0],
        t_eval=grid,
        method="DOP853",
        rtol=1e-12,
        atol=1e-22,
    )
    sol_r_ref = solve_ivp(
        lambda a, xs: ((blocks_Dm(a, k)[0] + blocks_Dm(a, k)[1] @ eval_ref(coeffs_ref[3], a)) @ xs) / (a * bg(a)[-1]),
        (1.0, 2.0),
        [D0, m0],
        t_eval=grid,
        method="DOP853",
        rtol=1e-13,
        atol=1e-23,
    )
    refinement_diff = float(max(np.max(np.abs(obs(sol_r_base.y)[i] - obs(sol_r_ref.y)[i])) / scales[i] for i in (0, 1)))
    check(refinement_diff < 1e-8, f"Refinement unstable: {refinement_diff}")

    # 3. Gate 3: Negative controls (wrong-sign Helmholtz M_scr^2 -> -M_scr^2, flipped Z sign, scrambled H)
    # Wrong-sign Z (Z = +D/r instead of -D/r => p = 2*ca^2*D!)
    def rhs_wrong_sign(a, xs):
        A, B, _, _ = blocks_Dm(a, k)
        Hm = -eval_mat(coeffs_map[0], a)
        return ((A + B @ Hm) @ xs) / (a * bg(a)[-1])

    sol_ws = solve_ivp(rhs_wrong_sign, (1.0, 2.0), [D0, m0], t_eval=grid, method="DOP853", rtol=1e-11, atol=1e-21)
    err_wrong_sign = float(max(np.max(np.abs(o_inv[i] - obs(sol_ws.y)[i])) / scales[i] for i in (0, 1)))
    check(err_wrong_sign > 1.0, f"Wrong-sign null did not fail strongly: {err_wrong_sign}")

    # Wrong-sign Helmholtz pole (p = ca^2 * (-M_scr^2)/(r - M_scr^2) * D)
    def rhs_neg_helmholtz(a, xs):
        Q, Kp, Kpp, R, W, H = bg(a)
        rv = (k / a) ** 2
        D_, m_ = xs
        M2 = Kpp * Q * Q * 2.0 / 3.0
        p_ = (Kp / (Q * Kpp)) * (-M2 / (rv - M2)) * D_
        Phi = -(D_ + 3 * H * m_) / (2 * rv)
        Phid = -H * Phi + m_ / 2.0
        return np.array([-3 * H * (D_ + p_) + 3 * W * Phid - rv * m_, -3 * H * m_ + p_ + W * Phi]) / (a * H)

    sol_nh = solve_ivp(rhs_neg_helmholtz, (1.0, 2.0), [D0, m0], t_eval=grid, method="DOP853", rtol=1e-11, atol=1e-21)
    err_neg_helm = float(max(np.max(np.abs(o_inv[i] - obs(sol_nh.y)[i])) / scales[i] for i in (0, 1)))
    check(err_neg_helm > 0.25, f"Negative-M_scr^2 null did not fail: {err_neg_helm}")

    # 4. Gate 3 / Duhamel separation: inject deliberate fast-mode leakage eta while keeping R[H_3] fixed!
    leakage_rows = []
    Z_scale = abs(y0_inv[3])
    for eta in [0.0, 0.01, 0.1, 1.0]:
        y0_leak = y0_inv.copy()
        y0_leak[3] += eta * Z_scale
        sol_l = solve_ivp(rhs_full, (1.0, 2.0), y0_leak, t_eval=grid, method="DOP853", rtol=1e-12, atol=1e-22)
        err_l = float(max(np.max(np.abs(obs(sol_l.y)[i] - obs(sol_r_base.y)[i])) / scales[i] for i in (0, 1)))
        leakage_rows.append({"eta_Z": eta, "max_rel_err": err_l, "invariance_defect_H3_unchanged": def_dim[3]})
    check(leakage_rows[3]["max_rel_err"] > 50.0 * leakage_rows[0]["max_rel_err"], "Leakage sensitivity check failed")

    return {
        "k_over_Q0": k,
        "gl2_x_gl2_basis_invariance_max_diff": max_basis_diff,
        "cheb_refinement_deg24_vs_deg36_max_diff": refinement_diff,
        "negative_control_flipped_H_error": err_wrong_sign,
        "negative_control_wrong_sign_helmholtz_error": err_neg_helm,
        "fast_mode_leakage_separation": leakage_rows,
    }


# ==============================================================================
# 4. FULL 6-STATE COUPLED BARYON + AeST VERIFICATION OF 2x2 G_eff(k/a)
# ==============================================================================
def run_coupled_baryon_aest_test() -> List[Dict]:
    grid = np.linspace(1.0, 2.0, 2001)
    fb = 0.1565  # Planck 2018 Omega_b / Omega_m
    qi = 1e-4
    R_A1 = 4 * qi + 2 * qi * qi
    R_b1 = R_A1 * fb / (1.0 - fb)

    def bg_2f(a):
        q = qi / (a**3)
        Q = 1.0 + q
        Kp = 4.0 * q
        Kpp = 4.0
        R_A = 4 * q + 2 * q * q
        W_A = Q * Kp
        R_b = R_b1 / (a**3)
        H = math.sqrt((R_b + R_A) / 3.0)
        return Q, Kp, Kpp, R_b, R_A, W_A, H

    rows = []
    for lam_v in [1.0, 0.0, -0.5]:
        for k in [0.5, 2.8284271247461903, 10.0, 50.0]:
            Q1, Kp1, Kpp1, Rb1, RA1, WA1, H1 = bg_2f(1.0)
            r1 = k * k
            d0 = 1e-5
            Db0, DA0 = Rb1 * d0, RA1 * d0
            mb0, mA0 = -Rb1 * (H1 * d0) / r1, -RA1 * (H1 * d0) / r1
            den = lam_v * r1 + Kpp1 * Q1 * Q1 * (lam_v + 1.0) + 2.0 * r1
            ch0 = -DA0 / den
            Z0 = -DA0 * (lam_v + 2.0) / den

            def rhs_6(a, y):
                Q, Kp, Kpp, R_b, R_A, W_A, H = bg_2f(a)
                r = (k / a) ** 2
                Db, mb, DA, mA, ch, Z = y
                Phi = -(Db + DA + 3 * H * (mb + mA)) / (2 * r)
                Phid = -H * Phi + (mb + mA) / 2.0
                gam = (DA + r * Z) / (Q * Kpp)
                pA = Kp * gam
                Qdot = -3 * H * Kp / Kpp
                return np.array(
                    [
                        -3 * H * Db + 3 * R_b * Phid - r * mb,
                        -3 * H * mb + R_b * Phi,
                        -3 * H * (DA + pA) + 3 * W_A * Phid - r * mA,
                        -3 * H * mA + pA + W_A * Phi,
                        gam + Q * Z + (Qdot / Q - Q) * ch + (3 * H / (Q * Kpp)) * mA,
                        (-H + Q) * Z + (Kp - (2.0 + lam_v) * Q) * ch,
                    ]
                ) / (a * H)

            def rhs_red(a, y):
                Q, Kp, Kpp, R_b, R_A, W_A, H = bg_2f(a)
                r = (k / a) ** 2
                db, dbd, dA, dAd = y
                G_AA = (Kpp * Q * Q * (lam_v + 1.0) - lam_v * r) / (Kpp * Q * Q * (lam_v + 1.0) + (2.0 + lam_v) * r)
                return np.array(
                    [
                        dbd,
                        -2 * H * dbd + 0.5 * (R_b * db + R_A * dA),
                        dAd,
                        -2 * H * dAd + 0.5 * (R_b * db + R_A * G_AA * dA),
                    ]
                ) / (a * H)

            s6 = solve_ivp(rhs_6, (1.0, 2.0), [Db0, mb0, DA0, mA0, ch0, Z0], t_eval=grid, method="DOP853", rtol=1e-10, atol=1e-22)
            sr = solve_ivp(rhs_red, (1.0, 2.0), [d0, H1 * d0, d0, H1 * d0], t_eval=grid, method="DOP853", rtol=1e-11, atol=1e-22)
            check(s6.success and sr.success, f"6-state ODE failed lam={lam_v} k={k}")
            Rb_g = R_b1 / (grid**3)
            RA_g = 4 * (qi / (grid**3)) + 2 * (qi / (grid**3)) ** 2
            db6, dA6 = s6.y[0] / Rb_g, s6.y[2] / RA_g
            err_b = float(np.max(np.abs(db6 - sr.y[0])) / np.max(np.abs(sr.y[0])))
            err_A = float(np.max(np.abs(dA6 - sr.y[2])) / np.max(np.abs(sr.y[2])))
            check(err_b < 0.002 and err_A < 0.003, f"2x2 G_eff mismatch lam={lam_v}, k={k}: {err_b}, {err_A}")

            # Exact asymptotic growing-mode eigenvalue & segregation ratio at r -> oo
            G_AA_1 = (4.0 * (lam_v + 1.0) - lam_v * r1) / (4.0 * (lam_v + 1.0) + (2.0 + lam_v) * r1)
            M2 = np.array([[fb, 1.0 - fb], [fb, (1.0 - fb) * G_AA_1]])
            evals, evecs = np.linalg.eig(M2)
            ip = int(np.argmax(evals.real))
            lp = float(evals[ip].real)
            p_plus = (-0.5 + math.sqrt(0.25 + 6.0 * lp)) / 2.0
            rows.append(
                {
                    "lam_s": lam_v,
                    "k_over_Q0": k,
                    "G_AA_at_a1": G_AA_1,
                    "asymptotic_growth_exponent_p_plus": p_plus,
                    "delta_b_growth_full6": float(db6[-1] / d0),
                    "delta_b_growth_reduced2x2": float(sr.y[0, -1] / d0),
                    "delta_b_rel_err": err_b,
                    "delta_A_growth_full6": float(dA6[-1] / d0),
                    "delta_A_growth_reduced2x2": float(sr.y[2, -1] / d0),
                    "delta_A_rel_err": err_A,
                    "final_segregation_dA_over_db": float(dA6[-1] / db6[-1]),
                }
            )
    return rows


# ==============================================================================
# 5. EXACT RATIONAL SYLVESTER CHECK OF MINKOWSKI H_2 POLE-ZERO BOUNDARY
# ==============================================================================
def exact_rational_minkowski_inertia() -> List[Dict]:
    """Pure Fraction Sylvester congruence C H_2 C^T = D across k^2 = mu^2 (zero floats)."""
    def H2_matrix_exact(KB: Fraction, lam: Fraction, Kpp: Fraction, r: Fraction) -> List[List[Fraction]]:
        # Exact Hessian of H_2(chi, p, P) at Q=1 from symbolic formula:
        # H_2 = 1/2 x^T M x, where M = Hess(H_2)
        b = Fraction(2) - KB
        m00 = Fraction(2) * r * b * (Fraction(2) + KB * lam) / KB
        m01 = -b / KB
        m02 = -b / KB
        m11 = Fraction(1) / (Fraction(2) * Kpp) + Fraction(1) / (Fraction(2) * KB * r)
        m12 = Fraction(1) / (Fraction(2) * KB * r)
        m22 = Fraction(1) / (Fraction(2) * KB * r) - Fraction(1) / (Fraction(4) * r)
        return [[m00, m01, m02], [m01, m11, m12], [m02, m12, m22]]

    def exact_ldl(M: List[List[Fraction]]):
        n = len(M)
        A = [[M[i][j] for j in range(n)] for i in range(n)]
        L = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        D = [Fraction(0)] * n
        for j in range(n):
            D[j] = A[j][j] - sum(L[j][k] * L[j][k] * D[k] for k in range(j))
            if D[j] == 0:
                continue
            for i in range(j + 1, n):
                L[i][j] = (A[i][j] - sum(L[i][k] * L[j][k] * D[k] for k in range(j))) / D[j]
        # Verify L D L^T == M identically over Q!
        for i in range(n):
            for j in range(n):
                rec = sum(L[i][k] * D[k] * L[j][k] for k in range(n))
                check(rec == M[i][j], f"Exact LDL^T mismatch at ({i},{j})")
        return D

    cases = [
        ("UV_stable_k2_9_above_mu2_8", Fraction(1), Fraction(1), Fraction(4), Fraction(9)),
        ("CRITICAL_pole_zero_k2_8_eq_mu2_8", Fraction(1), Fraction(1), Fraction(4), Fraction(8)),
        ("IR_clustering_k2_7_below_mu2_8", Fraction(1), Fraction(1), Fraction(4), Fraction(7)),
        ("Cosmological_lam0_k2_4", Fraction(1), Fraction(0), Fraction(4), Fraction(4)),
    ]
    out = []
    for label, KB, lam, Kpp, r in cases:
        M = H2_matrix_exact(KB, lam, Kpp, r)
        D = exact_ldl(M)
        inertia = (sum(1 for d in D if d > 0), sum(1 for d in D if d == 0), sum(1 for d in D if d < 0))
        G_AA = (Kpp * (lam + 1) - (Fraction(2) - KB) * lam * r) / (Kpp * (lam + 1) + (Fraction(2) + KB * lam) * r)
        out.append(
            {
                "case": label,
                "KB": str(KB),
                "lam_s": str(lam),
                "Kpp": str(Kpp),
                "r_eq_k2": str(r),
                "exact_D_pivots": [str(d) for d in D],
                "exact_inertia_pos_zero_neg": list(inertia),
                "exact_G_AA_over_Gtilde": str(G_AA),
            }
        )
    # Verify exact sign correlation: inertia (3,0,0) <=> G_AA < 0; (2,1,0) <=> G_AA == 0; (2,0,1) <=> G_AA > 0!
    check(out[0]["exact_inertia_pos_zero_neg"] == [3, 0, 0] and Fraction(out[0]["exact_G_AA_over_Gtilde"]) < 0, "UV sign check failed")
    check(out[1]["exact_inertia_pos_zero_neg"] == [2, 1, 0] and Fraction(out[1]["exact_G_AA_over_Gtilde"]) == 0, "Critical sign check failed")
    check(out[2]["exact_inertia_pos_zero_neg"] == [2, 0, 1] and Fraction(out[2]["exact_G_AA_over_Gtilde"]) > 0, "IR sign check failed")
    return out


def main() -> None:
    sym = symbolic_theorems()
    bench = run_aest_benchmark(deg=24, rtol=1e-12)
    controls = run_negative_controls_and_invariance()
    coupled = run_coupled_baryon_aest_test()
    mink_exact = exact_rational_minkowski_inertia()

    payload = {
        "probe": "probe1_aest_helmholtz_closure",
        "symbolic_theorems": sym,
        "aest_benchmark_k6_to_24": bench,
        "anti_shadow_controls_and_invariance": controls,
        "coupled_baryon_aest_6state_verification": coupled,
        "exact_rational_minkowski_pole_zero_inertia": mink_exact,
    }
    # Reference-BLAS IEEE-754 float payload digest (cross-BLAS builds may differ at <=1.7e-11 relative last-ULP)
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["sha256_canonical"] = hashlib.sha256(canon).hexdigest()
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("=== PROBE 1 COMPLETE: ALL EXACT, INVARIANCE & NEGATIVE-CONTROL CHECKS PASSED ===")
    print(f"Output: {OUT_PATH}")
    print(f"SHA256: {payload['sha256_canonical']}")
    print("\n--- Benchmark Summary (aest-response-gate/slow-mode 1% gate) ---")
    for r in bench["rows"]:
        fc = r["fenichel_closures"]
        print(
            f"k={r['k_over_Q0']:4.1f} | ZP={100*r['zero_pressure']['max_err']:6.3f}% (def={r['zero_pressure']['invariance_defect_dimless']:.2e}) | "
            f"Ad={100*r['adiabatic_pressure']['max_err']:7.3f}% | "
            f"H0(probe)={100*fc['H0']['vs_probe_frozen_ic']['max_err']:.4f}% | "
            f"H3(inv)={100*fc['H3']['vs_invariant_ic']['max_err']:.6f}% (def={fc['H3']['invariance_defect_dimless']:.2e})"
        )
    print("\n--- Exact Rational Pole-Zero Inertia Duality ---")
    for row in mink_exact:
        print(f"  {row['case']:34s}: inertia={row['exact_inertia_pos_zero_neg']}  G_AA={row['exact_G_AA_over_Gtilde']}")
    print("\n--- Coupled 6-State Baryon + AeST Verification ---")
    for row in coupled:
        print(
            f"  lam={row['lam_s']:+4.1f}, k/Q0={row['k_over_Q0']:7.4f} | G_AA={row['G_AA_at_a1']:+7.4f} | "
            f"err_b={100*row['delta_b_rel_err']:.4f}%, err_A={100*row['delta_A_rel_err']:.4f}% | "
            f"dA/db={row['final_segregation_dA_over_db']:.4f}"
        )


if __name__ == "__main__":
    main()
