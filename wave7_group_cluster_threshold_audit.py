"""
Foundation-0 / gravity -- Wave-7 Empirical Group & Cluster Threshold Fit (C-21, C-22; M-06)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
"""

from __future__ import annotations
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

G = 6.67430e-11
C = 299792458.0
K_B_KEV_J = 1.602176634e-16
M_P = 1.67262192369e-27
MU_ICM = 0.60
M_SUN = 1.98847e30
PC = 3.085677581491367e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
A0_EMP = 1.20e-10
PHI_CRIT_C2_W6 = 8.0e-6
SIGMA_CRIT_W6_KMS = (C * math.sqrt(PHI_CRIT_C2_W6 / (2.0 * (1.0 + math.log(4.0))))) / 1.0e3
COSMIC_OMEGA_M_OVER_B = 0.315 / 0.0493


def tx_to_sigma(tx_kev: float) -> float:
    return math.sqrt((tx_kev * K_B_KEV_J) / (MU_ICM * M_P)) / 1.0e3


def build_catalog() -> list[dict]:
    rows: list[dict] = []
    gal = [
        ("KiDS_Bin1", 131.6, 129.8, 0.045, "Mistele2024_KiDS_WL"),
        ("KiDS_Bin2", 169.4, 171.2, 0.035, "Mistele2024_KiDS_WL"),
        ("KiDS_Bin3", 214.5, 216.1, 0.030, "Mistele2024_KiDS_WL"),
        ("KiDS_Bin4", 269.0, 267.8, 0.035, "Mistele2024_KiDS_WL"),
        ("SPARC_220", 220.0, 220.0, 0.013, "SPARC_HSB"),
        ("SPARC_285", 285.0, 283.7, 0.016, "SPARC_HSB"),
    ]
    def add(name: str, cat: str, sig: float, rm: float, sx: float, sy: float, cov: float) -> None:
        rows.append({"name": name, "cat": cat, "sig": round(sig, 2), "R": round(rm, 4),
                     "logR": round(math.log10(rm), 5), "sx": round(sx, 4), "sy": round(sy, 4), "cov": cov})
    for name, vo, vm, ferr, cat in gal:
        add(name, cat, vo / math.sqrt(2.0), (vo / vm) ** 4, 0.012, 4.0 * ferr / math.log(10.0), 0.0)

    opt56 = [
        ("NGC5746", 39, 107.0, 0.36), ("NGC4697", 37, 109.0, 0.39), ("NGC3100", 34, 142.0, 0.43),
        ("NGC4636", 32, 73.0, 0.30), ("NGC3607", 31, 124.0, 0.83), ("NGC4501", 31, 199.0, 1.73),
        ("NGC3031", 30, 138.0, 3.20), ("NGC1553", 29, 185.0, 2.40), ("NGC4105", 29, 139.0, 1.16),
        ("NGC4631", 28, 90.0, 0.63), ("NGC3379", 27, 193.0, 5.20), ("NGC3923", 26, 159.0, 1.94),
        ("ESO507", 26, 130.0, 0.43), ("NGC5078", 26, 138.0, 0.71), ("NGC1407", 25, 167.0, 2.42),
        ("NGC1395", 24, 121.0, 0.80), ("NGC4039", 23, 74.0, 0.12), ("NGC4303", 23, 115.0, 0.99),
        ("NGC4535", 23, 121.0, 0.48), ("NGC4753", 23, 98.0, 0.72), ("NGC0988", 22, 103.0, 0.40),
        ("NGC1332", 22, 183.0, 4.00), ("NGC7176", 22, 139.0, 0.84), ("NGC4373", 21, 149.0, 0.70),
        ("NGC5322", 21, 169.0, 3.75), ("NGC3877", 21, 65.0, 0.20), ("NGC3894", 21, 123.0, 0.73),
        ("NGC2911", 21, 144.0, 1.93), ("NGC4111", 20, 93.0, 0.69), ("NGC5011", 20, 131.0, 0.62),
        ("NGC5557", 20, 141.0, 1.02), ("NGC3610", 19, 119.0, 1.06), ("NGC6868", 19, 182.0, 1.52),
        ("NGC0891", 18, 60.0, 0.08), ("NGC4527", 18, 85.0, 0.50), ("NGC5473", 18, 94.0, 0.56),
        ("NGC0488", 17, 85.0, 0.10), ("ESO320", 17, 150.0, 1.25), ("NGC5363", 17, 143.0, 3.49),
        ("NGC4321", 17, 165.0, 2.64), ("NGC0524", 16, 147.0, 0.96), ("NGC3627", 16, 154.0, 2.64),
        ("NGC3945", 16, 92.0, 0.48), ("NGC4125g", 16, 85.0, 0.31), ("NGC4151", 16, 69.0, 0.27),
        ("NGC4254", 16, 92.0, 0.75), ("NGC4666", 16, 98.0, 0.67), ("NGC4936", 16, 194.0, 2.91),
        ("NGC5090", 16, 218.0, 2.79), ("NGC5982", 16, 159.0, 1.22), ("NGC3801", 15, 82.0, 0.16),
        ("NGC4224", 15, 118.0, 1.15), ("NGC4258", 15, 80.0, 0.56), ("NGC4993", 15, 74.0, 0.14),
        ("NGC5128", 15, 94.0, 0.61), ("NGC5198", 15, 101.0, 0.91),
    ]
    for name, nv, sig, mmlk in opt56:
        add(name, "Milgrom2019_opt", sig, mmlk / 0.80, math.sqrt(1.0 / (2.0 * (nv - 1.0)) + 0.12 ** 2) / math.log(10.0), 0.18, 4.0)

    rich10 = [
        ("NGC4472*", 355, 291.0, 3.29), ("NGC3311*", 139, 426.0, 12.87), ("NGC4696*", 116, 303.0, 3.37),
        ("NGC1316*", 111, 244.0, 2.25), ("NGC4261*", 87, 276.0, 7.51), ("NGC5846*", 74, 228.0, 5.42),
        ("NGC3992*", 72, 120.0, 0.55), ("NGC5371*", 55, 195.0, 1.56), ("NGC3223*", 53, 404.0, 24.98),
        ("NGC5044*", 52, 245.0, 5.00),
    ]
    for name, nv, sig, mmlk in rich10:
        add(name, "Milgrom2019_rich", sig, mmlk / (0.80 + 1.60 * min(1.0, max(0.0, (sig - 180.0) / 220.0))),
            math.sqrt(1.0 / (2.0 * (nv - 1.0)) + 0.10 ** 2) / math.log(10.0), 0.20, 4.0)

    ang23 = [
        ("NGC4125_X", 0.50, 0.39, 0.26), ("NGC5129", 0.80, 1.70, 1.00), ("RGH80", 0.90, 2.20, 1.20),
        ("NGC4325", 0.90, 3.30, 2.50), ("NGC5044_X", 1.00, 3.70, 2.70), ("NGC2563", 1.20, 1.90, 1.40),
        ("NGC533", 1.20, 2.50, 1.60), ("NGC1550", 1.30, 3.90, 3.00), ("MS0116", 1.40, 9.70, 6.60),
        ("ESO552", 2.00, 14.90, 8.60), ("A2717", 2.20, 21.80, 8.40), ("AWM4", 2.40, 24.90, 13.60),
        ("A1991", 2.60, 36.20, 22.20), ("ESO306", 2.80, 21.70, 14.00), ("A2589", 3.30, 44.20, 12.10),
        ("A0133", 4.10, 140.0, 100.0), ("A0383_X", 4.80, 108.0, 75.5), ("A0907", 6.00, 167.0, 89.8),
        ("A1795", 6.10, 106.0, 66.8), ("A1413", 7.40, 430.0, 310.0), ("A0478_X", 7.90, 336.0, 175.0),
        ("A2029_X", 8.50, 331.0, 230.0), ("A2390_X", 8.90, 842.0, 555.0),
    ]
    for name, tx, mm, mdm in ang23:
        add(name, "Angus2008_Xray", tx_to_sigma(tx), 1.70 if name == "NGC4125_X" else mm / (mm - mdm), 0.020, 0.14, 2.0)
    for name, a, b in [("RXJ1159", (1.60, 10.7, 7.2), (1.80, 33.8, 21.0)),
                       ("MKW4", (1.90, 7.2, 4.6), (1.60, 15.2, 5.9)), ("A0262", (2.10, 21.3, 13.6), (2.40, 12.6, 6.8))]:
        add(name, "Angus2008_Xray", tx_to_sigma(0.5 * (a[0] + b[0])),
            math.sqrt((a[1] / (a[1] - a[2])) * (b[1] / (b[1] - b[2]))), 0.020, 0.14, 2.0)

    def wl_core_r(z: float, m200_1e14: float) -> float:
        hz = (72.0e3 / MPC) * math.sqrt(0.30 * ((1.0 + z) ** 3) + 0.70)
        rc = 3.0 * (hz ** 2) / (8.0 * math.pi * G)
        m200 = m200_1e14 * 1.0e14 * M_SUN
        r200 = ((3.0 * m200) / (4.0 * math.pi * 200.0 * rc)) ** (1.0 / 3.0)
        c200 = 5.71 * ((m200 / ((2.0e12 / 0.72) * M_SUN)) ** (-0.084)) * ((1.0 + z) ** (-0.47))
        rs = r200 / c200
        rm = 250.0 * KPC
        x = rm / rs
        mnfw = m200 * (math.log(1.0 + x) - x / (1.0 + x)) / (math.log(1.0 + c200) - c200 / (1.0 + c200))
        gn = G * mnfw / (rm ** 2)
        lo, hi = 1.0e-14, 10.0 * gn
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if mid / (1.0 - math.exp(-math.sqrt(mid / A0_EMP))) < gn:
                lo = mid
            else:
                hi = mid
        return (0.5 * (lo + hi)) / (0.130 * gn)

    ket28 = [
        ("XID210020", 0.100, 1.65, 0.30, 1.06, 1.10), ("XID110850", 0.237, 2.39, 0.70, 4.82, 2.23),
        ("XID110090", 0.159, 3.62, 0.79, 2.81, 1.61), ("XID110860", 0.204, 3.87, 1.19, 2.30, 1.54),
        ("XID210740", 0.314, 4.59, 1.57, 6.61, 3.19), ("XID210010", 0.189, 4.88, 0.62, 9.92, 3.06),
        ("XID111180", 0.185, 5.00, 0.61, 11.81, 2.89), ("XID210910", 0.316, 5.04, 2.42, 12.94, 6.91),
        ("XID210630", 0.368, 5.31, 2.48, 3.52, 4.58), ("XID210970", 0.459, 5.35, 1.18, 13.72, 7.13),
        ("XID110460", 0.270, 7.25, 3.19, 10.78, 3.76), ("XID102760", 0.470, 8.20, 5.55, 7.80, 4.68),
        ("Abell2597", 0.0852, 3.58, 0.07, 4.432, 1.656), ("Abell2244", 0.0989, 5.37, 0.12, 4.678, 3.543),
        ("MACSJ1731", 0.3890, 5.87, 0.61, 32.977, 5.906), ("Abell963", 0.2060, 6.08, 0.30, 6.623, 2.365),
        ("Abell2261", 0.2240, 6.10, 0.32, 21.246, 4.090), ("Abell521", 0.2475, 6.21, 0.28, 11.680, 2.803),
        ("Abell85", 0.0557, 6.45, 0.10, 7.240, 1.968), ("Abell2218", 0.1710, 6.97, 0.37, 7.697, 2.047),
        ("Abell520", 0.2030, 7.23, 0.23, 8.343, 1.925), ("Abell68", 0.2546, 7.56, 0.97, 13.254, 2.294),
        ("Abell209", 0.2060, 8.23, 0.66, 17.559, 2.993), ("Abell2204", 0.1511, 8.55, 0.58, 23.197, 4.283),
        ("Abell1689", 0.1832, 9.15, 0.35, 16.843, 2.429), ("Abell2142", 0.0904, 10.04, 0.26, 12.457, 2.095),
        ("MACSJ1206", 0.4390, 10.71, 1.29, 15.813, 3.580), ("MACSJ2211", 0.3960, 13.97, 2.74, 19.434, 4.164),
    ]
    for name, z, tx, etx, m200, em200 in ket28:
        ewl = 0.5 * abs(math.log10(wl_core_r(z, m200 + 0.5 * em200)) - math.log10(wl_core_r(z, max(0.20, m200 - 0.5 * em200))))
        add(name, "Kettula2015_WL", tx_to_sigma(tx), wl_core_r(z, m200), (0.5 * etx / tx) / math.log(10.0), math.sqrt(ewl ** 2 + 0.11 ** 2), 0.0)

    return sorted(rows, key=lambda d: d["sig"])


def odr_chi2(ds: list[dict], fn, cov_on: bool = True) -> dict:
    chi2 = 0.0
    sq = []
    for r in ds:
        xi, yi, sx, sy, a = math.log10(r["sig"]), r["logR"], r["sx"], r["sy"], r["cov"]
        if not cov_on or sx <= 1.0e-6:
            d = yi - fn(r["sig"])
            chi2 += (d * d) / (sy * sy + (a * sx) ** 2)
            sq.append(d * d)
        else:
            bq, br = 1.0e30, 0.0
            for k in range(-14, 15):
                u = xi + (k / 4.0) * sx
                dx = xi - u
                dy = (yi - a * dx) - fn(10.0 ** u)
                q = (dx / sx) ** 2 + (dy / sy) ** 2
                if q < bq:
                    bq, br = q, dy
            chi2 += bq
            sq.append(br * br)
    return {"chi2": round(chi2, 4), "rms_dex": round(math.sqrt(sum(sq) / len(sq)), 4), "n": len(ds)}


def pred_tf(s: float, sc: float, amp: float) -> float:
    return 0.0 if s <= sc else math.log10(1.0 + amp * (((s * s - sc * sc) / (1000.0 ** 2 - sc * sc)) ** 1.5))


def pred_cap(s: float, sc: float, sh: float, rsat: float) -> float:
    if s <= sc:
        return 0.0
    x3 = (s * s - sc * sc) ** 1.5
    return math.log10(1.0 + (rsat - 1.0) * (x3 / (x3 + (sh ** 3))))


def fit_sample(ds: list[dict], label: str) -> dict:
    n = len(ds)
    m0 = odr_chi2(ds, lambda _s: 0.0)
    m1b = min(
        ({**odr_chi2(ds, lambda s, a=i * 0.05: pred_tf(s, SIGMA_CRIT_W6_KMS, a)), "best_amp_at_1000": round(i * 0.05, 3)}
         for i in range(1, 160)),
        key=lambda d: d["chi2"],
    )
    m1b["bic"] = round(m1b["chi2"] + math.log(n), 4)

    m2 = min(
        ({**odr_chi2(ds, lambda s, _sh=float(ih), _rs=ir / 100.0: pred_cap(s, SIGMA_CRIT_W6_KMS, _sh, _rs)),
          "sigma_crit_kms_fixed": round(SIGMA_CRIT_W6_KMS, 2), "sigma_half_kms": float(ih), "R_sat": ir / 100.0}
         for ih in range(20, 480, 20) for ir in range(240, 460, 10)),
        key=lambda d: d["chi2"],
    )
    m2["bic"] = round(m2["chi2"] + 2.0 * math.log(n), 4)

    prof = []
    best_m3 = None
    for sc in range(150, 525, 5):
        bsc = min(
            ({**odr_chi2(ds, lambda s, _sc=float(sc), _sh=float(ih), _rs=ir / 100.0: pred_cap(s, _sc, _sh, _rs)),
              "sigma_crit_kms": float(sc), "sigma_half_kms": float(ih),
              "sigma_50pct_midpoint_kms": round(math.sqrt(float(sc) ** 2 + float(ih) ** 2), 2), "R_sat": ir / 100.0}
             for ih in range(40, 340, 20) for ir in range(260, 460, 10)),
            key=lambda d: d["chi2"],
        )
        prof.append((float(sc), bsc["chi2"]))
        if best_m3 is None or bsc["chi2"] < best_m3["chi2"]:
            best_m3 = bsc

    cmin = best_m3["chi2"]
    ci95 = [sc for sc, c2 in prof if c2 <= cmin + 4.0]
    best_m3["bic"] = round(cmin + 3.0 * math.log(n), 4)
    best_m3["ci_95pct_sigma_crit_kms"] = [min(ci95), max(ci95)]
    best_m3["delta_chi2_vs_M0_pure_MOND"] = round(m0["chi2"] - cmin, 3)
    best_m3["delta_chi2_vs_M1b_unbounded_TF"] = round(m1b["chi2"] - cmin, 3)
    best_m3["delta_chi2_wave6_388kms_vs_best"] = round(m2["chi2"] - cmin, 3)
    return {
        "sample_label": label,
        "n_systems": n,
        "M0_universal_a0_MOND": m0,
        "M1b_unbounded_TF_best_amp": m1b,
        "M2_wave6_388kms_supply_capped": m2,
        "M3_profiled_3param_supply_capped": best_m3,
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
    all_rows = build_catalog()
    w_150_1200 = [r for r in all_rows if 150.0 <= r["sig"] <= 1200.0]
    clean_60 = [r for r in all_rows if r["cat"] not in ("Milgrom2019_opt", "Milgrom2019_rich")]
    assert len(all_rows) == 126 and len(w_150_1200) == 77 and len(clean_60) == 60

    fit_prim = fit_sample(w_150_1200, "Primary_150_to_1200_kms_Covariant_ODR")
    fit_full = fit_sample(all_rows, "Full_60_to_1494_kms_Covariant_ODR")
    fit_clean = fit_sample(clean_60, "Zero_Sigma4_Covariance_WL_Xray_SPARC_60")

    bins = []
    for lbl, lo, hi in [
        ("60-150_kms", 60.0, 150.0), ("150-230_kms", 150.0, 230.0), ("230-390_kms", 230.0, 390.0),
        ("390-600_kms", 390.0, 600.0), ("600-900_kms", 600.0, 900.0), ("900-1200_kms", 900.0, 1200.0),
        ("1200-1500_kms", 1200.0, 1500.0),
    ]:
        sub = [r for r in all_rows if lo <= r["sig"] < hi]
        w_num = sum(r["logR"] / (r["sy"] ** 2 + (r["cov"] * r["sx"]) ** 2) for r in sub)
        w_den = sum(1.0 / (r["sy"] ** 2 + (r["cov"] * r["sx"]) ** 2) for r in sub)
        bins.append({
            "bin": lbl, "count": len(sub),
            "median_R_MOND": round(statistics.median([r["R"] for r in sub]), 3),
            "ivar_mean_R_MOND": round(10.0 ** (w_num / w_den), 3),
        })

    m3p = fit_prim["M3_profiled_3param_supply_capped"]
    m3c = fit_clean["M3_profiled_3param_supply_capped"]
    assert m3p["delta_chi2_vs_M0_pure_MOND"] > 200.0
    assert m3p["delta_chi2_vs_M1b_unbounded_TF"] > 15.0

    cert7 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE7-EMPIRICAL-THRESHOLD/1.1",
        "epistemic_status": "EMPIRICAL-FIT (3-PARAMETER HILL SATURATION CURVE ON PUBLISHED GROUP/CLUSTER DATA)",
        "caveat": (
            "Phenomenological 3-parameter fit (sigma_crit, sigma_half, R_sat) to the known MOND "
            "cluster residual mass discrepancy (Sanders 2003; Angus et al. 2008; Milgrom 2019). "
            "Single-zone sharp onset at 388.1 km/s is disfavored relative to gradual onset starting "
            "around ~190-200 km/s (delta_chi2 = 10.6 on zero-covariance WL+X-ray+SPARC subset), "
            "while unbounded Thomas-Fermi scaling without saturation fails above ~900 km/s."
        ),
        "dataset_counts": {
            "total_systems": len(all_rows),
            "primary_150_to_1200_kms": len(w_150_1200),
            "zero_sigma4_cov_wl_xray_sparc": len(clean_60),
            "kids_isolated_lenses_in_4_galaxy_bins": 129027,
        },
        "regime_binned_summary": bins,
        "model_fits": {
            "primary_150_to_1200_kms": fit_prim,
            "full_60_to_1494_kms": fit_full,
            "zero_cov_wl_xray_sparc": fit_clean,
        },
        "summary_metrics": {
            "wave6_apriori_single_zone_sigma_crit_kms": round(SIGMA_CRIT_W6_KMS, 2),
            "primary_fitted_sigma_crit_kms": m3p["sigma_crit_kms"],
            "primary_fitted_sigma_50pct_midpoint_kms": m3p["sigma_50pct_midpoint_kms"],
            "zero_cov_fitted_sigma_crit_kms": m3c["sigma_crit_kms"],
            "zero_cov_fitted_sigma_50pct_midpoint_kms": m3c["sigma_50pct_midpoint_kms"],
            "fitted_core_plateau_R_sat_250kpc": m3p["R_sat"],
            "planck2018_cosmic_Omega_m_over_Omega_b": round(COSMIC_OMEGA_M_OVER_B, 4),
        },
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave7_group_cluster_certificates.json"
    emit_or_verify(cert7, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
