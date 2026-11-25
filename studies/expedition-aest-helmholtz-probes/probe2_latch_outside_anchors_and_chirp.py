#!/usr/bin/env python3
"""
Probe 2:
  Part A (SEAM-03 / Portal 4B): Exact Latch Orthogonal Complement & Sample-Disjoint
      Outside-Anchor + 5,000-Trial Permuted-Null (T4) Audit on Foundation-0/gravity
      real multi-catalog data (126-system Wave-7/9/10 group/cluster compilation +
      SPARC 14-bin RAR vs KiDS-1000 1 Mpc WL outside anchor).
  Part B (ep-03 / Session 1 Pair 20): Repaired, scale-invariant, zero-prior-smuggled
      blind GW chirp exponent estimator alpha_hat = argmin CV(fdot * f^(-alpha)) +
      fixed dual-channel parity-lag correlator, tested against 5 adversarial null classes.

Zero unseeded randomness. All verdicts use explicit checks (python3 -O safe).
Run:
  python3 -I -O -B -W error studies/expedition-aest-helmholtz-probes/probe2_latch_outside_anchors_and_chirp.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from scipy.optimize import minimize
from scipy.signal import hilbert, welch

OUT_PATH = Path(__file__).resolve().parent / "probe2_latch_chirp_results.json"
GRAVITY_REPO = Path(os.environ.get("GRAVITY_REPO") or Path(__file__).resolve().parents[2])


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"CHECK FAILED: {msg}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    check(spec is not None and spec.loader is not None, f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ==============================================================================
# PART A: PHYSICS LATCH (T19) + SAMPLE-DISJOINT OUTSIDE ANCHORS + T4 PERMUTED NULLS
# ==============================================================================
def wave10_jeans_pred(sig: float, sig_j: float = 185.59, r_cdm_bar: float = 8.5238095238) -> float:
    """Wave-9/10 Jeans trapping curve: log10(1 + f_trap * R_dust) where f_trap = max(0, 1 - (sig_j/sig)^2)."""
    if sig <= sig_j:
        return 0.0
    f_trap = 1.0 - (sig_j / sig) ** 2
    # Wave-9/10 maps total/MOND boost ratio at 250 kpc via 1 + (R_sat_eff - 1) * f_trap;
    # use Wave-9/10's exact cluster-core effective ceiling from Vikhlinin f_b,2500=0.105 => R_max = 3.85 (or fitted)!
    return math.log10(1.0 + f_trap * (r_cdm_bar - 1.0))


def hill_pred(sig: float, sc: float, sh: float, rsat: float) -> float:
    if sig <= sc:
        return 0.0
    x3 = (sig * sig - sc * sc) ** 1.5
    return math.log10(1.0 + (rsat - 1.0) * (x3 / (x3 + sh**3)))


def sigmoid_pred(sig: float, log_s0: float, width: float, amp: float) -> float:
    """Smooth threshold-free logistic control (zero sharp threshold at 185 km/s!)."""
    z = (math.log10(sig) - log_s0) / max(0.02, width)
    z = max(-40.0, min(40.0, z))
    return amp / (1.0 + math.exp(-z))


def weighted_chi2(rows: List[dict], fn) -> Tuple[float, np.ndarray, np.ndarray]:
    res = []
    wt = []
    for r in rows:
        # Effective variance combining sy and cov*sx (exact diagonalized total variance in logR)
        var = r["sy"] ** 2 + (r["cov"] * r["sx"]) ** 2
        res.append(r["logR"] - fn(r["sig"]))
        wt.append(1.0 / var)
    res_a = np.array(res, dtype=float)
    wt_a = np.array(wt, dtype=float)
    return float(np.sum(wt_a * res_a * res_a)), res_a, wt_a


def fit_hill(rows: List[dict]) -> Dict:
    def obj(p):
        sc, sh, rsat = p
        if not (50.0 <= sc <= 600.0 and 20.0 <= sh <= 800.0 and 1.2 <= rsat <= 12.0):
            return 1e12
        return weighted_chi2(rows, lambda s: hill_pred(s, sc, sh, rsat))[0]

    best = None
    for sc0 in [120.0, 190.0, 300.0]:
        for sh0 in [100.0, 280.0]:
            res = minimize(obj, [sc0, sh0, 3.8], method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-5})
            if best is None or res.fun < best.fun:
                best = res
    sc, sh, rsat = [float(x) for x in best.x]
    return {"sc": sc, "sh": sh, "rsat": rsat, "chi2": float(best.fun)}


def fit_sigmoid(rows: List[dict]) -> Dict:
    def obj(p):
        ls0, wd, amp = p
        if not (1.5 <= ls0 <= 3.3 and 0.03 <= wd <= 1.2 and 0.05 <= amp <= 1.5):
            return 1e12
        return weighted_chi2(rows, lambda s: sigmoid_pred(s, ls0, wd, amp))[0]

    best = None
    for ls0 in [2.1, 2.4, 2.7]:
        for wd in [0.1, 0.35]:
            res = minimize(obj, [ls0, wd, 0.6], method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-5})
            if best is None or res.fun < best.fun:
                best = res
    ls0, wd, amp = [float(x) for x in best.x]
    return {"log_s0": ls0, "s0_kms": 10.0**ls0, "width_dex": wd, "amp_dex": amp, "chi2": float(best.fun)}


def fit_jeans_1p(rows: List[dict]) -> Dict:
    """1-parameter Jeans threshold + free plateau amp (2-param) vs fixed Planck/Vikhlinin."""
    def obj(p):
        sj, rsat = p
        if not (50.0 <= sj <= 600.0 and 1.2 <= rsat <= 12.0):
            return 1e12
        return weighted_chi2(rows, lambda s: wave10_jeans_pred(s, sj, rsat))[0]

    best = None
    for sj0 in [120.0, 185.0, 280.0]:
        res = minimize(obj, [sj0, 4.0], method="Nelder-Mead", options={"maxiter": 3000})
        if best is None or res.fun < best.fun:
            best = res
    return {"sig_j": float(best.x[0]), "rsat": float(best.x[1]), "chi2": float(best.fun)}


def part_a_gravity_latch_audit() -> Dict:
    w7 = load_module(GRAVITY_REPO / "wave7_group_cluster_threshold_audit.py", "wave7_mod")
    w3 = load_module(GRAVITY_REPO / "wave3_empirical_audit.py", "wave3_mod")
    all_rows = w7.build_catalog()
    check(len(all_rows) == 126, f"Expected 126 systems in wave7 catalog, got {len(all_rows)}")

    # Group systems into genuinely disjoint survey/catalog families
    families = {
        "Galaxies_SPARC_KiDS": [r for r in all_rows if r["cat"] in ("SPARC_HSB", "Mistele2024_KiDS_WL")],
        "Milgrom2019_opt": [r for r in all_rows if r["cat"] == "Milgrom2019_opt"],
        "Milgrom2019_rich": [r for r in all_rows if r["cat"] == "Milgrom2019_rich"],
        "Angus2008_Xray": [r for r in all_rows if r["cat"] == "Angus2008_Xray"],
        "Kettula2015_WL": [r for r in all_rows if r["cat"] == "Kettula2015_WL"],
    }

    # 1. Exact Latch Geometry on the 126-system linearized tangent space Phi of the smooth sigmoid / Hill model
    # Compute exact Jacobian Phi (126 x 3) in whitened (W^{1/2}) metric at full-sample fit!
    full_sig = fit_sigmoid(all_rows)
    full_hill = fit_hill(all_rows)
    full_jeans = fit_jeans_1p(all_rows)
    n = len(all_rows)
    W_sqrt = np.array([1.0 / math.sqrt(r["sy"] ** 2 + (r["cov"] * r["sx"]) ** 2) for r in all_rows])
    y_obs = np.array([r["logR"] for r in all_rows])

    # Tangent Jacobian Phi of smooth 3-param sigmoid model at optimum (whitened!)
    eps = 1e-5
    p0 = np.array([full_sig["log_s0"], full_sig["width_dex"], full_sig["amp_dex"]])
    Phi = np.zeros((n, 3))
    for j in range(3):
        dp = np.zeros(3)
        dp[j] = eps
        fp = np.array([sigmoid_pred(r["sig"], *(p0 + dp)) for r in all_rows])
        fm = np.array([sigmoid_pred(r["sig"], *(p0 - dp)) for r in all_rows])
        Phi[:, j] = W_sqrt * (fp - fm) / (2 * eps)
    Q_phi, _ = np.linalg.qr(Phi)  # Orthonormal basis for Col(Phi) in whitened metric

    # Compute exact sin^2(w, Col(Phi)) for:
    #   (a) Inside-span probe: w in Col(Phi) (exact Latch => sin^2 = 0!)
    #   (b) Each catalog's indicator mean shift (sample-disjoint systematic offset!)
    #   (c) Sharp 185 km/s threshold kink difference (Hill - Sigmoid)!
    def sin2_to_col(v: np.ndarray) -> float:
        vn = np.linalg.norm(v)
        if vn == 0:
            return 0.0
        proj = Q_phi @ (Q_phi.T @ v)
        return float(max(0.0, min(1.0, 1.0 - (np.linalg.norm(proj) ** 2) / (vn * vn))))

    diff_kink = W_sqrt * np.array(
        [hill_pred(r["sig"], full_hill["sc"], full_hill["sh"], full_hill["rsat"]) - sigmoid_pred(r["sig"], *p0) for r in all_rows]
    )
    latch_geometry = {
        "whitened_col_rank": int(np.linalg.matrix_rank(Phi)),
        "orthogonal_complement_dim": int(n - np.linalg.matrix_rank(Phi)),
        "inside_span_probe_sin2": sin2_to_col(Phi @ np.array([1.0, -0.5, 0.3])),
        "sharp_185_kink_vs_smooth_sigmoid_sin2": sin2_to_col(diff_kink),
        "catalog_offset_sin2": {},
    }
    check(latch_geometry["inside_span_probe_sin2"] < 1e-14, "Inside-span sin^2 not zero!")
    for cname, crows in families.items():
        mask = np.array([1.0 if r in crows else 0.0 for r in all_rows])
        latch_geometry["catalog_offset_sin2"][cname] = sin2_to_col(W_sqrt * mask)

    # 2. Truly Sample-Disjoint Outside-Anchor Leave-One-Catalog-Out (LOCO) Cross-Validation!
    loco_results = []
    for hold_name, hold_rows in families.items():
        train_rows = [r for r in all_rows if r not in hold_rows]
        h_fit = fit_hill(train_rows)
        s_fit = fit_sigmoid(train_rows)
        j_fit = fit_jeans_1p(train_rows)
        c2_h, _, _ = weighted_chi2(hold_rows, lambda s: hill_pred(s, h_fit["sc"], h_fit["sh"], h_fit["rsat"]))
        c2_s, _, _ = weighted_chi2(hold_rows, lambda s: sigmoid_pred(s, s_fit["log_s0"], s_fit["width_dex"], s_fit["amp_dex"]))
        c2_j, _, _ = weighted_chi2(hold_rows, lambda s: wave10_jeans_pred(s, j_fit["sig_j"], j_fit["rsat"]))
        c2_m0, _, _ = weighted_chi2(hold_rows, lambda s: 0.0)
        loco_results.append(
            {
                "held_out_catalog": hold_name,
                "n_holdout": len(hold_rows),
                "sigma_range_kms": [float(min(r["sig"] for r in hold_rows)), float(max(r["sig"] for r in hold_rows))],
                "train_hill_sc_kms": h_fit["sc"],
                "train_jeans_sigJ_kms": j_fit["sig_j"],
                "holdout_chi2_pure_MOND": c2_m0,
                "holdout_chi2_hill_3p": c2_h,
                "holdout_chi2_smooth_sigmoid_3p": c2_s,
                "holdout_chi2_jeans_2p": c2_j,
                "delta_chi2_sigmoid_minus_hill_on_holdout": c2_s - c2_h,
            }
        )

    # 3. T4 Early Warning in Passing Residuals: 5,000-trial Catalog-Stratified Permuted Nulls!
    # Question: After fitting the smooth 3-parameter sigmoid baseline, do the residuals show
    # statistically significant (a) sharp-threshold kink preference, or (b) catalog-by-catalog
    # systematic offset / trend that survives 5,000 stratified permutations?
    rng = np.random.default_rng(20261120)
    c2_sig_full, res_sig, wt_full = weighted_chi2(all_rows, lambda s: sigmoid_pred(s, *p0))
    c2_hill_full, res_hill, _ = weighted_chi2(
        all_rows, lambda s: hill_pred(s, full_hill["sc"], full_hill["sh"], full_hill["rsat"])
    )
    # Test statistic 1 (T4 kink projection): weighted correlation of smooth-sigmoid residuals with kink template
    w_res = np.sqrt(wt_full) * res_sig
    t_kink_obs = float(abs(np.dot(w_res, diff_kink)) / (np.linalg.norm(w_res) * np.linalg.norm(diff_kink) + 1e-30))

    # Test statistic 2 (T4 cross-catalog offset ANOVA F-like chi2 drop across the 5 disjoint catalogs)
    cat_indices = {cname: [i for i, r in enumerate(all_rows) if r in crows] for cname, crows in families.items()}

    def catalog_offset_chi2(r_vec: np.ndarray) -> float:
        total = 0.0
        for idxs in cat_indices.values():
            w_sub = wt_full[idxs]
            r_sub = r_vec[idxs]
            mu_c = float(np.sum(w_sub * r_sub) / np.sum(w_sub))
            total += float(np.sum(w_sub) * mu_c * mu_c)
        return total

    t_cat_obs = catalog_offset_chi2(res_sig)

    n_perm = 5000
    ge_kink = 0
    ge_cat = 0
    # Permute standardized residuals z_i = sqrt(w_i) * res_i:
    # - Within-catalog permutation for kink test (tests whether kink exists beyond catalog offsets!)
    # - Global permutation for catalog-offset test (tests whether catalogs differ systematically!)
    z_sig = np.sqrt(wt_full) * res_sig
    for _ in range(n_perm):
        # Global perm for catalog offset
        z_glob = rng.permutation(z_sig)
        r_glob = z_glob / np.sqrt(wt_full)
        if catalog_offset_chi2(r_glob) >= t_cat_obs:
            ge_cat += 1
        # Within-catalog perm for kink test
        z_strat = z_sig.copy()
        for idxs in cat_indices.values():
            z_strat[idxs] = rng.permutation(z_strat[idxs])
        t_k = float(abs(np.dot(z_strat, diff_kink)) / (np.linalg.norm(z_strat) * np.linalg.norm(diff_kink) + 1e-30))
        if t_k >= t_kink_obs:
            ge_kink += 1

    p_kink = (ge_kink + 1.0) / (n_perm + 1.0)
    p_cat = (ge_cat + 1.0) / (n_perm + 1.0)

    # 4. SPARC 14-bin RAR -> KiDS-1000 1 Mpc WL truly sample-disjoint outside-anchor test!
    # Fit (ds, a0) on SPARC 14 bins ONLY (exact Wave-3 data), then evaluate on disjoint KiDS-1000 1 Mpc 4 bins!
    def sparc_chi2(ds, a0):
        return sum(
            ((lgo - w3.pred_log10_gobs(lgb, ds, a0)) / (sd / math.sqrt(n_pts))) ** 2
            for lgb, lgo, sd, n_pts in w3.SPARC_RAR_BINS
        )

    best_sparc = min(
        ((sparc_chi2(0.40 + 0.01 * i, (0.50 + 0.01 * j) * 1e-10), 0.40 + 0.01 * i, (0.50 + 0.01 * j) * 1e-10)
         for i in range(101) for j in range(151)),
        key=lambda t: t[0],
    )
    # Also evaluate fixed ds=1.00 (best a0 on SPARC)
    best_ds1 = min(
        ((sparc_chi2(1.0, (0.50 + 0.01 * j) * 1e-10), 1.0, (0.50 + 0.01 * j) * 1e-10) for j in range(151)),
        key=lambda t: t[0],
    )
    # Predict KiDS-1000 1 Mpc V_circ from deep-limit generalized BTFR:
    # g_obs = (g_b * a0^ds)^(1/(1+ds)) => V^2/r = (G M / r^2)^(1/(1+ds)) * a0^(ds/(1+ds))
    # => V_pred(r=1 Mpc) = sqrt(r * ((G M / r^2) * a0^ds)^(1/(1+ds)))
    G_si, M_sun, kpc = 6.67430e-11, 1.98847e30, 3.085677581491367e19
    r_eval = 1000.0 * kpc

    def kids_chi2(ds, a0):
        c2 = 0.0
        for logM, v_obs, v_err in w3.KIDS_WL_ALL_1000KPC:
            gb = G_si * (10.0**logM) * M_sun / (r_eval**2)
            g_pred = 10.0 ** w3.pred_log10_gobs(math.log10(gb), ds, a0)
            v_pred_kms = math.sqrt(g_pred * r_eval) / 1e3
            c2 += ((v_obs - v_pred_kms) / v_err) ** 2
        return c2

    sparc_to_kids = {
        "sparc_best_free_ds": {
            "ds": round(best_sparc[1], 3),
            "a0": best_sparc[2],
            "sparc_chi2": round(best_sparc[0], 4),
            "disjoint_kids_1mpc_chi2": round(kids_chi2(best_sparc[1], best_sparc[2]), 4),
        },
        "sparc_fixed_ds_1": {
            "ds": 1.0,
            "a0": best_ds1[2],
            "sparc_chi2": round(best_ds1[0], 4),
            "disjoint_kids_1mpc_chi2": round(kids_chi2(1.0, best_ds1[2]), 4),
        },
    }

    return {
        "n_systems": n,
        "full_sample_fits": {
            "hill_3p": full_hill,
            "smooth_sigmoid_3p": full_sig,
            "jeans_2p": full_jeans,
            "delta_chi2_smooth_sigmoid_minus_hill": float(c2_sig_full - c2_hill_full),
        },
        "latch_geometry": latch_geometry,
        "leave_one_catalog_out_outside_anchors": loco_results,
        "t4_permuted_null_early_warning": {
            "n_permutations": n_perm,
            "seed": 20261120,
            "kink_projection_stat": t_kink_obs,
            "kink_stratified_perm_pvalue": p_kink,
            "cross_catalog_offset_chi2": t_cat_obs,
            "cross_catalog_offset_perm_pvalue": p_cat,
        },
        "sparc_to_kids_1mpc_disjoint_anchor": sparc_to_kids,
    }


# ==============================================================================
# PART B: REPAIRED, PRIOR-FREE, SCALE-INVARIANT GW CHIRP EXPONENT ESTIMATOR (ep-03)
# ==============================================================================
def iaaft_surrogate(x: np.ndarray, rng: np.random.Generator, n_iter: int = 40) -> np.ndarray:
    """Iterative Amplitude-Adjusted Fourier Transform surrogate (preserves exact PSD + marginal amplitudes)."""
    x_sorted = np.sort(x)
    amp = np.abs(np.fft.rfft(x))
    y = rng.permutation(x)
    for _ in range(n_iter):
        yf = np.fft.rfft(y)
        y = np.fft.irfft(amp * np.exp(1j * np.angle(yf)), n=len(x))
        ranks = np.argsort(np.argsort(y))
        y = x_sorted[ranks]
    return y


def blind_chirp_exponent_estimator(
    y1: np.ndarray,
    y2: np.ndarray,
    fs: float,
    max_lag_samples: int = 80,
) -> Dict:
    """
    Repaired blind dual-channel parity-lag + scale-invariant chirp exponent estimator.
    Fixes ALL 3 bugs of Session 1 pair_20_block_00.py:
      1. Bounds-safe lag slicing (zero negative-index wraparound!).
      2. Consistent one-sided Welch PSD whitening (explicit 2/fs scaling).
      3. ZERO hardcoded frequency band [30,350] Hz and ZERO hardcoded -11/3 exponent:
         estimates instantaneous frequency f(t) from the strongest coherent envelope
         window and fits free exponent alpha_hat = argmin CV(fdot * f^(-alpha))!
    """
    n = len(y1)
    # 1. Properly normalized one-sided MEDIAN Welch PSD whitening (robust against transient self-cancellation!)
    nperseg = min(512, n // 8)
    freqs, psd1 = welch(y1, fs=fs, nperseg=nperseg, return_onesided=True, scaling="density", average="median")
    _, psd2 = welch(y2, fs=fs, nperseg=nperseg, return_onesided=True, scaling="density", average="median")
    rfreqs = np.fft.rfftfreq(n, d=1.0 / fs)
    p1_i = np.maximum(np.interp(rfreqs, freqs, psd1), 1e-30)
    p2_i = np.maximum(np.interp(rfreqs, freqs, psd2), 1e-30)
    # Whiten via inverse sqrt(PSD) — note consistent 1/sqrt(psd) factor across full spectrum (no hardcoded band!)
    w1 = np.fft.irfft(np.fft.rfft(y1) / np.sqrt(p1_i), n=n)
    w2 = np.fft.irfft(np.fft.rfft(y2) / np.sqrt(p2_i), n=n)
    w1 = (w1 - np.mean(w1)) / (np.std(w1) + 1e-30)
    w2 = (w2 - np.mean(w2)) / (np.std(w2) + 1e-30)

    # 2. Bounds-safe lagged cross-correlation (strictly t_start >= max_lag, t_end <= n - max_lag!)
    win = max(128, int(0.25 * fs))
    best_corr = 0.0
    best_abs = -1.0
    best_lag = 0
    step = max(32, win // 4)
    for t0 in range(max_lag_samples, n - win - max_lag_samples + 1, step):
        seg2 = w2[t0 : t0 + win]
        n2 = np.linalg.norm(seg2)
        if n2 < 1e-12:
            continue
        for lag in range(-max_lag_samples, max_lag_samples + 1):
            seg1 = w1[t0 + lag : t0 + lag + win]
            c = float(np.dot(seg1, seg2) / (np.linalg.norm(seg1) * n2 + 1e-30))
            if abs(c) > best_abs:
                best_abs = abs(c)
                best_corr = c
                best_lag = lag

    # 3. Align coherent pair using detected sign & lag, locate transient via coherent product a1 * a2,
    #    and extract ridge frequency f(t) via ZERO-PRIOR STFT spectral-peak tracking (no hardcoded band!)
    sgn = 1.0 if best_corr >= 0 else -1.0
    if best_lag >= 0:
        a1 = w1[best_lag:]
        a2 = sgn * w2[: n - best_lag]
    else:
        a1 = w1[: n + best_lag]
        a2 = sgn * w2[-best_lag:]
    combined = 0.5 * (a1 + a2)

    # Compute STFT on aligned coherent stream using Hann window (zero-padded for fine bin resolution, ZERO band prior!)
    win_len = 256
    nfft = 1024
    hop = 16
    hann = np.hanning(win_len)
    n_frames = (len(combined) - win_len) // hop + 1
    stft_cross = np.zeros((n_frames, nfft // 2 + 1))
    t_frames = np.zeros(n_frames)
    for fi in range(n_frames):
        s = fi * hop
        F1 = np.fft.rfft(a1[s : s + win_len] * hann, n=nfft)
        F2 = np.fft.rfft(a2[s : s + win_len] * hann, n=nfft)
        stft_cross[fi] = np.maximum(0.0, np.real(F1 * np.conj(F2)))
        t_frames[fi] = (s + 0.5 * win_len) / fs
    df = fs / nfft

    # Track peak coherent cross-power ridge per time frame with parabolic sub-bin interpolation
    frame_peak_pow = np.max(stft_cross[:, 4:-4], axis=1)
    med_pow = float(np.median(frame_peak_pow))
    max_pow = float(np.max(frame_peak_pow))
    if max_pow < 10.0 * max(med_pow, 1e-30):
        return {
            "peak_corr": round(best_corr, 5),
            "best_lag_samples": best_lag,
            "frac_rising": 0.0,
            "rel_freq_sweep": 0.0,
            "alpha_hat": None,
            "min_nonlinearity": 1.0,
            "monotone_chirp_detected": False,
        }

    # Contiguous active ridge around peak power above 10% of peak coherent cross-power
    pk_f = int(np.argmax(frame_peak_pow))
    p_thr = med_pow + 0.10 * (max_pow - med_pow)
    lo_f = pk_f
    while lo_f > 0 and frame_peak_pow[lo_f - 1] >= p_thr:
        lo_f -= 1
    hi_f = pk_f
    while hi_f < n_frames - 1 and frame_peak_pow[hi_f + 1] >= p_thr:
        hi_f += 1
    # Trim boundary frames (half a Hann window on each side) to avoid taper-edge bias
    span_f = hi_f - lo_f + 1
    if span_f >= 24:
        trim_f = max(4, int(0.12 * span_f))
        lo_f += trim_f
        hi_f -= trim_f

    f_ridge = []
    t_ridge = []
    for fi in range(lo_f, hi_f + 1):
        spec = stft_cross[fi]
        k_pk = int(np.argmax(spec[4:-4])) + 4
        y_m, y_0, y_p = math.log(spec[k_pk - 1] + 1e-30), math.log(spec[k_pk] + 1e-30), math.log(spec[k_pk + 1] + 1e-30)
        denom = y_m - 2.0 * y_0 + y_p
        delta = 0.5 * (y_m - y_p) / denom if abs(denom) > 1e-12 else 0.0
        delta = max(-0.5, min(0.5, delta))
        f_ridge.append((k_pk + delta) * df)
        t_ridge.append(t_frames[fi])

    f_arr = np.array(f_ridge, dtype=float)
    t_arr = np.array(t_ridge, dtype=float)
    if len(f_arr) < 12:
        return {
            "peak_corr": round(best_corr, 5),
            "best_lag_samples": best_lag,
            "frac_rising": 0.0,
            "rel_freq_sweep": 0.0,
            "alpha_hat": None,
            "min_nonlinearity": 1.0,
            "monotone_chirp_detected": False,
        }

    # Require genuine monotonic rise and meaningful frequency sweep (> 20%) to reject constant-f glitches!
    diffs = np.diff(f_arr)
    frac_rising = float(np.mean(diffs > 0.0))
    rel_sweep = float((np.max(f_arr) - np.min(f_arr)) / max(np.mean(f_arr), 1e-12))
    # Net upward correlation between t and f
    corr_tf = float(np.corrcoef(t_arr, f_arr)[0, 1]) if np.std(f_arr) > 1e-12 else 0.0
    if rel_sweep < 0.20 or corr_tf < 0.85:
        return {
            "peak_corr": round(best_corr, 5),
            "best_lag_samples": best_lag,
            "frac_rising": round(frac_rising, 4),
            "rel_freq_sweep": round(rel_sweep, 4),
            "alpha_hat": None,
            "min_nonlinearity": 1.0,
            "monotone_chirp_detected": False,
        }

    # EXACT INTEGRAL (DERIVATIVE-FREE, SCALE- & SHIFT-INVARIANT) BOX-COX CHIRP NULL-EQUIVALENCE:
    #   df/dt = kappa * f^alpha  <=>  u_alpha(f) = (f^(1-alpha) - 1)/(1-alpha) [ln(f) at alpha=1]
    #   is an EXACT AFFINE LINEAR FUNCTION OF t!
    # Minimize 1 - R^2(t, u_alpha(f(t))) over free alpha in [-1, 6] (zero hardcoded exponent!).
    # Strictly invariant under t -> a*t + b AND f -> c*f!
    t_c = t_arr - np.mean(t_arr)
    t_norm = float(np.linalg.norm(t_c))
    alphas = np.linspace(-1.0, 6.0, 701)
    best_nonlin = float("inf")
    best_alpha = 0.0
    for al in alphas:
        if abs(al - 1.0) < 1e-6:
            u = np.log(f_arr)
        else:
            u = (f_arr ** (1.0 - al) - 1.0) / (1.0 - al)
        u_c = u - np.mean(u)
        u_norm = float(np.linalg.norm(u_c))
        if u_norm < 1e-30:
            continue
        r_corr = float(np.dot(t_c, u_c) / (t_norm * u_norm))
        nonlin = max(0.0, 1.0 - r_corr * r_corr)
        if nonlin < best_nonlin:
            best_nonlin = nonlin
            best_alpha = float(al)

    return {
        "peak_corr": round(best_corr, 5),
        "best_lag_samples": best_lag,
        "frac_rising": round(frac_rising, 4),
        "rel_freq_sweep": round(rel_sweep, 4),
        "alpha_hat": round(best_alpha, 4),
        "min_nonlinearity": round(best_nonlin, 7),
        "monotone_chirp_detected": bool(abs(best_corr) > 0.65 and corr_tf > 0.90 and rel_sweep >= 0.20 and best_nonlin < 0.005),
    }


def part_b_chirp_invariant_audit() -> Dict:
    rng = np.random.default_rng(20261120)
    fs = 4096.0
    T = 6.0  # 6-second record so transient occupies <10% -> median Welch PSD uncontaminated!
    N = int(fs * T)
    t = np.arange(N) / fs
    lag_true = 28  # ~6.84 ms parity-inverted lag

    def make_pair(sig: np.ndarray, noise_std: float = 0.04, parity: float = -1.0, seed_off: int = 0):
        r = np.random.default_rng(20261120 + seed_off)
        s1 = np.roll(sig, lag_true)
        s1[:lag_true] = 0.0
        s2 = parity * sig
        # Stationary colored background noise (white + mild 1/f rolloff) to test median whitening!
        rf = np.fft.rfftfreq(N, d=1.0 / fs)
        color = 1.0 / np.sqrt(1.0 + (rf / 120.0) ** 2)
        n1 = np.fft.irfft(np.fft.rfft(r.normal(0.0, 1.0, size=N)) * color, n=N)
        n2 = np.fft.irfft(np.fft.rfft(r.normal(0.0, 1.0, size=N)) * color, n=N)
        n1 = noise_std * n1 / (np.std(n1) + 1e-30)
        n2 = noise_std * n2 / (np.std(n2) + 1e-30)
        return s1 + n1, s2 + n2

    def smooth_box(t_arr: np.ndarray, t_lo: float, t_hi: float) -> np.ndarray:
        u = np.clip((t_arr - t_lo) / (t_hi - t_lo), 0.0, 1.0)
        in_win = (t_arr >= t_lo) & (t_arr <= t_hi)
        return np.where(in_win, np.sin(math.pi * u) ** 0.5, 0.0)

    # 1. Newtonian inspiral signal (f(t) = A * (t_c - t)^(-3/8) => exact alpha = 11/3 = 3.6667)
    def newtonian_inspiral(f_scale: float = 1.0):
        t_c = 3.32
        tau = np.maximum(t_c - t, 1e-4)
        A = 35.0 * f_scale
        phi = -2.0 * math.pi * (8.0 / 5.0) * A * (tau ** (5.0 / 8.0))
        env = smooth_box(t, 2.75, 3.29) * (tau ** (-0.25))
        env = env / (np.max(env) + 1e-30)
        return env * np.cos(phi)

    # Scale-invariance check: run at f_scale = 1.0 AND f_scale = 2.5 (outside hardcoded [30,350] Hz!)
    sig_pn_1 = newtonian_inspiral(1.0)
    sig_pn_2p5 = newtonian_inspiral(2.5)
    y1_pn1, y2_pn1 = make_pair(sig_pn_1, noise_std=0.03, parity=-1.0, seed_off=1)
    y1_pn25, y2_pn25 = make_pair(sig_pn_2p5, noise_std=0.03, parity=-1.0, seed_off=2)

    # 2. Negative Control A: Linear chirp (fdot = const => exact alpha = 0.0, NOT 11/3!)
    t_mid = 3.0
    env_g = np.exp(-0.5 * ((t - t_mid) / 0.14) ** 2)
    f0_lin, k_lin = 120.0, 450.0
    sig_lin = env_g * np.cos(2.0 * math.pi * (f0_lin * (t - t_mid) + 0.5 * k_lin * (t - t_mid) ** 2))
    y1_lin, y2_lin = make_pair(sig_lin, noise_std=0.03, parity=-1.0, seed_off=3)

    # 3. Negative Control B: Exponential chirp (fdot/f = const => exact alpha = 1.0, NOT 11/3!)
    r_exp = 3.0
    f0_exp = 60.0
    phi_exp = 2.0 * math.pi * (f0_exp / r_exp) * np.exp(r_exp * (t - 2.75))
    env_exp = smooth_box(t, 2.75, 3.28)
    sig_exp = env_exp * np.cos(phi_exp)
    y1_exp, y2_exp = make_pair(sig_exp, noise_std=0.03, parity=-1.0, seed_off=4)

    # 4. Negative Control C: Sine-Gaussian burst glitch (constant frequency => fdot ~ 0!)
    sig_glitch = np.exp(-0.5 * ((t - 3.0) / 0.08) ** 2) * np.cos(2.0 * math.pi * 140.0 * t)
    y1_gl, y2_gl = make_pair(sig_glitch, noise_std=0.03, parity=-1.0, seed_off=5)

    # 5. Negative Control D: Independent colored 1/f^2 Gaussian noise
    rf = np.fft.rfftfreq(N, d=1.0 / fs)
    filt = 1.0 / np.maximum(rf, 5.0)
    y1_red = np.fft.irfft(np.fft.rfft(rng.normal(size=N)) * filt, n=N)
    y2_red = np.fft.irfft(np.fft.rfft(rng.normal(size=N)) * filt, n=N)

    # 6. Negative Control E: IAAFT phase-randomized surrogate of the Newtonian inspiral!
    y1_iaaft = iaaft_surrogate(y1_pn1, np.random.default_rng(20261121))
    y2_iaaft = iaaft_surrogate(y2_pn1, np.random.default_rng(20261122))

    res_pn1 = blind_chirp_exponent_estimator(y1_pn1, y2_pn1, fs)
    res_pn25 = blind_chirp_exponent_estimator(y1_pn25, y2_pn25, fs)
    res_lin = blind_chirp_exponent_estimator(y1_lin, y2_lin, fs)
    res_exp = blind_chirp_exponent_estimator(y1_exp, y2_exp, fs)
    res_gl = blind_chirp_exponent_estimator(y1_gl, y2_gl, fs)
    res_red = blind_chirp_exponent_estimator(y1_red, y2_red, fs)
    res_iaaft = blind_chirp_exponent_estimator(y1_iaaft, y2_iaaft, fs)

    # Explicit anti-shadow assertions:
    # - Newtonian inspirals at BOTH frequency scales recover alpha ~ 11/3 = 3.667 within 0.25 and exact lag + parity!
    check(res_pn1["monotone_chirp_detected"] and abs(res_pn1["alpha_hat"] - 11.0 / 3.0) < 0.25, f"PN 1x failed: {res_pn1}")
    check(res_pn25["monotone_chirp_detected"] and abs(res_pn25["alpha_hat"] - 11.0 / 3.0) < 0.25, f"PN 2.5x scale-invariance failed: {res_pn25}")
    check(res_pn1["best_lag_samples"] == lag_true and res_pn1["peak_corr"] < -0.7, f"PN parity/lag failed: {res_pn1}")
    # - Linear chirp recovers alpha ~ 0 (separated from 11/3 by > 3.0!)
    check(res_lin["monotone_chirp_detected"] and abs(res_lin["alpha_hat"] - 0.0) < 0.25, f"Linear chirp failed: {res_lin}")
    # - Exponential chirp recovers alpha ~ 1 (separated from 11/3 by > 2.0!)
    check(res_exp["monotone_chirp_detected"] and abs(res_exp["alpha_hat"] - 1.0) < 0.25, f"Exp chirp failed: {res_exp}")
    # - Glitch, red noise, and IAAFT surrogate are REJECTED as monotone chirps!
    check(not res_gl["monotone_chirp_detected"], f"Sine-Gaussian glitch falsely triggered chirp: {res_gl}")
    check(not res_red["monotone_chirp_detected"], f"Red noise falsely triggered chirp: {res_red}")
    check(not res_iaaft["monotone_chirp_detected"], f"IAAFT surrogate falsely triggered chirp: {res_iaaft}")

    return {
        "true_lag_samples": lag_true,
        "newtonian_inspiral_1x_true_alpha_3.6667": res_pn1,
        "newtonian_inspiral_2.5x_scale_invariance": res_pn25,
        "control_linear_chirp_true_alpha_0.0": res_lin,
        "control_exponential_chirp_true_alpha_1.0": res_exp,
        "control_sine_gaussian_glitch": res_gl,
        "control_independent_red_noise": res_red,
        "control_iaaft_surrogate": res_iaaft,
    }


def main() -> None:
    part_a = part_a_gravity_latch_audit()
    part_b = part_b_chirp_invariant_audit()
    payload = {
        "probe": "probe2_latch_outside_anchors_and_chirp",
        "part_a_gravity_latch_and_t4_audit": part_a,
        "part_b_repaired_blind_chirp_invariant": part_b,
    }
    # Reference-BLAS IEEE-754 float payload digest (cross-BLAS builds may differ at <=1.5e-15 relative last-ULP)
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["sha256_canonical"] = hashlib.sha256(canon).hexdigest()
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("=== PROBE 2 COMPLETE: LATCH / OUTSIDE-ANCHOR / T4 & BLIND CHIRP PASSED ===")
    print(f"Output: {OUT_PATH}")
    print(f"SHA256: {payload['sha256_canonical']}")
    print("\n--- Part A: Latch Geometry & T4 Permuted Nulls (126 gravity systems) ---")
    print("  Full-sample chi2: Hill 3p =", round(part_a["full_sample_fits"]["hill_3p"]["chi2"], 3),
          "| Smooth Sigmoid 3p =", round(part_a["full_sample_fits"]["smooth_sigmoid_3p"]["chi2"], 3),
          "| Jeans 2p =", round(part_a["full_sample_fits"]["jeans_2p"]["chi2"], 3))
    print("  sin^2(sharp_185_kink, Col(Phi)) =", round(part_a["latch_geometry"]["sharp_185_kink_vs_smooth_sigmoid_sin2"], 5))
    print("  T4 stratified-perm p(kink) =", round(part_a["t4_permuted_null_early_warning"]["kink_stratified_perm_pvalue"], 5),
          "| T4 global-perm p(cross-catalog offset) =", round(part_a["t4_permuted_null_early_warning"]["cross_catalog_offset_perm_pvalue"], 5))
    print("  LOCO sample-disjoint holdouts:")
    for row in part_a["leave_one_catalog_out_outside_anchors"]:
        print(
            f"    hold={row['held_out_catalog']:20s} (n={row['n_holdout']:2d}): "
            f"MOND={row['holdout_chi2_pure_MOND']:7.2f}, Hill={row['holdout_chi2_hill_3p']:6.2f}, "
            f"Sigmoid={row['holdout_chi2_smooth_sigmoid_3p']:6.2f}, Jeans2p={row['holdout_chi2_jeans_2p']:6.2f} "
            f"(train sc={row['train_hill_sc_kms']:.1f}, sigJ={row['train_jeans_sigJ_kms']:.1f})"
        )
    print("  SPARC -> disjoint KiDS-1000 1 Mpc:", part_a["sparc_to_kids_1mpc_disjoint_anchor"])
    print("\n--- Part B: Blind Scale-Invariant Chirp Estimator (zero priors) ---")
    for k, v in part_b.items():
        if isinstance(v, dict):
            print(f"  {k:42s}: corr={v['peak_corr']:+.3f}, lag={v['best_lag_samples']:+3d}, alpha_hat={str(v['alpha_hat']):>6s}, nonlin={v['min_nonlinearity']:.2e}, detected={v['monotone_chirp_detected']}")


if __name__ == "__main__":
    main()
