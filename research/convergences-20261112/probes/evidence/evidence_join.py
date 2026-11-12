#!/usr/bin/env python3
"""Synthetic evidence joins with explicit measurement and selection models.

Uses only the Python standard library. No astronomical data are fitted.
Run: python3 evidence_join.py
Writes results.json beside this script. All variables are dimensionless except
the deliberately invented eclipse times/periods, which are in days.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path


def variance_of_signal(noise_variance: float) -> float:
    """Posterior variance for q~N(0,1), y=q+noise of known variance."""
    return noise_variance / (1.0 + noise_variance)


def entropy(probabilities: list[float]) -> float:
    return -sum(p * math.log2(p) for p in probabilities if p)


def control_case(alpha: float, variance: float = 0.01) -> dict:
    """y=q+b+e, x=alpha*q+b+eta; q,b~N(0,1), e,eta~N(0,v).

    The known-model posterior uses both measurements correctly, including
    target leakage into the control. The residual response is what blind
    population regression y-E[y|x] would retain of q.
    """
    cyy = 2.0 + variance
    cxx = alpha * alpha + 1.0 + variance
    cyx = alpha + 1.0
    determinant = cyy * cxx - cyx * cyx
    posterior_y_weight = (cxx - alpha * cyx) / determinant
    posterior_x_weight = (alpha * cyy - cyx) / determinant
    posterior_variance = 1.0 - posterior_y_weight - alpha * posterior_x_weight
    beta = cyx / cxx
    return {
        "signal_leakage_into_control": alpha,
        "known_model_posterior_variance": posterior_variance,
        "posterior_mean_weights_y_x": [posterior_y_weight, posterior_x_weight],
        "blind_regression_beta": beta,
        "blind_regression_signal_response": 1.0 - beta * alpha,
    }


def gaussian_probe() -> dict:
    v = 0.01
    n = 100
    single = variance_of_signal(1.0 + v)
    repeated_shared_bias = variance_of_signal(1.0 + v / n)
    repeated_independent_bias = variance_of_signal((1.0 + v) / n)
    clean_control = control_case(0.0, v)
    joined = clean_control["known_model_posterior_variance"]
    residual_noise = v + v / (1.0 + v)
    assert math.isclose(joined, variance_of_signal(residual_noise), abs_tol=1e-13)

    # Incorrectly treating the common calibration offset as independent
    # produces an incorrect posterior mean as well as an overnarrow interval.
    wrong_variance = repeated_independent_bias
    wrong_gain = 1.0 - wrong_variance
    wrong_mse = (1.0 - wrong_gain) ** 2 + wrong_gain**2 * (1.0 + v / n)
    wrong_95_coverage = math.erf(1.959963984540054 * math.sqrt(wrong_variance / wrong_mse) / math.sqrt(2.0))

    # Independent simulation checks the closed-form posterior error variance.
    rng = random.Random(20261112)
    trials = 100_000
    w_y, w_x = clean_control["posterior_mean_weights_y_x"]
    single_error = joint_error = 0.0
    for _ in range(trials):
        q, b = rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)
        y = q + b + rng.gauss(0.0, math.sqrt(v))
        x = b + rng.gauss(0.0, math.sqrt(v))
        single_error += (q - y / (2.0 + v)) ** 2
        joint_error += (q - w_y * y - w_x * x) ** 2
    single_mc, joint_mc = single_error / trials, joint_error / trials
    assert abs(single_mc / single - 1) < 0.02
    assert abs(joint_mc / joined - 1) < 0.02
    assert math.isclose(control_case(1.0)["known_model_posterior_variance"], variance_of_signal(1.0 + v / 2.0))

    return {
        "model": "q,b independent N(0,1); y_i=q+b+e_i; x=b+eta; e_i,eta independent N(0,0.01)",
        "posterior_variances": {
            "one_target_measurement": single,
            "one_hundred_exact_copies": single,
            "one_hundred_fresh_readouts_same_bias": repeated_shared_bias,
            "one_hundred_measurements_independent_biases": repeated_independent_bias,
            "one_target_plus_one_nuisance_control": joined,
        },
        "control_alone_information_about_q_bits": 0.0,
        "control_conditional_information_given_y_bits": 0.5 * math.log2(single / joined),
        "posterior_variance_reduction_with_control_factor": single / joined,
        "wrong_independence_model": {
            "assumed_posterior_variance": wrong_variance,
            "actual_estimator_mean_squared_error": wrong_mse,
            "actual_prior_predictive_coverage_of_nominal_95_percent_interval": wrong_95_coverage,
        },
        "control_leakage_cases": [control_case(a) for a in (0.0, 0.1, 0.5, 1.0)],
        "simulation": {
            "seed": 20261112,
            "trials": trials,
            "single_measurement_error_variance": single_mc,
            "joined_measurement_error_variance": joint_mc,
        },
    }


def predicts_eclipse(time: float, period: float) -> bool:
    # Deliberately idealized zero timing error and fixed eclipse shape.
    return abs(time / period - round(time / period)) < 1e-10


def expected_information(periods: list[float], time: float, completeness: float) -> float:
    prior = 1.0 / len(periods)
    detection_probabilities = [completeness if predicts_eclipse(time, p) else 0.0 for p in periods]
    p_detect = sum(detection_probabilities) * prior
    expected_entropy = 0.0
    for detected, outcome_probability in ((True, p_detect), (False, 1.0 - p_detect)):
        if outcome_probability == 0:
            continue
        likelihoods = detection_probabilities if detected else [1.0 - d for d in detection_probabilities]
        posterior = [prior * likelihood / outcome_probability for likelihood in likelihoods]
        expected_entropy += outcome_probability * entropy(posterior)
    return entropy([prior] * len(periods)) - expected_entropy


def alias_probe() -> dict:
    candidates = [120.0 / k for k in range(1, 7)]
    archival_survivors = [p for p in candidates if predicts_eclipse(-440.0, p)]
    assert archival_survivors == [40.0, 20.0]
    completeness_cases = []
    for c in (0.0, 0.05, 0.95, 1.0):
        likelihoods = [1.0 - c if predicts_eclipse(20.0, p) else 1.0 for p in archival_survivors]
        norm = sum(likelihoods)
        completeness_cases.append({
            "detection_completeness": c,
            "posterior_after_no_eclipse_at_day_20": {str(p): l / norm for p, l in zip(archival_survivors, likelihoods)},
            "expected_information_at_day_20_bits": expected_information(archival_survivors, 20.0, c),
            "expected_information_at_shared_phase_day_0_bits": expected_information(archival_survivors, 0.0, c),
        })
    assert math.isclose(completeness_cases[2]["posterior_after_no_eclipse_at_day_20"]["40.0"], 1 / 1.05)
    return {
        "synthetic_event_times_days": [0.0, 120.0],
        "assumptions": "Uniform prior on six displayed aliases; known phase; perfect detected-event times; stationary eclipse; zero false positive rate; known detection completeness.",
        "modern_alias_periods_days": candidates,
        "added_archival_event_time_days": -440.0,
        "surviving_aliases_days": archival_survivors,
        "candidate_discriminating_exposure_day": 20.0,
        "cases": completeness_cases,
    }


def line_graph_probe() -> dict:
    # An algebraic four-level example. Alternating even/odd parity can allow
    # this cycle, unlike a triangle of three electric-dipole transitions.
    # This is not an atomic identification: intensities and other quantum
    # numbers still have to be checked for real line assignments.
    edges = [3.0, 5.0, 4.0, 12.0]
    cycle = lambda values: values[0] + values[1] + values[2] - values[3]
    scaled = [1.02 * value for value in edges]
    wrong_assignment = [3.0, 5.0, 4.0, 12.5]
    assert abs(cycle(edges)) < 1e-12
    assert abs(cycle(scaled)) < 1e-12
    assert cycle(wrong_assignment) == -0.5
    return {
        "assumed_levels": [0.0, 3.0, 8.0, 12.0],
        "observed_differences": edges,
        "cycle_residual": cycle(edges),
        "with_wrong_fourth_line_cycle_residual": cycle(wrong_assignment),
        "with_shared_2_percent_scale_error_cycle_residual": cycle(scaled),
        "interpretation": "An extra edge can check consistency without adding parameter dimension. A common multiplicative calibration error survives every cycle check.",
    }


def main() -> None:
    result = {
        "status": "Synthetic reproducible demonstrations, not new observational findings or a replication of nonlinear ICA identifiability.",
        "gaussian_control": gaussian_probe(),
        "eclipse_aliases": alias_probe(),
        "difference_graph": line_graph_probe(),
    }
    out = Path(__file__).with_name("results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
