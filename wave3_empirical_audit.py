#!/usr/bin/env python3
"""
Foundation-0 / gravity — Wave-3 Empirical Observational Audit
=============================================================
Zero-dependency Python 3 standard-library statistical evaluation of quantum-condensate
and fractal-gravity models against real published astronomical measurements:

1. Official SPARC Binned Radial Acceleration Relation (`RARbins.mrt`, 2,630 points across
   153 galaxies; Lelli, McGaugh, Schombert & Pawlowski 2017, ApJ 836, 152):
   https://astroweb.cwru.edu/SPARC/RARbins.mrt
2. KiDS-1000 Weak-Lensing (139,027 isolated lenses, 50-1000 kpc) & SPARC Kinematic BTFR
   Table 2 (Mistele, McGaugh, Lelli, Schombert & Li 2024, ApJL 969, L3):
   https://arxiv.org/html/2406.09685v1

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
M_SUN = 1.98847e30
PC = 3.085677581491367e16
KPC = 1.0e3 * PC

SPARC_RAR_BINS = [
    (-11.69, -10.75, 0.18, 75),
    (-11.48, -10.70, 0.16, 191),
    (-11.26, -10.57, 0.15, 308),
    (-11.05, -10.43, 0.14, 323),
    (-10.84, -10.31, 0.13, 283),
    (-10.62, -10.17, 0.12, 229),
    (-10.41, -10.03, 0.14, 242),
    (-10.19, -9.90, 0.13, 229),
    (-9.98,  -9.76, 0.14, 204),
    (-9.76,  -9.60, 0.14, 177),
    (-9.55,  -9.44, 0.14, 137),
    (-9.34,  -9.29, 0.11, 104),
    (-9.12,  -9.11, 0.13, 85),
    (-8.91,  -8.90, 0.11, 43),
]

KIDS_WL_ALL_300KPC = [
    (10.10, 137.3, 11.5),
    (10.66, 182.1, 10.8),
    (10.96, 204.7, 8.2),
    (11.29, 260.2, 6.2),
]

KIDS_WL_ALL_1000KPC = [
    (10.11, 135.8, 9.6),
    (10.66, 175.3, 9.3),
    (10.96, 211.0, 6.6),
    (11.29, 259.4, 5.1),
]

SPARC_KINEMATIC_BTFR = [
    (8.69, 0.06, 54.2, 1.0),
    (9.25, 0.04, 77.9, 1.1),
    (9.67, 0.08, 89.1, 1.3),
    (10.00, 0.05, 121.7, 1.8),
    (10.46, 0.05, 160.7, 1.7),
    (10.72, 0.09, 186.6, 3.3),
    (11.03, 0.05, 219.3, 1.8),
    (11.34, 0.10, 271.0, 6.4),
]


def pred_log10_gobs(log10_gbar: float, ds: float, a0: float) -> float:
    gb = 10.0 ** log10_gbar
    if ds <= 1.0e-9:
        return log10_gbar
    gamma = ds / (1.0 + ds)
    u = (gb / a0) ** gamma
    if u > 40.0:
        return log10_gbar
    return math.log10(gb / (1.0 - math.exp(-u)))


def fit_1_sparc_rar_spectral_dimension() -> dict:
    total_points = sum(row[3] for row in SPARC_RAR_BINS)

    def chi2_for(ds: float, a0: float) -> float:
        c2 = 0.0
        for lgb, lgo, sd, n_pts in SPARC_RAR_BINS:
            sem = sd / math.sqrt(n_pts)
            pred = pred_log10_gobs(lgb, ds, a0)
            c2 += ((lgo - pred) / sem) ** 2
        return c2

    best_a0_ds1 = 1.20e-10
    min_c2_ds1 = 1.0e30
    for j in range(600):
        a0_try = (0.80 + 0.80 * j / 599.0) * 1.0e-10
        c2 = chi2_for(1.0, a0_try)
        if c2 < min_c2_ds1:
            min_c2_ds1 = c2
            best_a0_ds1 = a0_try

    best_ds = 1.0
    best_a0_joint = best_a0_ds1
    min_c2_joint = 1.0e30
    profile_table = []
    profile_cache = []

    for i in range(141):
        ds_val = 0.40 + 0.01 * i
        c2_prof = 1.0e30
        a0_prof = 1.2e-10
        for j in range(401):
            a0_try = (0.40 + 2.20 * j / 400.0) * 1.0e-10
            c2 = chi2_for(ds_val, a0_try)
            if c2 < c2_prof:
                c2_prof = c2
                a0_prof = a0_try
        profile_cache.append((ds_val, c2_prof))
        if c2_prof < min_c2_joint:
            min_c2_joint = c2_prof
            best_ds = ds_val
            best_a0_joint = a0_prof
        if i % 15 == 0 or abs(ds_val - 0.75) < 1e-9 or abs(ds_val - 0.94) < 1e-9 or abs(ds_val - 1.00) < 1e-9:
            profile_table.append({
                "d_s": round(ds_val, 2),
                "implied_btfr_slope": round(2.0 * (1.0 + ds_val), 3),
                "profiled_a0_1e10_m_s2": round(a0_prof * 1.0e10, 4),
                "chi2_14bins": round(c2_prof, 3),
            })

    ds_1sigma = [ds_v for ds_v, c2_v in profile_cache if c2_v <= min_c2_joint + 1.0]
    chi2_ds075 = next(c2_v for ds_v, c2_v in profile_cache if abs(ds_v - 0.75) < 1e-9)

    return {
        "n_rotation_points": total_points,
        "n_bins": len(SPARC_RAR_BINS),
        "newtonian_no_dm_chi2": round(chi2_for(0.0, 1.2e-10), 1),
        "fixed_ds1_best_a0_1e10_m_s2": round(best_a0_ds1 * 1.0e10, 4),
        "fixed_ds1_chi2": round(min_c2_ds1, 3),
        "constitutive_ds075_chi2": round(chi2_ds075, 3),
        "delta_chi2_ds075_vs_ds1": round(chi2_ds075 - min_c2_ds1, 3),
        "joint_best_ds": round(best_ds, 3),
        "joint_ds_1sigma_interval": [round(min(ds_1sigma), 3), round(max(ds_1sigma), 3)],
        "joint_best_a0_1e10_m_s2": round(best_a0_joint * 1.0e10, 4),
        "joint_min_chi2": round(min_c2_joint, 3),
        "profile_scan": profile_table,
    }


def fit_btfr_sample(rows: list[tuple[float, float, float, float]], beta_fixed: float | None = None) -> dict:
    best_beta = beta_fixed if beta_fixed is not None else 4.0
    best_a = 0.0
    best_c2 = 1.0e30
    betas = [beta_fixed] if beta_fixed is not None else [1.80 + 0.01 * k for k in range(321)]

    for b_try in betas:
        w_sum = 0.0
        wy_sum = 0.0
        for lmb, slmb, vf, svf in rows:
            sv_log = svf / (vf * math.log(10.0))
            var = slmb * slmb + (b_try * sv_log) ** 2
            w = 1.0 / var
            w_sum += w
            wy_sum += w * (lmb - b_try * math.log10(vf))
        a_opt = wy_sum / w_sum
        c2 = 0.0
        for lmb, slmb, vf, svf in rows:
            sv_log = svf / (vf * math.log(10.0))
            var = slmb * slmb + (b_try * sv_log) ** 2
            c2 += ((lmb - (a_opt + b_try * math.log10(vf))) ** 2) / var
        if c2 < best_c2:
            best_c2 = c2
            best_beta = b_try
            best_a = a_opt

    k_params = 1 if beta_fixed is not None else 2
    n_obs = len(rows)
    return {
        "beta_slope": round(best_beta, 4),
        "implied_effective_ds": round(0.5 * best_beta - 1.0, 4),
        "intercept_A": round(best_a, 4),
        "chi2": round(best_c2, 3),
        "dof": n_obs - k_params,
        "BIC": round(best_c2 + k_params * math.log(n_obs), 3),
    }


def fit_2_scale_flow_kinematic_vs_1mpc_lensing() -> dict:
    sparc_rows = [(lmb, slmb, vf, svf) for lmb, slmb, vf, svf in SPARC_KINEMATIC_BTFR]
    kids_rows_stat = [(lmb, 0.02, vf, svf) for lmb, vf, svf in KIDS_WL_ALL_1000KPC]
    combined_rows = sparc_rows + [(lmb, 0.10, vf, svf) for lmb, vf, svf in KIDS_WL_ALL_1000KPC]

    kin_free = fit_btfr_sample(sparc_rows, None)
    wl_free = fit_btfr_sample(kids_rows_stat, None)

    comb_free = fit_btfr_sample(combined_rows, None)
    comb_ds1 = fit_btfr_sample(combined_rows, 4.0)
    comb_ds075 = fit_btfr_sample(combined_rows, 3.5)
    comb_coord = fit_btfr_sample(combined_rows, 2.0)

    return {
        "regime_progression_inner_to_1Mpc": {
            "inner_SPARC_kinematic_10_30kpc": kin_free,
            "outer_KiDS_weak_lensing_50_1000kpc": wl_free,
        },
        "combined_12bin_model_comparison": {
            "free_powerlaw": comb_free,
            "ds1_condensate_beta_4_0": comb_ds1,
            "constitutive_ds075_beta_3_5": comb_ds075,
            "coord_fractal_Df2_beta_2_0": comb_coord,
        },
        "delta_BIC_coord_fractal_vs_ds1": round(comb_coord["BIC"] - comb_ds1["BIC"], 2),
        "delta_BIC_beta35_vs_ds1": round(comb_ds075["BIC"] - comb_ds1["BIC"], 2),
        "delta_BIC_free_vs_ds1": round(comb_free["BIC"] - comb_ds1["BIC"], 2),
    }


def fit_3_cosmic_efe_bound(a0_rar: float) -> dict:
    ratios = []
    for (lmb3, v3, s3), (lmb10, v10, s10) in zip(KIDS_WL_ALL_300KPC, KIDS_WL_ALL_1000KPC):
        r_m_kpc = math.sqrt(G * ((10.0 ** lmb10) * M_SUN) / a0_rar) / KPC
        ratio = v10 / v3
        sig_ratio = ratio * math.sqrt((s3 / v3) ** 2 + (s10 / v10) ** 2)
        ratios.append({
            "log10_Mb": lmb10,
            "r_M_kpc": round(r_m_kpc, 2),
            "Vflat_300kpc_kms": v3,
            "Vflat_1000kpc_kms": v10,
            "ratio_V1000_over_V300": round(ratio, 4),
            "sigma_ratio_conservative": round(sig_ratio, 4),
        })

    def pred_ratio(r_m_kpc: float, e_val: float) -> float:
        if e_val <= 1.0e-9:
            return 1.0
        r_efe = r_m_kpc / e_val
        def avg_v(r_lo: float, r_hi: float) -> float:
            n = 60
            return sum(
                ((1.0 / math.sqrt(1.0 + ((r_lo * ((r_hi / r_lo) ** ((k + 0.5) / n))) / r_efe) ** 2)) ** 0.5)
                for k in range(n)
            ) / n
        return avg_v(50.0, 1000.0) / avg_v(50.0, 300.0)

    c2_e0 = sum(((r["ratio_V1000_over_V300"] - 1.0) / r["sigma_ratio_conservative"]) ** 2 for r in ratios)
    e_95 = 0.0
    for k in range(500):
        e_try = 0.0002 * k
        c2 = sum(
            ((r["ratio_V1000_over_V300"] - pred_ratio(r["r_M_kpc"], e_try)) / r["sigma_ratio_conservative"]) ** 2
            for r in ratios
        )
        if c2 <= c2_e0 + 3.841:
            e_95 = e_try

    return {
        "kids_300_vs_1000kpc_bins": ratios,
        "chi2_at_e0_indefinite_flatness": round(c2_e0, 4),
        "cosmic_efe_95CL_upper_bound_gext_over_a0": round(e_95, 4),
        "min_EFE_horizon_for_Lstar_kpc": round(8.348 / e_95, 1) if e_95 > 0 else None,
    }


def main() -> int:
    f1 = fit_1_sparc_rar_spectral_dimension()
    a0_emp = f1["fixed_ds1_best_a0_1e10_m_s2"] * 1.0e-10
    f2 = fit_2_scale_flow_kinematic_vs_1mpc_lensing()
    f3 = fit_3_cosmic_efe_bound(a0_emp)

    assert 0.90 <= f1["joint_best_ds"] <= 1.05
    assert f1["delta_chi2_ds075_vs_ds1"] > 50.0
    assert f2["delta_BIC_coord_fractal_vs_ds1"] > 400.0
    assert f2["delta_BIC_beta35_vs_ds1"] > 8.0
    assert f2["regime_progression_inner_to_1Mpc"]["outer_KiDS_weak_lensing_50_1000kpc"]["beta_slope"] > (
        f2["regime_progression_inner_to_1Mpc"]["inner_SPARC_kinematic_10_30kpc"]["beta_slope"]
    )
    assert f3["cosmic_efe_95CL_upper_bound_gext_over_a0"] <= 0.025

    cert3 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE3-EMPIRICAL/1.0",
        "datasets": {
            "sparc_rar_url": "https://astroweb.cwru.edu/SPARC/RARbins.mrt",
            "kids_weak_lensing_url": "https://arxiv.org/html/2406.09685v1",
        },
        "fit_1_sparc_rar_2630_points": f1,
        "fit_2_scale_flow_and_btfr": f2,
        "fit_3_cosmic_efe_bound": f3,
    }
    canonical = json.dumps(cert3, sort_keys=True, separators=(",", ":")).encode("utf-8")
    cert3["sha256_canonical"] = hashlib.sha256(canonical).hexdigest()

    out_path = Path(__file__).resolve().parent / "results" / "wave3_empirical_certificates.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cert3, indent=2) + "\n", encoding="utf-8")
    print("ALL WAVE-3 EMPIRICAL OBSERVATIONAL CHECKS PASSED.")
    print(f"Canonical SHA-256: {cert3['sha256_canonical']}")
    if "--check" not in sys.argv:
        print(json.dumps(cert3, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
