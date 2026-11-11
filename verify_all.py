#!/usr/bin/env python3
"""
Foundation-0 / gravity — Reproducible Verification & Falsification Suite
========================================================================
Zero-dependency Python 3 standard-library verifier (`math`, `json`, `hashlib`)
for cross-scale quantum-condensate and fractal-abstraction models unifying
gravity and dark matter.

Usage:
    python3 verify_all.py            # Generates results/certificates.json & runs self-tests
    python3 verify_all.py --check    # Verifies invariants and exits 0 on pass

Code License: Apache-2.0 | Documentation/Results License: CC-BY-4.0
Attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0);
             not yet reviewed by a person.
"""

from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path

G = 6.67430e-11
HBAR = 1.054571817e-34
C = 299792458.0
EV_J = 1.602176634e-19
EV_KG = EV_J / (C ** 2)
M_SUN = 1.98847e30
PC = 3.085677581491367e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
AU = 1.495978707e11
A0 = 1.20e-10
ZETA_3_2 = 2.6123753486854883
H0_SI = (67.4 * 1.0e3) / MPC
OMEGA_LAMBDA = 0.6847


def linear_fit_slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def check_1_coordinate_vs_gradient_dichotomy() -> dict:
    log_masses = [7.0 + 0.1 * i for i in range(51)]
    masses_msun = [10.0 ** lm for lm in log_masses]
    masses_kg = [m * M_SUN for m in masses_msun]
    r_b_m = [1.8 * KPC * ((m / 1.0e10) ** 0.28) for m in masses_msun]

    r_eval = 100.0 * KPC
    l_star = 3.0 * KPC
    v_coord_log = []
    for m_kg, rb in zip(masses_kg, r_b_m):
        gb = G * m_kg / ((r_eval + rb) ** 2)
        gc = gb * (1.0 + r_eval / l_star)
        v_coord_log.append(math.log10(math.sqrt(r_eval * gc) / 1.0e3))
    beta_coord = linear_fit_slope(v_coord_log, log_masses)

    sweep = []
    for ds_tenth in range(0, 35, 5):
        ds = ds_tenth / 10.0
        q = 1.0 + 0.5 * ds
        p_lap = 2.0 + ds
        r1, r2 = 100.0 * KPC, 300.0 * KPC
        v1_logs = []
        alpha_lstar = 0.0
        for idx, (m_kg, rb) in enumerate(zip(masses_kg, r_b_m)):
            gb1 = G * m_kg / ((r1 + rb) ** 2)
            gb2 = G * m_kg / ((r2 + rb) ** 2)
            if ds == 0.0:
                g1, g2 = gb1, gb2
            else:
                exp_pow = ds / (1.0 + ds)
                g1 = gb1 * (1.0 + (A0 / gb1) ** exp_pow)
                g2 = gb2 * (1.0 + (A0 / gb2) ** exp_pow)
            v1 = math.sqrt(r1 * g1)
            v2 = math.sqrt(r2 * g2)
            v1_logs.append(math.log10(v1 / 1.0e3))
            if idx == 38:
                alpha_lstar = math.log(v2 / v1) / math.log(r2 / r1)
        sweep.append({
            "spectral_dim_ds": round(ds, 2),
            "lagrangian_exp_q": round(q, 2),
            "p_laplacian_exp": round(p_lap, 2),
            "outer_dlnv_dlnr_100_300kpc": round(alpha_lstar, 5),
            "btfr_slope_beta": round(linear_fit_slope(v1_logs, log_masses), 4),
        })

    sq_err_sf = 0.0
    n_grid = 200
    for i in range(n_grid):
        gb = 10.0 ** (-13.0 + 5.0 * i / (n_grid - 1))
        g_rar = gb / (1.0 - math.exp(-math.sqrt(gb / A0)))
        y = gb / A0
        g_sf = gb * (0.5 + math.sqrt(0.25 + 1.0 / y))
        sq_err_sf += (math.log10(g_sf) - math.log10(g_rar)) ** 2
    rar_rms_sf = math.sqrt(sq_err_sf / n_grid)

    sq_err_coord = 0.0
    cnt = 0
    for m_kg, rb in zip(masses_kg, r_b_m):
        for j in range(20):
            r_m = (10.0 ** (2.0 * j / 19.0)) * KPC
            gb = G * m_kg / ((r_m + rb) ** 2)
            g_rar = gb / (1.0 - math.exp(-math.sqrt(gb / A0)))
            g_c = gb * (1.0 + r_m / l_star)
            sq_err_coord += (math.log10(g_c) - math.log10(g_rar)) ** 2
            cnt += 1
    rar_rms_coord = math.sqrt(sq_err_coord / cnt)

    return {
        "coord_fractal_Df2_btfr_slope": round(beta_coord, 4),
        "coord_fractal_rar_rms_dex": round(rar_rms_coord, 4),
        "ds1_condensate_rar_rms_dex": round(rar_rms_sf, 4),
        "spectral_dimension_sweep": sweep,
    }


def check_2_schrodinger_poisson_soliton() -> dict:
    xi_min = 1.0e-4
    h = 0.0025

    def integrate(eps: float, xi_max: float = 13.0):
        xi = xi_min
        psi = 1.0 - (eps / 3.0) * (xi * xi)
        dpsi = -(2.0 * eps / 3.0) * xi
        phi = (1.0 / 6.0) * (xi * xi)
        dphi = (1.0 / 3.0) * xi

        def deriv(x: float, p: float, dp: float, ph: float, dph: float):
            return (
                dp,
                -2.0 * dp / x + 2.0 * (ph - eps) * p,
                dph,
                -2.0 * dph / x + p * p,
            )

        traj = [(xi, psi, dpsi, phi, dphi)]
        crossed_zero = False
        steps = int((xi_max - xi_min) / h)
        for _ in range(steps):
            k1 = deriv(xi, psi, dpsi, phi, dphi)
            x2 = xi + 0.5 * h
            k2 = deriv(x2, psi + 0.5 * h * k1[0], dpsi + 0.5 * h * k1[1], phi + 0.5 * h * k1[2], dphi + 0.5 * h * k1[3])
            k3 = deriv(x2, psi + 0.5 * h * k2[0], dpsi + 0.5 * h * k2[1], phi + 0.5 * h * k2[2], dphi + 0.5 * h * k2[3])
            x4 = xi + h
            k4 = deriv(x4, psi + h * k3[0], dpsi + h * k3[1], phi + h * k3[2], dphi + h * k3[3])

            psi = psi + (h / 6.0) * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0])
            dpsi = dpsi + (h / 6.0) * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1])
            phi = phi + (h / 6.0) * (k1[2] + 2.0 * k2[2] + 2.0 * k3[2] + k4[2])
            dphi = dphi + (h / 6.0) * (k1[3] + 2.0 * k2[3] + 2.0 * k3[3] + k4[3])
            xi = x4
            if psi <= 0.0:
                crossed_zero = True
                break
            if psi > 1.2 or dpsi > 0.0:
                break
            traj.append((xi, psi, dpsi, phi, dphi))
        return crossed_zero, traj

    lo, hi = 0.60, 0.75
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        crossed, _ = integrate(mid, xi_max=13.5)
        if crossed:
            hi = mid
        else:
            lo = mid
    eps0 = 0.5 * (lo + hi)
    _, traj = integrate(eps0, xi_max=11.0)

    enc = [0.0]
    for i in range(1, len(traj)):
        x0, p0 = traj[i - 1][0], traj[i - 1][1]
        x1, p1 = traj[i][0], traj[i][1]
        enc.append(enc[-1] + 0.5 * (x1 - x0) * (x0 * x0 * p0 * p0 + x1 * x1 * p1 * p1))
    m_dimless = enc[-1]

    xi_core = 0.0
    for i in range(1, len(traj)):
        r0, r1 = traj[i - 1][1] ** 2, traj[i][1] ** 2
        if r0 >= 0.5 >= r1:
            xi_core = traj[i - 1][0] + (0.5 - r0) / (r1 - r0) * (traj[i][0] - traj[i - 1][0])
            break

    half_target = 0.5 * m_dimless
    xi_half = 0.0
    for i in range(1, len(enc)):
        if enc[i - 1] <= half_target <= enc[i]:
            xi_half = traj[i - 1][0] + (half_target - enc[i - 1]) / (enc[i] - enc[i - 1]) * (traj[i][0] - traj[i - 1][0])
            break

    v2 = [enc[i] / traj[i][0] for i in range(len(traj))]
    idx_peak = max(range(len(v2)), key=lambda idx: v2[idx])
    xi_peak = traj[idx_peak][0]
    i1 = next(i for i, row in enumerate(traj) if row[0] >= 2.5 * xi_peak)
    i2 = len(traj) - 20
    outer_slope = math.log(math.sqrt(v2[i2] / v2[i1])) / math.log(traj[i2][0] / traj[i1][0])

    return {
        "eigenvalue_eps0": round(eps0, 8),
        "dimensionless_mass_int_xi2_psi2": round(m_dimless, 6),
        "xi_core_half_density": round(xi_core, 6),
        "xi_half_mass": round(xi_half, 6),
        "invariant_M_Rhalf_hbar2_Gm2": round(m_dimless * xi_half, 5),
        "invariant_M_Rcore_hbar2_Gm2": round(m_dimless * xi_core, 5),
        "outer_soliton_dlnv_dlnr": round(outer_slope, 4),
    }


def check_3_phase_space_inversion_and_hybrid_tower() -> dict:
    def crit_mass_ev(rho_kg_m3: float, sigma_ms: float) -> float:
        m_kg = (rho_kg_m3 * ((2.0 * math.pi) ** 1.5) * (HBAR ** 3) / (ZETA_3_2 * (sigma_ms ** 3))) ** 0.25
        return m_kg / EV_KG

    m_b_lstar = 6.0e10 * M_SUN
    v_flat = (G * m_b_lstar * A0) ** 0.25
    sig_gal = v_flat / math.sqrt(2.0)

    rho_iso_1mpc = (v_flat ** 2) / (4.0 * math.pi * G * (MPC ** 2))
    rho_nfw_1mpc = 0.08 * rho_iso_1mpc
    sig_bullet = 1.0e6
    rho_bullet_250kpc = (2.0 * (sig_bullet ** 2)) / (4.0 * math.pi * G * ((250.0 * KPC) ** 2))

    m_max_iso_1mpc = crit_mass_ev(rho_iso_1mpc, sig_gal)
    m_max_nfw_1mpc = crit_mass_ev(rho_nfw_1mpc, sig_gal)
    m_min_bullet = crit_mass_ev(rho_bullet_250kpc, sig_bullet)

    def degeneracy(f_frac: float, rho: float, m_ev: float, sig: float) -> float:
        m_kg = m_ev * EV_KG
        lam = math.sqrt(2.0 * math.pi) * HBAR / (m_kg * sig)
        return ((f_frac * rho) / m_kg) * (lam ** 3)

    n_light_1mpc = degeneracy(0.02, rho_nfw_1mpc, 0.05, sig_gal)
    n_heavy_bullet = degeneracy(0.98, rho_bullet_250kpc, 3.00, sig_bullet)

    c0 = 0.091
    n_u = 3000
    du = 15.0 / n_u
    enc_prof = [0.0]
    for i in range(1, n_u + 1):
        u0, u1 = (i - 1) * du, i * du
        f0 = 4.0 * math.pi * u0 * u0 * ((1.0 + c0 * u0 * u0) ** (-8))
        f1 = 4.0 * math.pi * u1 * u1 * ((1.0 + c0 * u1 * u1) ** (-8))
        enc_prof.append(enc_prof[-1] + 0.5 * du * (f0 + f1))
    norm_total = enc_prof[-1]
    enc_prof = [val / norm_total for val in enc_prof]

    def enc_frac(u_val: float) -> float:
        if u_val >= 15.0:
            return 1.0
        idx = int(u_val / du)
        rem = (u_val - idx * du) / du
        return enc_prof[idx] * (1.0 - rem) + enc_prof[min(idx + 1, n_u)] * rem

    tower_ripples = []
    for b in [1.5, 2.0, 3.0, 4.0, 6.0, 7.0, 10.0]:
        k_max = int(math.ceil(math.log(4000.0 / 0.25) / math.log(b))) + 2
        r_shells = [0.25 * (b ** k) for k in range(-4, k_max + 1)]
        v_vals = []
        for j in range(200):
            r_kpc = 10.0 * ((200.0 / 10.0) ** (j / 199.0))
            m_sum = sum(rk * enc_frac(r_kpc / rk) for rk in r_shells)
            v_vals.append(math.sqrt(m_sum / r_kpc))
        v_mean = sum(v_vals) / len(v_vals)
        ripple_pct = (max(v_vals) - min(v_vals)) / (2.0 * v_mean) * 100.0
        tower_ripples.append({
            "scale_ratio_b": b,
            "ripple_half_amp_pct": round(ripple_pct, 3),
            "passes_5pct_smoothness": ripple_pct <= 5.0,
        })

    return {
        "single_boson_bounds_eV": {
            "m_max_1Mpc_isothermal_eV": round(m_max_iso_1mpc, 4),
            "m_max_1Mpc_NFW_tail_eV": round(m_max_nfw_1mpc, 4),
            "m_min_Bullet_Cluster_melt_eV": round(m_min_bullet, 4),
            "single_boson_window_empty": bool(m_max_iso_1mpc < m_min_bullet),
        },
        "two_tier_hybrid_solution": {
            "m_light_eV": 0.05,
            "f_light": 0.02,
            "m_heavy_eV": 3.00,
            "f_heavy": 0.98,
            "light_Ndeg_at_1Mpc_NFW": round(n_light_1mpc, 2),
            "heavy_Ndeg_in_Bullet_core": round(n_heavy_bullet, 4),
            "bullet_internal_g_over_a0": round((2.0 * (sig_bullet ** 2) / (250.0 * KPC)) / A0, 3),
        },
        "fractal_soliton_tower_ripples": tower_ripples,
    }


def check_4_external_field_and_wide_binaries() -> dict:
    r_m_sun_au = math.sqrt(G * M_SUN / A0) / AU
    r_m_lstar_kpc = math.sqrt(G * (6.0e10 * M_SUN) / A0) / KPC
    e_mw = ((233.0e3) ** 2 / (8.1 * KPC)) / A0

    def asymp_efe_boost(e_val: float, family: str) -> float:
        if family == "simple":
            mu_e = e_val / (1.0 + e_val)
            l_e = 1.0 / (1.0 + e_val)
        else:
            mu_e = e_val / math.sqrt(1.0 + e_val * e_val)
            l_e = 1.0 / (1.0 + e_val * e_val)
        n_steps = 1000
        dth = math.pi / n_steps
        acc = 0.0
        for i in range(n_steps):
            th = (i + 0.5) * dth
            s = math.sin(th)
            acc += s / (mu_e * math.sqrt(1.0 + l_e * s * s)) * dth
        return 0.5 * acc

    boost_simple = asymp_efe_boost(e_mw, "simple")
    boost_std = asymp_efe_boost(e_mw, "standard")

    return {
        "solar_rM_AU": round(r_m_sun_au, 1),
        "lstar_rM_kpc": round(r_m_lstar_kpc, 3),
        "cosmic_efe_rollover_kpc_at_e0010": round(r_m_lstar_kpc / 0.010, 1),
        "milky_way_e_at_sun": round(e_mw, 4),
        "wide_binary_asymptotic_gravity_boost_simple_mu": round(boost_simple, 5),
        "wide_binary_velocity_boost_pct_simple_mu": round((math.sqrt(boost_simple) - 1.0) * 100.0, 2),
        "wide_binary_asymptotic_gravity_boost_standard_mu": round(boost_std, 5),
        "wide_binary_velocity_boost_pct_standard_mu": round((math.sqrt(boost_std) - 1.0) * 100.0, 2),
        "cosmological_coincidence": {
            "a0_empirical_m_s2": A0,
            "c_H0_over_2pi_m_s2": round(C * H0_SI / (2.0 * math.pi), 13),
            "c_H0_sqrt_OmegaL_over_2pi_m_s2": round(C * H0_SI * math.sqrt(OMEGA_LAMBDA) / (2.0 * math.pi), 13),
            "verlinde_c_H0_over_6_m_s2": round(C * H0_SI / 6.0, 13),
        },
    }


def run_assertions(cert: dict) -> None:
    c1 = cert["check_1_dichotomy"]
    assert 1.98 < c1["coord_fractal_Df2_btfr_slope"] < 2.06
    assert c1["coord_fractal_rar_rms_dex"] > 0.55
    ds1 = [r for r in c1["spectral_dimension_sweep"] if r["spectral_dim_ds"] == 1.0][0]
    assert abs(ds1["outer_dlnv_dlnr_100_300kpc"]) < 0.02
    assert 3.85 < ds1["btfr_slope_beta"] < 4.02
    assert c1["ds1_condensate_rar_rms_dex"] < 0.015

    c2 = cert["check_2_gravitational_atom"]
    assert abs(c2["invariant_M_Rhalf_hbar2_Gm2"] - 3.925) < 0.02
    assert abs(c2["outer_soliton_dlnv_dlnr"] + 0.5) < 0.015

    c3 = cert["check_3_phase_space_and_tower"]
    sb = c3["single_boson_bounds_eV"]
    assert sb["single_boson_window_empty"] is True
    assert sb["m_max_1Mpc_NFW_tail_eV"] < sb["m_max_1Mpc_isothermal_eV"] < sb["m_min_Bullet_Cluster_melt_eV"]
    hyb = c3["two_tier_hybrid_solution"]
    assert hyb["light_Ndeg_at_1Mpc_NFW"] > ZETA_3_2 and hyb["heavy_Ndeg_in_Bullet_core"] < ZETA_3_2
    r_b6 = [r for r in c3["fractal_soliton_tower_ripples"] if r["scale_ratio_b"] == 6.0][0]
    r_b7 = [r for r in c3["fractal_soliton_tower_ripples"] if r["scale_ratio_b"] == 7.0][0]
    assert r_b6["passes_5pct_smoothness"] is True and r_b7["passes_5pct_smoothness"] is False

    c4 = cert["check_4_efe_and_wide_binaries"]
    assert 800.0 < c4["cosmic_efe_rollover_kpc_at_e0010"] < 880.0
    assert c4["wide_binary_velocity_boost_pct_standard_mu"] < c4["wide_binary_velocity_boost_pct_simple_mu"]


def main() -> int:
    cert = {
        "schema": "FOUNDATION-0/GRAVITY-CERTIFICATES/1.0",
        "check_1_dichotomy": check_1_coordinate_vs_gradient_dichotomy(),
        "check_2_gravitational_atom": check_2_schrodinger_poisson_soliton(),
        "check_3_phase_space_and_tower": check_3_phase_space_inversion_and_hybrid_tower(),
        "check_4_efe_and_wide_binaries": check_4_external_field_and_wide_binaries(),
    }
    run_assertions(cert)
    canonical_bytes = json.dumps(cert, sort_keys=True, separators=(",", ":")).encode("utf-8")
    cert["sha256_canonical"] = hashlib.sha256(canonical_bytes).hexdigest()

    out_path = Path(__file__).resolve().parent / "results" / "certificates.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")

    print("ALL 4 THEOREM & NUMERICAL SUITES VERIFIED SUCCESSFULLY.")
    print(f"Certificate written to: {out_path}")
    print(f"Canonical SHA-256:      {cert['sha256_canonical']}")
    if "--check" not in sys.argv:
        print(json.dumps(cert, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
