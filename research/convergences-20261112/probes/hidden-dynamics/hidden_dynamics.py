#!/usr/bin/env python3
"""Small exact/reproducible examples of elimination, closure, and memory.

Python standard library only. These are mathematical examples, not fits to
astronomical data or an AeST/MOND calculation. Run this file from any directory.
Outputs are written beside the script.
"""

import cmath
import csv
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent


def exact(t, gamma, x0, y0):
    """x'=-x+y; y'=-gamma*(x+y). Return x and y."""
    gap = cmath.sqrt(gamma * gamma - 6 * gamma + 1)
    r1, r2 = (-(1 + gamma) + gap) / 2, (-(1 + gamma) - gap) / 2
    if abs(gap) < 1e-10:
        raise ValueError("Repeated-root case is not used in this probe")
    c1 = (-x0 + y0 - r2 * x0) / (r1 - r2)
    c2 = x0 - c1
    x = c1 * cmath.exp(r1 * t) + c2 * cmath.exp(r2 * t)
    dx = r1 * c1 * cmath.exp(r1 * t) + r2 * c2 * cmath.exp(r2 * t)
    assert abs(x.imag) < 1e-10 and abs(dx.imag) < 1e-10
    return x.real, (dx + x).real


def rk4(gamma, x0, y0, h, duration):
    x, y = x0, y0
    rows = [(0.0, x, y)]

    def f(x, y):
        return -x + y, -gamma * (x + y)

    for i in range(round(duration / h)):
        a, b = f(x, y)
        c, d = f(x + h * a / 2, y + h * b / 2)
        e, f2 = f(x + h * c / 2, y + h * d / 2)
        g, j = f(x + h * e, y + h * f2)
        x += h * (a + 2 * c + 2 * e + g) / 6
        y += h * (b + 2 * d + 2 * f2 + j) / 6
        rows.append(((i + 1) * h, x, y))
    return rows


def volterra(gamma, x0, y0, h, duration):
    """Independent trapezoid solution of the scalar memory equation.

    q(t)=integral_0^t exp[-gamma*(t-s)] x(s) ds.
    q is updated by trapezoidal convolution, NOT by the full y equation.
    x'=-x+exp(-gamma*t)*y0-gamma*q, also using trapezoid.
    """
    x, q, fprev = x0, 0.0, -x0 + y0
    decay = math.exp(-gamma * h)
    rows = [(0.0, x)]
    for i in range(round(duration / h)):
        t = (i + 1) * h
        known = math.exp(-gamma * t) * y0 - gamma * decay * q
        known -= gamma * h * decay * x / 2
        xnew = (x + h * (fprev + known) / 2) / (1 + h / 2 + gamma * h * h / 4)
        q = decay * q + h * (decay * x + xnew) / 2
        x = xnew
        fprev = -x + math.exp(-gamma * t) * y0 - gamma * q
        rows.append((t, x))
    return rows


def matrix_product(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def kron(a, b):
    return [[x * y for x in ar for y in br] for ar in a for br in b]


def conjugate(u, rho):
    # All matrices in this probe are real.
    return matrix_product(matrix_product(u, rho), transpose(u))


def partial_trace(rho, keep):
    if keep == "S":
        return [[sum(rho[2 * i + e][2 * j + e] for e in range(2)) for j in range(2)] for i in range(2)]
    return [[sum(rho[2 * s + i][2 * s + j] for s in range(2)) for j in range(2)] for i in range(2)]


def qubit_trace_distance(a, b):
    """Half the trace norm of the difference of two real qubit states."""
    d00, d11, d01 = a[0][0] - b[0][0], a[1][1] - b[1][1], a[0][1] - b[0][1]
    gap = math.sqrt((d00 - d11) ** 2 + 4 * d01 * d01)
    eigenvalues = ((d00 + d11 + gap) / 2, (d00 + d11 - gap) / 2)
    return sum(abs(value) for value in eigenvalues) / 2


def quantum_swap():
    # Reproduces the discrete process in Pollock et al. 1801.09811, App. B.3,
    # with an explicit reset inserted before the second swap.
    zero = [[1, 0], [0, 0]]
    one = [[0, 0], [0, 1]]
    plus = [[0.5, 0.5], [0.5, 0.5]]
    swap = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    cases = []
    for label, state in [("zero", zero), ("one", one), ("plus", plus)]:
        initial = kron(state, zero)
        mid = conjugate(swap, initial)
        smid, emid = partial_trace(mid, "S"), partial_trace(mid, "E")
        reset = kron(zero, emid)
        final = conjugate(swap, reset)
        sfinal = partial_trace(final, "S")
        defect = max(abs(mid[i][j] - kron(smid, emid)[i][j]) for i in range(4) for j in range(4))
        assert smid == zero and sfinal == state and defect == 0
        cases.append({"initial_system": label, "system_after_first_swap": smid,
                      "system_after_reset": zero, "system_after_second_swap": sfinal,
                      "product_state_defect_at_middle": defect})
    reset_distance = qubit_trace_distance(cases[0]["system_after_reset"], cases[1]["system_after_reset"])
    final_distance = qubit_trace_distance(cases[0]["system_after_second_swap"], cases[1]["system_after_second_swap"])
    assert reset_distance == 0 and final_distance == 1
    return {"cases": cases, "trace_distance_after_reset_zero_vs_one": reset_distance,
            "trace_distance_after_second_swap_zero_vs_one": final_distance,
            "qualification": "Product states at sampled discrete times; no claim about a continuous gate implementation."}


def main():
    checks = []
    for h in (0.04, 0.02, 0.01, 0.005):
        full = rk4(1, 1, -1, h, 6)
        reduced = volterra(1, 1, -1, h, 6)
        e_full = max(abs(x - exact(t, 1, 1, -1)[0]) for t, x, _ in full)
        e_reduced = max(abs(x - exact(t, 1, 1, -1)[0]) for t, x in reduced)
        checks.append({"dt": h, "full_rk4_max_abs_error": e_full,
                       "scalar_volterra_max_abs_error": e_reduced})
    assert checks[-1]["full_rk4_max_abs_error"] < 1e-10
    assert checks[-1]["scalar_volterra_max_abs_error"] < 1e-5
    convergence = [checks[i]["scalar_volterra_max_abs_error"] / checks[i+1]["scalar_volterra_max_abs_error"] for i in range(3)]
    assert all(3.8 < ratio < 4.2 for ratio in convergence)

    markov_errors = []
    for gamma in (1, 10, 100):
        err = max(abs(exact(i / 2000, gamma, 1, -1)[0] - math.exp(-2 * i / 2000)) for i in range(12001))
        markov_errors.append({"gamma": gamma, "max_abs_error_xdot_equals_minus_2x": err,
                              "interval": [0, 6], "initial_state": [1, -1]})
    assert markov_errors[-1]["max_abs_error_xdot_equals_minus_2x"] < markov_errors[0]["max_abs_error_xdot_equals_minus_2x"] / 30

    t_split = 1.0
    split = {"x0": 0.0, "gamma": 1.0, "t": t_split,
             "x_y0_plus_1": exact(t_split, 1, 0, 1)[0],
             "x_y0_minus_1": exact(t_split, 1, 0, -1)[0]}
    # Stationary 2D OU example: dZ=A Z dt+sqrt(2)dW, A=[[-1,1],[-1,-1]].
    # Stationary covariance is I since A+A^T+2I=0. C_x(t)=exp(-|t|) cos(t).
    lag = math.pi / 4
    c1, c2 = math.exp(-lag) * math.cos(lag), math.exp(-2 * lag) * math.cos(2 * lag)
    conditional_covariance = c2 - c1 * c1
    conditional_correlation = conditional_covariance / (1 - c1 * c1)
    ou = {"lag": lag, "C0": 1.0, "C_lag": c1, "C_2lag": c2,
          "markov_required_C_2lag": c1 * c1,
          "cov_X0_X2_given_X1": conditional_covariance,
          "corr_X0_X2_given_X1": conditional_correlation,
          "conditional_mutual_information_nats": -math.log(1 - conditional_correlation ** 2) / 2}
    assert abs(conditional_covariance) > 0.1

    frequency = []
    for gamma in (1, 20):
        for omega in (0, 1, 2):
            s = complex(0, omega)
            chi = (s + gamma) / (s * s + (1 + gamma) * s + 2 * gamma)
            frequency.append({"gamma": gamma, "omega": omega, "response_real": chi.real,
                              "response_imag": chi.imag, "amplitude": abs(chi),
                              "phase_deg": math.degrees(cmath.phase(chi))})
    # Hidden-coordinate rescaling leaves the complete retained response unchanged.
    # Original B=1, C=-gamma, D=-gamma. Transform y_new=r*y.
    rescale, gamma = 7.0, 20.0
    response_defects = []
    for omega in (0, 0.5, 1, 2, 10):
        s = complex(0, omega)
        original = -gamma / (s + gamma)
        transformed = (1 / rescale) * (1 / (s + gamma)) * (-rescale * gamma)
        response_defects.append(abs(original - transformed))
    assert max(response_defects) < 1e-14

    results = {"kind": "synthetic mathematical probes; no observational data",
               "classical_equations": "x'=-x+y; y'=-gamma*(x+y)",
               "reduced_equation": "x'=-x+exp(-gamma*t)*y0-gamma*integral_0^t exp(-gamma*(t-s))*x(s) ds",
               "same_present_different_hidden_state": split,
               "numerical_checks": checks, "volterra_step_halving_error_ratios": convergence,
               "instantaneous_closure_errors": markov_errors,
               "stationary_gaussian_non_markov_witness": ou,
               "same_static_response_different_transient_response": frequency,
               "hidden_coordinate_rescaling_max_response_defect": max(response_defects),
               "quantum_two_swap_with_reset": quantum_swap(),
               "all_assertions_passed": True}
    (OUT / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    with (OUT / "trajectories.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["t", "x_hidden_plus", "x_hidden_minus", "x_gamma1", "x_gamma10", "x_gamma100", "instantaneous_closure"])
        for i in range(1201):
            t = i / 200
            writer.writerow([t, exact(t, 1, 0, 1)[0], exact(t, 1, 0, -1)[0],
                             *[exact(t, g, 1, -1)[0] for g in (1, 10, 100)], math.exp(-2*t)])
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
