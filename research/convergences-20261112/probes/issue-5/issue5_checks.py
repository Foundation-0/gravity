"""Small analytic checks for issue #5. No AeST collapse is simulated.

Run from the repository root: python3 research/convergences-20261112/probes/issue-5/issue5_checks.py
Requires SymPy; writes results.json beside this script.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as s


def main() -> None:
    x, t, T, alpha, M = s.symbols("x t T alpha M", real=True)
    pi = x**2 / (2 * (T - t))
    velocity = -s.diff(pi, x)
    sigma = s.simplify(s.diff(pi, t) - s.diff(pi, x) ** 2 / 2)
    fourth_derivative = s.diff(pi, x, 4)
    eom = s.simplify(
        s.diff(sigma, t)
        - s.diff(sigma * s.diff(pi, x), x)
        + alpha / M**2 * fourth_derivative
    )
    burgers = s.simplify(s.diff(velocity, t) + velocity * s.diff(velocity, x))
    assert sigma == fourth_derivative == eom == burgers == 0

    # Differences of two linear AeST initial states, using 2007.00082 Eqs 7-11.
    # B = 1/(8*pi*Gtilde*a**2*rhobar); k is the comoving wave number.
    # Common metric and other-species data are held fixed initially.
    B, k, KB, Q, cs2, w, eps, H = s.symbols(
        "B k K_B Q c_ad_squared w epsilon H", nonzero=True, real=True
    )
    A = (1 + w) / (Q * cs2)
    delta_E = eps
    delta_chi = s.Integer(0)
    delta_Y = KB * delta_E + (2 - KB) * delta_chi
    delta_gamma = B * k**2 * delta_Y / A
    delta_density = s.simplify(A * delta_gamma - B * k**2 * delta_Y)
    delta_theta = s.Integer(0)
    delta_pressure = s.simplify(cs2 * delta_density + cs2 * B * k**2 * delta_Y)
    delta_theta_dot = s.simplify(delta_pressure / (1 + w))
    kinematic_delta_theta_dot = s.simplify(delta_gamma / Q)
    delta_density_dot = s.simplify(-3 * H * delta_pressure)
    delta_E_dot = s.simplify(
        -H * eps - (2 - KB) * Q * delta_pressure / (KB * (1 + w))
    )
    assert delta_density == delta_theta == 0
    assert s.simplify(delta_pressure - cs2 * B * k**2 * KB * eps) == 0
    assert s.simplify(delta_theta_dot - kinematic_delta_theta_dot) == 0

    # Exact free-streaming counterexample: same density, mean velocity and
    # variance, different distribution shape. No gravity or collisions.
    response = []
    for tau in [0.0, 0.5, 1.0, math.pi / 2, math.pi]:
        response.append(
            {
                "tau_equals_k_sigma_t": tau,
                "two_stream_density_amplitude_ratio": math.cos(tau),
                "gaussian_density_amplitude_ratio": math.exp(-tau * tau / 2),
            }
        )
    assert abs(response[-1]["two_stream_density_amplitude_ratio"] + 1) < 1e-14

    result = {
        "scope": "Analytic identities and exact toy responses; no nonlinear AeST simulation.",
        "sympy_version": s.__version__,
        "perfect_caustic": {
            "model": "Nonrelativistic ghost-condensate truncation, external potential zero",
            "pi": str(pi),
            "velocity": str(velocity),
            "Sigma": str(sigma),
            "pi_xxxx": str(fourth_derivative),
            "equation_of_motion_residual": str(eom),
            "inviscid_burgers_residual": str(burgers),
            "pi_xx": str(s.diff(pi, x, 2)),
            "status": "Local exact special solution for t<T. Not a finite-energy periodic halo.",
        },
        "linear_aest_compensated_initial_pair": {
            "delta_E": str(delta_E),
            "delta_gamma": str(delta_gamma),
            "delta_density_contrast": str(delta_density),
            "delta_theta": str(delta_theta),
            "delta_pressure_contrast": str(delta_pressure),
            "delta_theta_dot": str(delta_theta_dot),
            "kinematic_delta_theta_dot": str(kinematic_delta_theta_dot),
            "delta_density_dot": str(delta_density_dot),
            "delta_E_dot_from_published_equation_12": str(delta_E_dot),
            "status": "Algebra in published linear variables; implementation must verify its complete constraint map and admissible initial ensemble.",
        },
        "free_streaming_equal_first_moments": {
            "two_stream_variance_over_sigma_squared": 1,
            "gaussian_variance_over_sigma_squared": 1,
            "two_stream_fourth_moment_over_sigma_fourth": 1,
            "gaussian_fourth_moment_over_sigma_fourth": 3,
            "density_response": response,
        },
    }
    path = Path(__file__).with_name("results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": "passed", "results": str(path)}, indent=2))


if __name__ == "__main__":
    main()
