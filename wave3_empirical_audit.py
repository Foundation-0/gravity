"""
Foundation-0 / gravity -- Wave-3 Empirical Binned Fit Audit (Claim C-08)
========================================================================
Python 3 standard-library statistical evaluation of generalized RAR / BTFR
scaling expressions against published binned astronomical tables:

  1. SPARC Binned Radial Acceleration Relation (RARbins.mrt, 14 bin means
     summarizing 2,630 rotation points across 153 galaxies; Lelli, McGaugh,
     Schombert & Pawlowski 2017, ApJ 836, 152). Note: Using s/sqrt(N) on bin
     means treats radial points within the same galaxy as independent and
     yields a profiled minimum at d_s = 0.94 (1-sigma [0.92, 0.96]), not 1.00.
  2. KiDS-1000 Weak-Lensing Stacked BTFR (4 stellar-mass bins totaling
     52,553 + 43,727 + 22,950 + 9,797 = 129,027 isolated lenses, 50-1000 kpc)
     & SPARC Kinematic BTFR (8 bins) from Mistele, McGaugh, Lelli, Schombert
     & Li (2024, ApJL 969, L3; arXiv:2406.09685, Sec. II & Table 2). Note:
     Mistele et al. adopt H0 = 73.0 km/s/Mpc (whereas Planck 2018 H0 = 67.4
     km/s/Mpc is used in a_dS elsewhere in this repository).

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
    (-11.69, -10.75, 0.18, 75), (-11.48, -10.70, 0.16, 191),
    (-11.26, -10.57, 0.15, 308), (-11.05, -10.43, 0.14, 323),
    (-10.84, -10.31, 0.13, 283), (-10.62, -10.17, 0.12, 229),
    (-10.41, -10.03, 0.14, 242), (-10.19, -9.90, 0.13, 229),
    (-9.98,  -9.76, 0.14, 204), (-9.76,  -9.60, 0.14, 177),
    (-9.55,  -9.44, 0.14, 137), (-9.34,  -9.29, 0.11, 104),
    (-9.12,  -9.11, 0.13, 85),  (-8.91,  -8.90, 0.11, 43),
]

KIDS_ISOLATED_LENS_COUNTS_BY_BIN = [52553, 43727, 22950, 9797]

KIDS_WL_ALL_300KPC = [
    (10.10, 137.3, 11.5), (10.66, 182.1, 10.8),
    (10.96, 204.7, 8.2),  (11.29, 260.2, 6.2),
]

KIDS_WL_ALL_1000KPC = [
    (10.11, 135.8, 9.6), (10.66, 175.3, 9.3),
    (10.96, 211.0, 6.6), (11.29, 259.4, 5.1),
]

SPARC_KINEMATIC_BTFR = [
    (8.69, 0.06, 54.2, 1.0),  (9.25, 0.04, 77.9, 1.1),
    (9.67, 0.08, 89.1, 1.3),  (10.00, 0.05, 121.7, 1.8),
    (10.46, 0.05, 160.7, 1.7), (10.72, 0.09, 186.6, 3.3),
    (11.03, 0.05, 219.3, 1.8), (11.34, 0.10, 271.0, 6.4),
]


def pred_log10_gobs(log10_gbar: float, ds: float, a0: float) -> float:
    gb = 10.0 ** log10_gbar
    if ds <= 1.0e-9:
        return log10_gbar
    u = (gb / a0) ** (ds / (1.0 + ds))
    if u > 40.0:
        return log10_gbar
    return math.log10(gb / (1.0 - math.exp(-u)))


def fit_1_sparc_rar_spectral_dimension() -> dict:
    total_points = sum(row[3] for row in SPARC_RAR_BINS)

    def chi2_for(ds: float, a0: float) -> float:
        return sum(
            ((lgo - pred_log10_gobs(lgb, ds, a0)) / (sd / math.sqrt(n_pts))) ** 2
            for lgb, lgo, sd, n_pts in SPARC_RAR_BINS
        )

    best_ds = 1.0
    best_a0_joint = 1.2e-10
    min_c2_joint = 1.0e30
    profile_table = []
    profile_cache = []

    for i in range(141):
        ds_val = round(0.40 + 0.01 * i, 2)
        c2_prof = 1.0e30
        a0_prof = 1.2e-10
        for j in range(2201):
            a0_try = (0.40 + 0.001 * j) * 1.0e-10
            c2 = chi2_for(ds_val, a0_try)
            if c2 < c2_prof:
                c2_prof = c2
                a0_prof = a0_try
        profile_cache.append((ds_val, a0_prof, c2_prof))
        if c2_prof < min_c2_joint:
            min_c2_joint = c2_prof
            best_ds = ds_val
            best_a0_joint = a0_prof
        if i % 15 == 0 or ds_val in (0.75, 0.94, 1.00):
            profile_table.append({
                "d_s": ds_val,
                "implied_btfr_slope": round(2.0 * (1.0 + ds_val), 3),
                "profiled_a0_1e10_m_s2": round(a0_prof * 1.0e10, 4),
                "chi2_14bins": round(c2_prof, 3),
            })

    _, best_a0_ds1, min_c2_ds1 = next(t for t in profile_cache if t[0] == 1.00)
    _, _, chi2_ds075 = next(t for t in profile_cache if t[0] == 0.75)
    ds_1sigma = [ds_v for ds_v, _, c2_v in profile_cache if c2_v <= min_c2_joint + 1.0]

    return {
        "epistemic_status": "EMPIRICAL-FIT (KNOWN-RAR-INTERPOLATOR)",
        "methodology_caveat": (
            "Fit to 14 published RARbins.mrt bin means using sem = sd/sqrt(N), which treats "
            "radial points within the same galaxy as independent; joint minimum is d_s = 0.94, not 1.00."
        ),
        "n_rotation_points_summarized": total_points,
        "n_bins_fitted": len(SPARC_RAR_BINS),
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
    betas = [beta_fixed] if beta_fixed is not None else [round(1.80 + 0.01 * k, 2) for k in range(321)]

    for b_try in betas:
        w_sum = 0.0
        wy_sum = 0.0
        for lmb, slmb, vf, svf in rows:
            sv_log = svf / (vf * math.log(10.0))
            w = 1.0 / (slmb * slmb + (b_try * sv_log) ** 2)
            w_sum += w
            wy_sum += w * (lmb - b_try * math.log10(vf))
        a_opt = wy_sum / w_sum
        c2 = sum(
            ((lmb - (a_opt + b_try * math.log10(vf))) ** 2)
            / (slmb * slmb + (b_try * (svf / (vf * math.log(10.0)))) ** 2)
            for lmb, slmb, vf, svf in rows
        )
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


def fit_2_btfr_sparc_and_kids() -> dict:
    sparc_rows = list(SPARC_KINEMATIC_BTFR)
    kids_rows_stat = [(lmb, 0.02, vf, svf) for lmb, vf, svf in KIDS_WL_ALL_1000KPC]
    combined_rows = sparc_rows + [(lmb, 0.10, vf, svf) for lmb, vf, svf in KIDS_WL_ALL_1000KPC]

    kin_free = fit_btfr_sample(sparc_rows, None)
    wl_free = fit_btfr_sample(kids_rows_stat, None)
    comb_free = fit_btfr_sample(combined_rows, None)
    comb_ds1 = fit_btfr_sample(combined_rows, 4.0)
    comb_ds075 = fit_btfr_sample(combined_rows, 3.5)
    comb_coord = fit_btfr_sample(combined_rows, 2.0)

    return {
        "methodology_caveat": (
            "Fits 8 SPARC kinematic BTFR bins and 4 stacked KiDS WL BTFR bins (0.02 dex assumed "
            "centroid mass error in standalone WL fit; 0.10 dex M*/L systematic in 12-bin fit). "
            "Combined free slope is beta = 3.83 with delta_BIC(free - beta=4) = -0.44."
        ),
        "separate_sample_fits": {
            "SPARC_kinematic_BTFR_8bins": kin_free,
            "KiDS_weak_lensing_BTFR_4bins_1000kpc": wl_free,
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
    for (_, v3, s3), (lmb10, v10, s10) in zip(KIDS_WL_ALL_300KPC, KIDS_WL_ALL_1000KPC):
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
                (1.0 / math.sqrt(1.0 + ((r_lo * ((r_hi / r_lo) ** ((k + 0.5) / n))) / r_efe) ** 2)) ** 0.5
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
    assert sum(KIDS_ISOLATED_LENS_COUNTS_BY_BIN) == 129027
    f1 = fit_1_sparc_rar_spectral_dimension()
    a0_emp = f1["fixed_ds1_best_a0_1e10_m_s2"] * 1.0e-10
    f2 = fit_2_btfr_sparc_and_kids()
    f3 = fit_3_cosmic_efe_bound(a0_emp)

    ds1_row = next(r for r in f1["profile_scan"] if r["d_s"] == 1.0)
    assert f1["fixed_ds1_chi2"] == ds1_row["chi2_14bins"]
    assert f1["fixed_ds1_best_a0_1e10_m_s2"] == ds1_row["profiled_a0_1e10_m_s2"]
    assert f1["joint_best_ds"] == 0.94
    assert f1["delta_chi2_ds075_vs_ds1"] > 50.0
    assert f2["delta_BIC_coord_fractal_vs_ds1"] > 400.0
    assert f3["cosmic_efe_95CL_upper_bound_gext_over_a0"] <= 0.025

    cert3 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE3-EMPIRICAL/1.1",
        "datasets": {
            "sparc_rar_source": "Lelli, McGaugh, Schombert & Pawlowski (2017, ApJ 836, 152), RARbins.mrt (14 bins, 2,630 points)",
            "kids_wl_source": "Mistele, McGaugh, Lelli, Schombert & Li (2024, ApJL 969, L3; arXiv:2406.09685, Sec. II & Table 2)",
            "kids_isolated_lens_counts_by_mass_bin": KIDS_ISOLATED_LENS_COUNTS_BY_BIN,
            "kids_isolated_lens_total": sum(KIDS_ISOLATED_LENS_COUNTS_BY_BIN),
            "hubble_constant_convention_note": (
                "Mistele et al. (2024) adopt H0 = 73.0 km/s/Mpc for lens distances and stellar masses, "
                "whereas Planck 2018 H0 = 67.4 km/s/Mpc is used when evaluating a_dS = c*H0/(2*pi) elsewhere."
            ),
        },
        "fit_1_sparc_rar_14_bins": f1,
        "fit_2_btfr_sparc_and_kids": f2,
        "fit_3_cosmic_efe_bound": f3,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave3_empirical_certificates.json"
    emit_or_verify(cert3, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
