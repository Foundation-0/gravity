"""
Foundation-0 / gravity -- Wave-4 Interpolator Scan, Bogoliubov BVP & Fermion Audit (C-09..C-11)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
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
K_B_EV_K = 8.617333262e-5
T_CMB_K = 2.7255
T_NU0_EV = ((4.0 / 11.0) ** (1.0 / 3.0)) * T_CMB_K * K_B_EV_K

SPARC_RAR_BINS = [
    (-11.69, -10.75, 0.18, 75), (-11.48, -10.70, 0.16, 191),
    (-11.26, -10.57, 0.15, 308), (-11.05, -10.43, 0.14, 323),
    (-10.84, -10.31, 0.13, 283), (-10.62, -10.17, 0.12, 229),
    (-10.41, -10.03, 0.14, 242), (-10.19, -9.90, 0.13, 229),
    (-9.98,  -9.76, 0.14, 204), (-9.76,  -9.60, 0.14, 177),
    (-9.55,  -9.44, 0.14, 137), (-9.34,  -9.29, 0.11, 104),
    (-9.12,  -9.11, 0.13, 85),  (-8.91,  -8.90, 0.11, 43),
]


def mu_alpha(x: float, alpha: float) -> float:
    if x <= 0.0:
        return 0.0
    xa = x ** alpha
    if xa > 45.0:
        return 1.0
    if xa < 1.0e-12:
        return x
    return (1.0 - math.exp(-xa)) ** (1.0 / alpha)


def dln_mu_dln_x(x: float, alpha: float) -> float:
    xa = x ** alpha
    if xa > 45.0:
        return 0.0
    if xa < 1.0e-9:
        return 1.0
    ex = math.exp(-xa)
    return (xa * ex) / (1.0 - ex)


def invert_gobs_from_gbar(gbar: float, a0: float, alpha: float) -> float:
    y = gbar / a0
    lo = y
    hi = max(y * 2.0, math.sqrt(y) * 2.0) + 5.0
    while mu_alpha(hi, alpha) * hi < y:
        hi *= 2.0
    for _ in range(52):
        mid = 0.5 * (lo + hi)
        if mu_alpha(mid, alpha) * mid < y:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi) * a0


def wide_binary_velocity_boost_pct(e_mw: float, alpha: float) -> float:
    mu_e = mu_alpha(e_mw, alpha)
    l_e = dln_mu_dln_x(e_mw, alpha)
    n_th = 600
    dth = math.pi / n_th
    acc = sum(
        math.sin((i + 0.5) * dth) / (mu_e * math.sqrt(1.0 + l_e * (math.sin((i + 0.5) * dth) ** 2)))
        for i in range(n_th)
    ) * dth
    return (math.sqrt(0.5 * acc) - 1.0) * 100.0


def check_c09_interpolator_tradeoff() -> dict:
    g_mw_si = (233.0e3 ** 2) / (8.1 * KPC)
    alphas = [round(0.45 + 0.05 * k, 2) for k in range(56)]
    grid_evals = []
    min_chi2_overall = 1.0e30

    for alpha in alphas:
        best_c2 = 1.0e30
        best_a0 = 1.2e-10
        for j in range(61):
            a0_try = (0.85 + 0.85 * j / 60.0) * 1.0e-10
            c2 = sum(
                ((lgo - math.log10(invert_gobs_from_gbar(10.0 ** lgb, a0_try, alpha))) / (sd / math.sqrt(n_pts))) ** 2
                for lgb, lgo, sd, n_pts in SPARC_RAR_BINS
            )
            if c2 < best_c2:
                best_c2 = c2
                best_a0 = a0_try
        e_mw = g_mw_si / best_a0
        wb_pct = wide_binary_velocity_boost_pct(e_mw, alpha)
        grid_evals.append((alpha, best_a0, best_c2, e_mw, wb_pct))
        min_chi2_overall = min(min_chi2_overall, best_c2)

    min_wb_5sig = min(wb for _, _, c2, _, wb in grid_evals if c2 - min_chi2_overall <= 25.0)
    min_dc2_2pct = min(c2 - min_chi2_overall for _, _, c2, _, wb in grid_evals if wb <= 2.0)
    scan_rows = [
        {
            "alpha_sharpness": alpha,
            "profiled_a0_1e10_m_s2": round(best_a0 * 1.0e10, 4),
            "sparc_rar_chi2": round(best_c2, 2),
            "delta_chi2_from_min": round(best_c2 - min_chi2_overall, 2),
            "e_MW_at_profiled_a0": round(e_mw, 4),
            "wide_binary_velocity_boost_pct": round(wb_pct, 2),
        }
        for alpha, best_a0, best_c2, e_mw, wb_pct in grid_evals
        if alpha in {0.5, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0}
    ]
    return {
        "epistemic_status": "COMPUTED (MODEL-FAMILY-SCAN)",
        "caveat": "Scans mu_alpha(x) = (1 - exp(-x^alpha))^(1/alpha); 2% wide-binary ceiling is an input assumption.",
        "g_MW_solar_circle_1e10_m_s2": round(g_mw_si * 1.0e10, 4),
        "min_sparc_chi2": round(min_chi2_overall, 3),
        "min_wb_velocity_boost_pct_within_delta_chi2_25": round(min_wb_5sig, 2),
        "min_sparc_delta_chi2_if_wb_boost_le_2pct": round(min_dc2_2pct, 2),
        "alpha_tradeoff_table": scan_rows,
    }


def solve_tridiagonal(a: list[float], b: list[float], c: list[float], d: list[float]) -> list[float]:
    n = len(b)
    cp = [0.0] * n
    dp = [0.0] * n
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        denom = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / denom if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denom
    x = [0.0] * n
    x[n - 1] = dp[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def solve_action_bogoliubov_bvp(mass_msun: float, r_b_m: float, xi_coh_kpc: float) -> dict:
    xi_m = xi_coh_kpc * KPC
    m_kg = mass_msun * M_SUN
    n_pts = 550
    s_min, s_max = math.log(AU), math.log(MPC)
    ds = (s_max - s_min) / (n_pts - 1)
    s_grid = [s_min + i * ds for i in range(n_pts)]
    r_grid = [math.exp(s) for s in s_grid]
    rhs_src = [G * m_kg * ((r / (r + r_b_m)) ** 2) for r in r_grid]
    u = [math.sqrt(A0 * src) * (r / (r + xi_m)) for r, src in zip(r_grid, rhs_src)]
    u[0] = 0.0

    for _ in range(35):
        a_sub, b_diag, c_sup, res = [0.0] * n_pts, [1.0] * n_pts, [0.0] * n_pts, [0.0] * n_pts
        for i in range(1, n_pts - 1):
            pref = (xi_m * xi_m) / r_grid[i]
            u_pp = (u[i + 1] - 2.0 * u[i] + u[i - 1]) / (ds * ds)
            u_p = (u[i + 1] - u[i - 1]) / (2.0 * ds)
            res[i] = pref * (u_pp - u_p - 2.0 * u[i]) - (u[i] * u[i]) / A0 + rhs_src[i]
            a_sub[i] = -pref * (1.0 / (ds * ds) + 1.0 / (2.0 * ds))
            b_diag[i] = -pref * (-2.0 / (ds * ds) - 2.0) + (2.0 * u[i]) / A0
            c_sup[i] = -pref * (1.0 / (ds * ds) - 1.0 / (2.0 * ds))
        res[-1] = math.sqrt(A0 * rhs_src[-1]) - u[-1]
        delta = solve_tridiagonal(a_sub, b_diag, c_sup, res)
        u = [max(0.0, ui + di) for ui, di in zip(u, delta)]
        if max(abs(di) for di in delta) < 1.0e-7:
            break

    max_rel_res = max(
        abs(-((xi_m * xi_m) / r_grid[i]) * ((u[i + 1] - 2.0 * u[i] + u[i - 1]) / (ds * ds) - (u[i + 1] - u[i - 1]) / (2.0 * ds) - 2.0 * u[i]) + (u[i] * u[i]) / A0 - rhs_src[i]) / (G * m_kg)
        for i in range(1, n_pts - 1)
    )

    def interp_ratio(target_r_m: float) -> tuple[float, float]:
        ts = math.log(target_r_m)
        idx = min(max(int((ts - s_min) / ds), 0), n_pts - 2)
        w = (ts - s_grid[idx]) / ds
        g_ph = (u[idx] * (1.0 - w) + u[idx + 1] * w) / target_r_m
        g_n = G * m_kg / ((target_r_m + r_b_m) ** 2)
        return g_ph, g_ph / g_n

    return {
        "max_relative_ode_residual": max_rel_res,
        "saturn_9_58AU": interp_ratio(9.58 * AU),
        "wide_binary_10kAU": interp_ratio(1.0e4 * AU),
        "wide_binary_20kAU": interp_ratio(2.0e4 * AU),
        "galactic_100kpc": interp_ratio(100.0 * KPC),
        "galactic_1Mpc": interp_ratio(1.0 * MPC),
    }


def check_c10_c11_bogoliubov_and_fermion_audit() -> dict:
    xi_coh_kpc = 0.20
    f_b = 0.025
    v_gal_ms = 175.8e3
    m_boson_ev = (HBAR / (math.sqrt(2.0) * (xi_coh_kpc * KPC) * v_gal_ms)) / EV_KG

    sol_star = solve_action_bogoliubov_bvp(1.0, 0.005 * AU, xi_coh_kpc)
    sol_gal = solve_action_bogoliubov_bvp(6.0e10, 2.97 * KPC, xi_coh_kpc)

    g_n_100 = G * 6.0e10 * M_SUN / (((100.0 + 2.97) * KPC) ** 2)
    g_n_1000 = G * 6.0e10 * M_SUN / (((1000.0 + 2.97) * KPC) ** 2)
    gal_rec_100 = (sol_gal["galactic_100kpc"][0] / math.sqrt(A0 * g_n_100)) * 100.0

    g_f = 2.0
    omega_f_h2 = 0.117
    rho_dyn_dwarf = ((25.0e3) ** 2) / (4.0 * math.pi * G * (KPC ** 2))
    rho_dyn_lstar = (v_gal_ms ** 2) / (4.0 * math.pi * G * ((10.0 * KPC) ** 2))
    rho_dyn_bullet = (2.0 * ((1000.0e3) ** 2)) / (4.0 * math.pi * G * ((250.0 * KPC) ** 2))

    def fermion_profile(mf_ev: float) -> dict:
        mf_kg = mf_ev * EV_KG
        pref = g_f * (mf_kg ** 4) / (((2.0 * math.pi) ** 1.5) * (HBAR ** 3))
        t_ratio = ((2.0 / g_f) * (omega_f_h2 * 93.14 / mf_ev)) ** (1.0 / 3.0)
        g_star_s_dec_req = 10.75 / (t_ratio ** 3)
        dneff_bbn = (g_f / 2.0) * (t_ratio ** 4)
        rho_f_over_rho_gamma_uv = (7.0 / 8.0) * ((4.0 / 11.0) ** (4.0 / 3.0)) * dneff_bbn
        z_nr = (mf_ev / (3.15137 * T_NU0_EV * t_ratio)) - 1.0
        return {
            "m_F_eV": mf_ev,
            "required_T_F_over_T_nu": round(t_ratio, 4),
            "required_g_star_S_at_decoupling": round(g_star_s_dec_req, 2),
            "Delta_N_eff_at_BBN_relativistic": round(dneff_bbn, 4),
            "rho_F_over_rho_gamma_UV_with_7_8_factor": round(rho_f_over_rho_gamma_uv, 4),
            "nonrelativistic_transition_z_nr": round(z_nr, 1),
            "nonrelativistic_prior_to_CMB_z1100": bool(z_nr > 1100.0),
            "excluded_by_WDM_freestreaming_lt_3keV": bool(mf_ev < 3000.0),
            "dwarf_1kpc_max_halo_frac_pct": round((pref * (15.0e3 ** 3) / rho_dyn_dwarf) * 100.0, 5),
            "spiral_10kpc_max_halo_frac_pct": round((pref * (125.0e3 ** 3) / rho_dyn_lstar) * 100.0, 4),
            "bullet_250kpc_capacity_ratio": round((pref * (1000.0e3 ** 3)) / rho_dyn_bullet, 2),
        }

    return {
        "epistemic_status": "COMPUTED (BVP-SOLVER & FREEZE-OUT-ARITHMETIC)",
        "input_coherence_length_xi_kpc": xi_coh_kpc,
        "implied_ultralight_boson_mass_eV": float(f"{m_boson_ev:.4e}"),
        "input_boson_dm_fraction_f_B": f_b,
        "f_B_below_0_20_published_rule_of_thumb": bool(f_b < 0.20),
        "lyman_alpha_caveat": (
            "xi_coh = 0.20 kpc and f_B = 0.025 are chosen inputs; f_B < 0.20 is a threshold check "
            "against Kobayashi et al. (2017, PRD 96, 123514), not a hydrodynamical forest transfer-function solve."
        ),
        "stellar_wide_binary_ode_audit": {
            "max_relative_ode_residual": float(f"{sol_star['max_relative_ode_residual']:.3e}"),
            "saturn_9_58AU_gph_over_gN": float(f"{sol_star['saturn_9_58AU'][1]:.3e}"),
            "wide_binary_10kAU_gph_over_gN": float(f"{sol_star['wide_binary_10kAU'][1]:.3e}"),
            "wide_binary_20kAU_gph_over_gN": float(f"{sol_star['wide_binary_20kAU'][1]:.3e}"),
            "wide_binary_20kAU_velocity_shift_pct": float(f"{(math.sqrt(1.0 + sol_star['wide_binary_20kAU'][1]) - 1.0) * 100.0:.3e}"),
        },
        "lstar_galaxy_ode_audit": {
            "max_relative_ode_residual": float(f"{sol_gal['max_relative_ode_residual']:.3e}"),
            "recovery_of_deep_MOND_limit_at_100kpc_pct": round(gal_rec_100, 5),
            "v_circ_100kpc_kms": round(math.sqrt(100.0 * KPC * (g_n_100 + sol_gal["galactic_100kpc"][0])) / 1.0e3, 2),
            "v_circ_1Mpc_kms": round(math.sqrt(1000.0 * KPC * (g_n_1000 + sol_gal["galactic_1Mpc"][0])) / 1.0e3, 2),
        },
        "claim_c11_relativistic_freezeout_fermion_audit": [
            fermion_profile(3.0),
            fermion_profile(11.0),
            fermion_profile(35.0),
        ],
    }


def emit_or_verify(cert: dict, out_path: Path) -> None:
    canonical = json.dumps(cert, sort_keys=True, separators=(",", ":")).encode("utf-8")
    cert["sha256_canonical"] = hashlib.sha256(canonical).hexdigest()
    rendered = json.dumps(cert, indent=2) + "\n"
    if "--check" in sys.argv:
        assert out_path.is_file(), f"Missing certificate file: {out_path}"
        on_disk_text = out_path.read_text(encoding="utf-8")
        on_disk_obj = json.loads(on_disk_text)
        stored_sha = on_disk_obj.pop("sha256_canonical", None)
        disk_canonical = json.dumps(on_disk_obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
        assert stored_sha == hashlib.sha256(disk_canonical).hexdigest(), "Canonical SHA-256 mismatch on disk"
        assert stored_sha == cert["sha256_canonical"], "Recomputed canonical SHA-256 mismatch"
        assert on_disk_text == rendered, "Certificate file is not byte-identical to generator output"
        print(f"CHECK OK (byte-identical): {out_path.name} sha256_canonical={stored_sha}")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"WROTE {out_path.name} sha256_canonical={cert['sha256_canonical']}")


def main() -> int:
    c09 = check_c09_interpolator_tradeoff()
    c10_c11 = check_c10_c11_bogoliubov_and_fermion_audit()

    assert c09["min_wb_velocity_boost_pct_within_delta_chi2_25"] > 10.0
    assert c09["min_sparc_delta_chi2_if_wb_boost_le_2pct"] > 300.0
    assert c10_c11["stellar_wide_binary_ode_audit"]["saturn_9_58AU_gph_over_gN"] < 1.0e-11
    assert c10_c11["stellar_wide_binary_ode_audit"]["wide_binary_20kAU_gph_over_gN"] < 1.0e-5
    assert c10_c11["lstar_galaxy_ode_audit"]["recovery_of_deep_MOND_limit_at_100kpc_pct"] > 99.9
    assert all(row["nonrelativistic_prior_to_CMB_z1100"] for row in c10_c11["claim_c11_relativistic_freezeout_fermion_audit"])

    cert4 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE4-UNIFIED/1.1",
        "claim_c09_interpolator_tradeoff": c09,
        "claims_c10_c11_bogoliubov_and_fermion_audit": c10_c11,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave4_unified_certificates.json"
    emit_or_verify(cert4, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
