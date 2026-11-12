#!/usr/bin/env python3
"""Small checks of persistence mechanisms, not simulations of an AeST halo.

Python standard library only. Re-run to regenerate results.json.
Sources and physical limitations are in reports/persistence.md and its ledger.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def late_annihilation(q: float, u: float) -> tuple[float, float]:
    """y_minus(0)=1; y_plus-y_minus=q; dy_minus/du=-y_minus*y_plus.

    u = Y0 integral(s <sigma v> dt), after inverse production is negligible.
    Both y values are entropy-normalized yields divided by initial Y_minus.
    """
    if q == 0.0:
        ym = 1.0 / (1.0 + u)
    else:
        ym = q / (q + (1.0 + q) * math.expm1(q * u))
    return ym + q, ym


def annihilation_rk4(q: float, u: float, steps: int = 20000) -> float:
    h = u / steps
    y = 1.0
    f = lambda a: -a * (a + q)
    for _ in range(steps):
        a = f(y)
        b = f(y + 0.5 * h * a)
        c = f(y + 0.5 * h * b)
        d = f(y + h * c)
        y += h * (a + 2.0 * b + 2.0 * c + d) / 6.0
    return y


def annihilation_probe() -> dict:
    rows = []
    for q in (0.0, 0.001, 0.01, 0.1):
        yp, ym = late_annihilation(q, 100.0)
        numeric = annihilation_rk4(q, 100.0)
        relative_error = abs(numeric - ym) / ym
        assert relative_error < 1e-8
        assert math.isclose(yp - ym, q, abs_tol=1e-14)
        rows.append({
            "initial_asymmetry_q": q,
            "final_y_plus": yp,
            "final_y_minus": ym,
            "final_total_y": yp + ym,
            "minority_to_majority": ym / yp,
            "rk4_relative_error": relative_error,
        })
    return {
        "model": "After inverse production is negligible, adiabatic entropy, only pair annihilation, no decays or fresh production",
        "exposure_u": 100.0,
        "initial_y_minus": 1.0,
        "rows": rows,
        "radiation_era_example": {
            "assumptions": "Constant relativistic degrees of freedom and s-wave cross section; dY/dx proportional to -Y_plus Y_minus/x^2",
            "u_of_x": "u_infinity * (1 - x_start/x)",
            "lesson": "Finite integrated exposure leaves a symmetric remnant; an exact conserved excess also sets a lower bound",
        },
    }


def wave_probe() -> dict:
    """Exact free Schrodinger standing wave in units hbar=m=1.

    The pointwise Madelung current velocity is zero away from density nodes.
    Momentum measurements have two peaks. After averaging spatial interference,
    the Wigner distribution is a mixture of the two momentum peaks.
    This does not equate a wave's pointwise velocity with two classical velocities.
    """
    length = 2.0 * math.pi
    k = 3
    grid = 4096
    dx = length / grid
    norm = mean_p = mean_p2 = kinetic = max_current = 0.0
    for i in range(grid):
        x = (i + 0.37) * dx
        a, b = cmath.exp(1j * k * x), cmath.exp(-1j * k * x)
        psi = (a + b) / math.sqrt(2.0 * length)
        first = 1j * k * (a - b) / math.sqrt(2.0 * length)
        second = -(k * k) * psi
        norm += abs(psi) ** 2 * dx
        mean_p += (psi.conjugate() * (-1j * first)).real * dx
        mean_p2 += (psi.conjugate() * (-second)).real * dx
        kinetic += 0.5 * abs(first) ** 2 * dx
        max_current = max(max_current, abs((psi.conjugate() * first).imag))
    assert math.isclose(norm, 1.0, abs_tol=1e-12)
    assert abs(mean_p) < 1e-12
    assert math.isclose(mean_p2, k * k, abs_tol=1e-11)
    assert math.isclose(kinetic, 0.5 * k * k, abs_tol=1e-11)
    assert max_current < 1e-12
    return {
        "model": "Free standing wave, not AeST and not a collapse simulation",
        "units": "hbar=m=1",
        "length": length,
        "wavenumber": k,
        "norm": norm,
        "mean_momentum": mean_p,
        "momentum_variance": mean_p2 - mean_p**2,
        "kinetic_energy": kinetic,
        "max_pointwise_probability_current": max_current,
        "momentum_distribution": [{"p": -k, "weight": 0.5}, {"p": k, "weight": 0.5}],
        "coarse_graining": "Spatial averaging over many interference fringes removes the p=0 Wigner interference term",
        "lesson": "Zero current does not imply zero momentum spread or zero kinetic energy",
    }


def simpson(fun, a: float, b: float, n: int = 4000) -> float:
    h = (b - a) / n
    value = fun(a) + fun(b)
    value += 4.0 * sum(fun(a + h * i) for i in range(1, n, 2))
    value += 2.0 * sum(fun(a + h * i) for i in range(2, n, 2))
    return value * h / 3.0


def spectral_probe() -> dict:
    """Integrate an assumed self-similar low-momentum spectrum, not dynamics.

    f(k,t)=t^alpha exp[-(t^beta k)^2], |k| <= K t^-beta.
    N scales as t^(alpha-beta), kinetic energy as t^(alpha-3 beta) in 1D.
    Setting alpha=beta conserves N in that moving band but reduces its energy.
    """
    beta = 0.1
    alpha = beta
    cutoff = 3.0
    rows = []
    baseline_n = baseline_e = None
    for t in (1.0, 10.0, 100.0):
        edge = cutoff * t ** (-beta)
        f = lambda k: t**alpha * math.exp(-((t**beta * k) ** 2))
        number = simpson(f, -edge, edge)
        energy = simpson(lambda k: 0.5 * k * k * f(k), -edge, edge)
        if baseline_n is None:
            baseline_n, baseline_e = number, energy
        ratio_n, ratio_e = number / baseline_n, energy / baseline_e
        expected_energy = t ** (-2.0 * beta)
        assert math.isclose(ratio_n, 1.0, rel_tol=1e-12)
        assert math.isclose(ratio_e, expected_energy, rel_tol=1e-12)
        rows.append({"t_over_t0": t, "moving_cutoff": edge,
                     "number_ratio": ratio_n, "kinetic_energy_ratio": ratio_e,
                     "expected_kinetic_energy_ratio": expected_energy})
    return {
        "model": "Assumed one-dimensional Gaussian scaling spectrum restricted to a moving low-momentum band",
        "alpha": alpha, "beta": beta,
        "rows": rows,
        "lesson": "An isolated whole system can order at low momentum by transferring energy outside that sector",
        "limit": "No collision equation was solved; no mechanism, exponent or applicability to dark matter is established",
    }


def condensation_clock_probe() -> dict:
    """Levkov et al. 2018 Sec. 6 illustrative virialized kinetic estimate.

    q = R m v/hbar >> 1; tau_gr/t_dyn ~= 0.047 q^3/ln(q).
    The coefficient includes their approximate virial density relation.
    This is not a universal bound and does not apply at q of order one.
    """
    rows = [{"q_Rmv_over_hbar": q,
             "tau_gr_over_t_dyn": 0.047 * q**3 / math.log(q)}
            for q in (10.0, 30.0, 100.0, 300.0)]
    return {"model": "Kinetic gravitational condensation estimate in a specified boson model",
            "rows": rows,
            "limit": "Requires high occupation, q much greater than one, kinetic evolution, and stated virial assumptions; not AeST"}


def main() -> None:
    result = {
        "status": "Illustrative analytical consequences with numerical checks; no observations or AeST nonlinear evolution",
        "late_annihilation": annihilation_probe(),
        "one_wave_two_momenta": wave_probe(),
        "ordering_by_spectral_transport": spectral_probe(),
        "condensation_time": condensation_clock_probe(),
    }
    destination = HERE / "results.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {destination}")
    print("Analytical solutions, conserved difference, wave moments and spectral integrals checked.")


if __name__ == "__main__":
    main()
