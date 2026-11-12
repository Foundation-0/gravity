"""
Foundation-0 / gravity -- Wave-9 Baryonic-Acceleration Crossover & Cluster-RAR Unification (C-23, C-24)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
"""

from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path

import wave7_group_cluster_threshold_audit as w7

G = 6.67430e-11
C = 299792458.0
M_SUN = 1.98847e30
PC = 3.085677581491367e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
A0 = 1.20e-10
OMEGA_B = 0.0493
OMEGA_M = 0.3150
OMEGA_C_OVER_B = (OMEGA_M - OMEGA_B) / OMEGA_B
F_BAR_R2500_VIKHLININ06 = 0.105
DUST_TO_B_R2500 = (1.0 - F_BAR_R2500_VIKHLININ06) / F_BAR_R2500_VIKHLININ06

KIDS_WL_1000KPC = [
    (10.11, 135.8, 9.6),
    (10.66, 175.3, 9.3),
    (10.96, 211.0, 6.6),
    (11.29, 259.4, 5.1),
]


def nu_rar(y: float) -> float:
    if y <= 0.0:
        return 1.0
    sy = math.sqrt(y)
    return 1.0 if sy > 40.0 else 1.0 / (1.0 - math.exp(-sy))


def invert_apparent_gddag(g_b: float, g_tot: float) -> float:
    ratio = g_tot / g_b
    if ratio <= 1.000001:
        return 0.0
    u = -math.log(1.0 - (1.0 / ratio))
    return g_b / (u * u)


def audit_c23_crossover_and_cluster_rar() -> dict:
    lo, hi = 1.0e-4, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if nu_rar(mid) > 1.0 + OMEGA_C_OVER_B:
            lo = mid
        else:
            hi = mid
    y_cross = 0.5 * (lo + hi)
    gb_cross = y_cross * A0

    r_1mpc = 1.0 * MPC
    kids_bins = []
    for log_mb, v_obs, sv_obs in KIDS_WL_1000KPC:
        mb_kg = (10.0 ** log_mb) * M_SUN
        gb = G * mb_kg / (r_1mpc ** 2)
        g_mond = gb * nu_rar(gb / A0)
        g_dust_max = OMEGA_C_OVER_B * gb
        v_m = math.sqrt(r_1mpc * g_mond) / 1.0e3
        v_md = math.sqrt(r_1mpc * (g_mond + g_dust_max)) / 1.0e3
        kids_bins.append({
            "log10_Mb": log_mb,
            "phonon_over_cosmic_dust_ratio_at_1Mpc": round((g_mond - gb) / g_dust_max, 2),
            "v_obs_kms": v_obs,
            "sigma_v_kms": sv_obs,
            "max_velocity_shift_from_100pct_cosmic_dust_pct": round(((v_md / v_m) - 1.0) * 100.0, 2),
        })

    cluster_rar_benchmarks = []
    for label, gb_val, ref in [
        ("CLASH_inner_mid_gb_4e11", 4.0e-11, "Tian et al. (2020, ApJ 896, 70): g_ddag = (2.02 +/- 0.11)e-9 m/s^2"),
        ("XCOP_Chandra_gb_1_6e11", 1.6e-11, "Pradyumna et al. (2021, PDU 31, 100765): g_ddag = (1.12 +/- 0.11)e-9 m/s^2"),
        ("XCOP_outskirts_gb_3e12", 3.0e-12, "Eckert et al. (2022, A&A 662, A123): virial-boundary flattening toward Omega_m/Omega_b"),
    ]:
        g_rar = gb_val * nu_rar(gb_val / A0)
        g_tot = g_rar + OMEGA_C_OVER_B * gb_val
        g_ddag = invert_apparent_gddag(gb_val, g_tot)
        gb2 = gb_val * 1.05
        gtot2 = gb2 * nu_rar(gb2 / A0) + OMEGA_C_OVER_B * gb2
        slope = math.log(gtot2 / g_tot) / math.log(1.05)
        cluster_rar_benchmarks.append({
            "regime": label,
            "g_bar_m_s2": gb_val,
            "predicted_apparent_g_ddag_1e9_m_s2": round(g_ddag * 1.0e9, 3),
            "predicted_log_slope_dln_gtot_dln_gbar": round(slope, 3),
            "predicted_R_MOND": round(g_tot / g_rar, 3),
            "published_comparison": ref,
        })

    def pred_log10_R(sigma_kms: float, sigma_j_kms: float, dust_ratio: float) -> float:
        if sigma_kms <= sigma_j_kms:
            return 0.0
        f_trap = 1.0 - ((sigma_j_kms / sigma_kms) ** 2)
        g_tot = 2.0 * ((sigma_kms * 1.0e3) ** 2) / (250.0 * KPC)
        lo_g, hi_g = 1.0e-15, g_tot
        for _ in range(55):
            mid_g = 0.5 * (lo_g + hi_g)
            if mid_g * (nu_rar(mid_g / A0) + f_trap * dust_ratio) < g_tot:
                lo_g = mid_g
            else:
                hi_g = mid_g
        gb_sol = 0.5 * (lo_g + hi_g)
        return math.log10(g_tot / (gb_sol * nu_rar(gb_sol / A0)))

    all_rows = w7.build_catalog()
    w_77 = [r for r in all_rows if 150.0 <= r["sig"] <= 1200.0]
    clean_60 = [r for r in all_rows if r["cat"] not in ("Milgrom2019_opt", "Milgrom2019_rich")]

    def fit_1param(ds: list[dict], dust_ratio: float) -> dict:
        best = min(
            ({**w7.odr_chi2(ds, lambda s, sj=float(k): pred_log10_R(s, sj, dust_ratio)), "best_sigma_J_kms": float(k)}
             for k in range(130, 350, 5)),
            key=lambda d: d["chi2"],
        )
        best["k"] = 1
        best["bic"] = round(best["chi2"] + math.log(len(ds)), 4)
        return best

    return {
        "epistemic_status": "COMPUTED & EMPIRICAL-FIT (1-PARAMETER JEANS SCALE; EXTERNAL A0, PLANCK OMEGA_C/OMEGA_B, VIKHLININ F_B,2500)",
        "fixed_external_inputs": {
            "a0_m_s2": A0,
            "Omega_c_over_Omega_b_Planck2018": round(OMEGA_C_OVER_B, 4),
            "f_bar_R2500_Vikhlinin2006": F_BAR_R2500_VIKHLININ06,
            "core_collisionless_to_baryon_ratio_R2500": round(DUST_TO_B_R2500, 4),
        },
        "phonon_dust_equality_crossover": {
            "g_bar_crossover_over_a0": round(y_cross, 5),
            "g_bar_crossover_m_s2": float(f"{gb_cross:.4e}"),
            "lstar_crossover_radius_kpc": round(math.sqrt(G * 6.0e10 * M_SUN / gb_cross) / KPC, 2),
            "rich_cluster_2_5e13Msun_crossover_radius_kpc": round(math.sqrt(G * 2.5e13 * M_SUN / gb_cross) / KPC, 1),
        },
        "kids_1Mpc_galaxy_insensitivity": kids_bins,
        "clash_vs_xcop_apparent_gddag_predictions": cluster_rar_benchmarks,
        "one_parameter_jeans_fits_unsegregated_R200": {
            "primary_77": fit_1param(w_77, OMEGA_C_OVER_B),
            "full_126": fit_1param(all_rows, OMEGA_C_OVER_B),
            "clean_60": fit_1param(clean_60, OMEGA_C_OVER_B),
        },
        "one_parameter_jeans_fits_icm_segregated_R2500": {
            "primary_77": fit_1param(w_77, DUST_TO_B_R2500),
            "full_126": fit_1param(all_rows, DUST_TO_B_R2500),
            "clean_60": fit_1param(clean_60, DUST_TO_B_R2500),
        },
    }


def audit_c24_aest_quasistatic_bound() -> dict:
    mu_inv_bin1 = math.sqrt(1.0 / (18.0 * 0.00390))
    mu_inv_lstar = math.sqrt(1.0 / (18.0 * 0.00835))
    r_m_cl_mpc = math.sqrt(G * 2.5e13 * M_SUN / A0) / MPC
    r_c_cl_mpc = (18.0 * r_m_cl_mpc * (mu_inv_lstar ** 2)) ** (1.0 / 3.0)
    return {
        "epistemic_status": "COMPUTED (PUBLISHED AEST QUASISTATIC EQUATION EVALUATION)",
        "reference": "Verwayen, Skordis & Boehm (2024, MNRAS 531, 272; arXiv:2304.05134, Eq. 35 & 50)",
        "mu_inv_min_KiDS_Bin1_Mpc": round(mu_inv_bin1, 3),
        "mu_inv_min_Lstar_Mpc": round(mu_inv_lstar, 3),
        "implied_cluster_rC_max_Mpc": round(r_c_cl_mpc, 3),
        "cluster_core_250kpc_inside_rC": bool(0.25 < r_c_cl_mpc),
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
    c23 = audit_c23_crossover_and_cluster_rar()
    c24 = audit_c24_aest_quasistatic_bound()

    assert all(b["max_velocity_shift_from_100pct_cosmic_dust_pct"] < 4.5 for b in c23["kids_1Mpc_galaxy_insensitivity"])
    clash_g = c23["clash_vs_xcop_apparent_gddag_predictions"][0]["predicted_apparent_g_ddag_1e9_m_s2"]
    xcop_g = c23["clash_vs_xcop_apparent_gddag_predictions"][1]["predicted_apparent_g_ddag_1e9_m_s2"]
    assert 1.90 <= clash_g <= 2.15 and 0.95 <= xcop_g <= 1.20
    assert c23["one_parameter_jeans_fits_icm_segregated_R2500"]["clean_60"]["bic"] < 66.0
    assert c24["cluster_core_250kpc_inside_rC"] is True

    cert9 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE9-CONVERGENCE/1.0",
        "claim_c23_phonon_dust_crossover_and_cluster_rar": c23,
        "claim_c24_aest_quasistatic_oscillation_bound": c24,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave9_scale_convergence_certificates.json"
    emit_or_verify(cert9, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
