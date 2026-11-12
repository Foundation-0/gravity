#!/usr/bin/env python3
"""Structural RAR identifiability, with deterministic synthetic controls only.

No observations are read. Accelerations are expressed in units of A_REF.
Run: python3 probe.py [--output results.json]
Dependencies: numpy, scipy. This is a design calculation, not a survey forecast.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import scipy
from scipy.optimize import least_squares, brentq
from scipy.stats import norm

A_REF = 1.2e-10
OMEGA_M = 0.315
LN10 = math.log(10.0)
PARAMETERS = ["ln_A_over_Aref", "ln_B", "q", "s", "ln_C", "u"]


def expansion(z):
    z = np.asarray(z, dtype=float)
    if np.any(z < 0) or not np.all(np.isfinite(z)):
        raise ValueError("Redshifts must be finite and nonnegative")
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + 1.0 - OMEGA_M)


def log_model(theta, log_gnom, z, deep=False):
    """ln(g_measured/A_REF); b=actual/nominal, k=measured/true."""
    la, lb, q, s, lc, u = np.asarray(theta, dtype=float)
    e = np.log(expansion(z))
    lg = np.asarray(log_gnom) + lb + s * e
    la_z = la + q * e
    if deep:
        return lc + u * e + 0.5 * (lg + la_z)
    x = np.exp(0.5 * (lg - la_z))
    return lc + u * e + lg - np.log(-np.expm1(-x))


def jacobian(theta, log_gnom, z, deep=False):
    la, lb, q, s, _, _ = np.asarray(theta, dtype=float)
    e = np.log(expansion(z))
    x = np.exp(0.5 * (log_gnom + lb - la + (s - q) * e))
    if deep:
        t = np.full_like(e, 0.5)
    else:
        t = np.zeros_like(x)
        m = x < 700
        t[m] = x[m] / (2.0 * np.expm1(x[m]))
    return np.column_stack([t, 1.0 - t, t * e, (1.0 - t) * e,
                            np.ones_like(e), e])


def grid(lo=-4, hi=2, nr=8, nz=16, local=False):
    zs = np.linspace(0.33, 1.44, nz)
    if local:
        zs = np.r_[0.0, zs]
    z, lg = np.meshgrid(zs, np.linspace(lo, hi, nr) * LN10, indexing="ij")
    return lg.ravel(), z.ravel()


def fisher_report(j, sigma_dex=0.05):
    """Unitless toy information; every row artificially independent."""
    singular = np.linalg.svd(j / (sigma_dex * LN10), compute_uv=False)
    tol = 1e-10 * singular[0]
    rank = int(np.count_nonzero(singular > tol))
    out = {"n_rows": int(j.shape[0]), "n_parameters": int(j.shape[1]),
           "rank_relative_tolerance": 1e-10, "numerical_rank": rank,
           "singular_values": singular.tolist(), "sigma_ln_y": sigma_dex * LN10,
           "independent_rows_assumed_for_design_only": True}
    if rank == j.shape[1]:
        _, sv, vt = np.linalg.svd(j / (sigma_dex * LN10), full_matrices=False)
        cov = (vt.T / sv**2) @ vt
        out["parameter_standard_deviations"] = np.sqrt(np.diag(cov)).tolist()
        out["condition_number"] = float(singular[0] / singular[-1])
    else:
        out["parameter_standard_deviations"] = None
        out["condition_number"] = None
    return out


def fit_subset(y, lg, z, free=(0, 2), fixed=None, deep=False):
    base = np.zeros(6) if fixed is None else np.array(fixed, dtype=float)
    free = list(free)

    def full(v):
        t = base.copy()
        t[free] = v
        return t

    fit = least_squares(lambda v: log_model(full(v), lg, z, deep) - y,
                        base[free], jac=lambda v: jacobian(full(v), lg, z, deep)[:, free],
                        xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=3000)
    err = (log_model(full(fit.x), lg, z, deep) - y) / LN10
    return {"success": bool(fit.success), "theta": full(fit.x).tolist(),
            "free_parameters": [PARAMETERS[i] for i in free],
            "max_abs_residual_dex": float(np.max(np.abs(err))),
            "rms_residual_dex": float(np.sqrt(np.mean(err**2)))}


def run():
    checks = []

    def check(name, condition, evidence):
        checks.append({"name": name, "passed": bool(condition), "evidence": evidence})
        if not condition:
            raise AssertionError(name + ": " + str(evidence))

    zero = np.zeros(6)
    wide_lg, wide_z = grid()
    # Derivatives checked against finite differences away from both limits.
    trial = np.array([0.17, -0.21, 0.72, 0.31, 0.08, -0.12])
    eps = 1e-6
    finite = np.column_stack([(log_model(trial + np.eye(6)[i] * eps, wide_lg, wide_z)
                              - log_model(trial - np.eye(6)[i] * eps, wide_lg, wide_z))
                             / (2 * eps) for i in range(6)])
    j = jacobian(trial, wide_lg, wide_z)
    diff = float(np.max(np.abs(j - finite)))
    check("analytic_jacobian_matches_finite_difference", diff < 2e-9, diff)

    designs = {}
    for name, lo, hi in [("deep_finite", -6, -4), ("transition", -2, 0),
                          ("wide", -4, 2)]:
        lg, z = grid(lo, hi)
        designs[name] = fisher_report(jacobian(zero, lg, z)[:, :4])
    designs["exact_deep_limit"] = fisher_report(jacobian(zero, wide_lg, wide_z, True)[:, :4])
    designs["one_redshift"] = fisher_report(jacobian(zero, wide_lg, np.ones_like(wide_z))[:, :4])
    # A selection pattern with fixed g_true/a0 also destroys the independent columns.
    fixed_ratio_theta = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
    track_lg = np.log(expansion(wide_z)) - 2 * LN10
    designs["fixed_ratio_selection_track"] = fisher_report(jacobian(fixed_ratio_theta, track_lg, wide_z)[:, :4])
    designs["wide_with_free_acceleration_calibration"] = fisher_report(jacobian(zero, wide_lg, wide_z))
    local_lg, local_z = grid(local=True)
    designs["wide_plus_local_with_free_acceleration_calibration"] = fisher_report(jacobian(zero, local_lg, local_z))
    # Fixing k over z removes the full-RAR symmetry. Fixing amplitudes alone does not.
    designs["wide_known_amplitudes_free_q_s_u"] = fisher_report(jacobian(zero, wide_lg, wide_z)[:, [2, 3, 5]])
    designs["wide_known_amplitudes_and_k_free_q_s"] = fisher_report(jacobian(zero, wide_lg, wide_z)[:, [2, 3]])
    check("deep_limit_rank_two", designs["exact_deep_limit"]["numerical_rank"] == 2, designs["exact_deep_limit"])
    check("wide_fixed_k_rank_four", designs["wide"]["numerical_rank"] == 4, designs["wide"]["numerical_rank"])
    check("single_redshift_rank_two", designs["one_redshift"]["numerical_rank"] == 2, designs["one_redshift"]["numerical_rank"])
    check("selection_track_rank_two", designs["fixed_ratio_selection_track"]["numerical_rank"] == 2, designs["fixed_ratio_selection_track"]["numerical_rank"])
    check("full_six_parameter_rank_four", designs["wide_with_free_acceleration_calibration"]["numerical_rank"] == 4, designs["wide_with_free_acceleration_calibration"]["numerical_rank"])
    check("local_anchor_does_not_restore_rank", designs["wide_plus_local_with_free_acceleration_calibration"]["numerical_rank"] == 4, designs["wide_plus_local_with_free_acceleration_calibration"]["numerical_rank"])
    check("known_amplitudes_leave_exponent_rank_two", designs["wide_known_amplitudes_free_q_s_u"]["numerical_rank"] == 2, designs["wide_known_amplitudes_free_q_s_u"]["numerical_rank"])
    check("known_k_restores_exponent_rank", designs["wide_known_amplitudes_and_k_free_q_s"]["numerical_rank"] == 2, designs["wide_known_amplitudes_and_k_free_q_s"]["numerical_rank"])

    # This symmetry is exact for the full interpolation, at every acceleration and z.
    # It also preserves all z=0 amplitudes if only the exponents are shifted.
    shifted = trial + np.array([0.0, 0.0, 1.3, 1.3, 0.0, -1.3])
    symmetry_err = float(np.max(np.abs(log_model(trial, local_lg, local_z)
                                       - log_model(shifted, local_lg, local_z))))
    check("full_RAR_exponent_symmetry_including_z0", symmetry_err < 3e-14, symmetry_err)
    amplitude_shift = trial + np.array([0.7, 0.7, 0.0, 0.0, -0.7, 0.0])
    amplitude_err = float(np.max(np.abs(log_model(trial, wide_lg, wide_z)
                                        - log_model(amplitude_shift, wide_lg, wide_z))))
    check("full_RAR_amplitude_symmetry", amplitude_err < 3e-14, amplitude_err)
    h = np.array([0, 0, 1, 0, 0, 0], dtype=float)
    calibration_counterexample = np.array([0, 0, 0, -1, 0, 1], dtype=float)
    counter_err = float(np.max(np.abs(log_model(h, local_lg, local_z)
                                      - log_model(calibration_counterexample, local_lg, local_z))))
    check("q1_and_q0_full_RAR_counterexample", counter_err < 3e-14, counter_err)
    null_amplitude = np.array([1, 1, 0, 0, -1, 0])
    null_exponent = np.array([0, 0, 1, 1, 0, -1])
    null_err = float(max(np.max(np.abs(j @ null_amplitude)), np.max(np.abs(j @ null_exponent))))
    check("analytic_null_vectors", null_err < 1e-14, null_err)

    injections = {}
    for name, truth in [("physical_evolution", h),
                         ("mass_drift_only", [0, 0, 0, 1, 0, 0]),
                         ("kinematic_drift_only", [0, 0, 0, 0, 0, 0.5]),
                         ("no_evolution", zero)]:
        truth = np.asarray(truth, dtype=float)
        per = {"truth": truth.tolist()}
        for dname, lo, hi, deep in [("exact_deep", -6, -4, True),
                                    ("finite_deep", -6, -4, False),
                                    ("wide", -4, 2, False)]:
            lg, z = grid(lo, hi)
            y = log_model(truth, lg, z, deep)
            per[dname + "_fit_assuming_B1_C1_s0_u0"] = fit_subset(y, lg, z, deep=deep)
        if truth[5] == 0:
            y = log_model(truth, wide_lg, wide_z)
            recovered = fit_subset(y, wide_lg, wide_z, free=(0, 1, 2, 3))
            per["wide_joint_mass_and_evolution_known_k"] = recovered
            max_error = float(np.max(np.abs(np.asarray(recovered["theta"]) - truth)))
            check(name + "_joint_recovery", max_error < 1e-8, max_error)
        expected = truth[2] + truth[3] + 2 * truth[5]
        qdeep = per["exact_deep_fit_assuming_B1_C1_s0_u0"]["theta"][2]
        check(name + "_deep_apparent_slope", abs(qdeep - expected) < 1e-10, {"recovered": qdeep, "expected": expected})
        injections[name] = per

    # Independent high-acceleration predictions can reveal a mass-only false law,
    # but cannot break the exact mass-plus-kinematics symmetry.
    low_lg, low_z = grid(-6, -4)
    high_lg, high_z = grid(1, 2)
    truth_mass = np.array([0, 0, 0, 1, 0, 0], dtype=float)
    wrong_fit = fit_subset(log_model(truth_mass, low_lg, low_z), low_lg, low_z)
    hold_err = (log_model(wrong_fit["theta"], high_lg, high_z)
                - log_model(truth_mass, high_lg, high_z)) / LN10
    holdout = {"training_max_residual_dex": wrong_fit["max_abs_residual_dex"],
               "held_out_high_acceleration_max_residual_dex": float(np.max(np.abs(hold_err))),
               "held_out_high_acceleration_rms_residual_dex": float(np.sqrt(np.mean(hold_err**2))),
               "caveat": "Synthetic held-out acceleration ranges, not independent observed galaxies."}
    check("mass_drift_wrong_law_exposed_by_high_branch", holdout["held_out_high_acceleration_max_residual_dex"] > 0.2, holdout)

    # A constant mass offset is a negative control for spurious redshift evolution.
    constant_mass = np.array([0, 0.2 * LN10, 0, 0, 0, 0], dtype=float)
    constant_fit = fit_subset(log_model(constant_mass, low_lg, low_z, True), low_lg, low_z, deep=True)
    check("constant_mass_shift_changes_amplitude_only_in_deep_limit", abs(constant_fit["theta"][2]) < 1e-10,
          constant_fit)

    # In the deep limit, ideal outer circular motion gives the same a0 statistic.
    gm, r, a = 2.3, 9.1, 0.8
    gbar = gm / r**2
    gobs = math.sqrt(a * gbar)
    v2 = gobs * r
    btfr_err = abs(v2**2 / gm - gobs**2 / gbar)
    check("same_data_BTFR_and_deep_RAR_are_identical", btfr_err < 1e-14, btfr_err)

    thresholds = []
    for z0, z1 in [(0.0, 1.0), (0.33, 1.44)]:
        ratio = float(expansion(z1) / expansion(z0))
        lever = math.log10(ratio)
        # A two-sided Gaussian 95% interval on q, centred on q=1, excludes q=0
        # only if total sigma_q < 1/1.95996. Other errors set zero for this bound.
        bound = lever / 1.959963984540054
        velocity_factor = ratio**0.25
        i_true = math.radians(60)
        i_assumed = math.asin(math.sin(i_true) / velocity_factor)
        thresholds.append({"z_low": z0, "z_high": z1, "E_ratio": ratio,
                           "q0_vs_q1_delta_log10_a0": lever,
                           "equivalent_deep_mass_factor_b": ratio,
                           "equivalent_deep_acceleration_factor_k": math.sqrt(ratio),
                           "equivalent_deep_velocity_factor": velocity_factor,
                           "equivalent_inferred_distance_over_true": 1 / math.sqrt(ratio),
                           "inclination_example_true_deg": 60.0,
                           "inclination_example_assumed_deg": math.degrees(i_assumed),
                           "max_sigma_differential_log10_b_if_only_error_95pct": bound,
                           "max_sigma_differential_log10_k_if_only_error_95pct": bound / 2,
                           "max_sigma_differential_log10_velocity_if_only_error_95pct": bound / 4,
                           "small_sigma_velocity_fraction_if_only_error_95pct": LN10 * bound / 4})

    # Correlated radial points do not deliver the nominal sqrt(n) gain.
    nrad, sig_ind, sig_common = 8, 0.05, 0.10
    honest = math.sqrt(sig_ind**2 / nrad + sig_common**2)
    naive = math.sqrt((sig_ind**2 + sig_common**2) / nrad)
    covariance_control = {"radii_per_galaxy": nrad, "independent_sigma_dex": sig_ind,
                          "shared_sigma_dex": sig_common,
                          "mean_sigma_with_covariance_dex": honest,
                          "mean_sigma_if_marginals_treated_independent_dex": naive,
                          "uncertainty_underestimate_factor": honest / naive}
    check("shared_radial_error_survives_averaging", honest > 2.5 * naive, covariance_control)

    # Deliberately constructed selection control, not the MUSE selection function.
    # For epsilon ~ N(0,sigma^2), selecting epsilon/sigma > alpha moves the
    # retained mean by sigma*phi(alpha)/SF(alpha). Choose thresholds that make
    # the retained conditional mean imitate q=1 although the parent has q=0.
    selection_z = np.linspace(0.33, 1.44, 16)
    selection_sigma = 0.10  # dex in measured log acceleration
    mills = lambda v: norm.pdf(v) / norm.sf(v)
    initial_offset = selection_sigma * mills(-2.0)
    target_offset = initial_offset + 0.5 * np.log10(expansion(selection_z) / expansion(selection_z[0]))
    alpha = np.array([brentq(lambda a: selection_sigma * mills(a) - offset, -12, 12)
                      for offset in target_offset])
    actual_offset = selection_sigma * np.array([mills(a) for a in alpha])
    apparent_slope = float(np.polyfit(np.log10(expansion(selection_z)), 2 * actual_offset, 1)[0])
    selection_control = {"parent_q": 0.0, "parent_b": 1.0, "parent_k": 1.0,
                         "noise_sigma_log10_acceleration": selection_sigma,
                         "retained_mean_apparent_q": apparent_slope,
                         "redshifts": selection_z.tolist(),
                         "cut_in_noise_sigma": alpha.tolist(),
                         "retained_fraction": norm.sf(alpha).tolist(),
                         "retained_mean_residual_dex": actual_offset.tolist(),
                         "interpretation": "A designed truncation counterexample; not a MUSE bias estimate."}
    check("selection_alone_can_shift_conditional_mean", abs(apparent_slope - 1.0) < 1e-11, selection_control)
    no_selection_slope = float(np.polyfit(np.log10(expansion(selection_z)), np.zeros_like(selection_z), 1)[0])
    check("unselected_parent_mean_has_no_evolution", abs(no_selection_slope) < 1e-14, no_selection_slope)

    return {"scope": "Deterministic synthetic identifiability only; no observational fit or survey power forecast.",
            "verdict": "pursue_conditional_calibration_and_selection_design; park_current_empirical_fit",
            "assumptions": {"A_reference_m_s2": A_REF, "Omega_m": OMEGA_M,
                            "cosmology": "flat matter plus constant Lambda, radiation neglected",
                            "b_convention": "actual baryonic acceleration / nominal at fixed geometry",
                            "k_convention": "measured total acceleration / true",
                            "parameters": PARAMETERS,
                            "toy_sigma_dex": 0.05,
                            "toy_rows_are_not_MUSE_measurements": True},
            "designs": designs, "injections": injections,
            "symmetry_max_abs_ln_difference": symmetry_err,
            "q1_q0_counterexample_max_abs_ln_difference": counter_err,
            "heldout": holdout, "constant_mass_control": constant_fit,
            "calibration_thresholds": thresholds, "covariance_control": covariance_control,
            "selection_control": selection_control,
            "checks": checks, "checks_passed": len(checks),
            "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__},
            "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = p.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"checks_passed": result["checks_passed"], "output": str(args.output),
                      "scope": result["scope"]}))
