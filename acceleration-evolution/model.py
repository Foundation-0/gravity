"""Late-time phenomenological acceleration evolution; standard library only.

No observational likelihood or covariant gravity theory is implemented here.
"""

import argparse
import json
import math
from pathlib import Path

FIDUCIAL_A = 1.2e-10  # m s^-2, independently calibrated normalization
FIDUCIAL_OMEGA_M = 0.315
GRID = (0.0, 0.33, 0.5, 0.75, 1.0, 1.44, 2.0, 3.0, 5.0)
C = 299792458.0  # m s^-1, exact
MPC_METRES = 3.085677581491367e22


def _finite(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite real number")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number")
    return value


def expansion(z, omega_m=FIDUCIAL_OMEGA_M):
    """E(z) for flat matter + constant Lambda, without radiation, 0 <= z <= 5."""
    _finite("z", z)
    _finite("omega_m", omega_m)
    if not 0 <= z <= 5:
        raise ValueError("z must lie in [0, 5]")
    if not 0 < omega_m < 1:
        raise ValueError("omega_m must lie strictly between 0 and 1")
    return math.sqrt(omega_m * (1 + z)**3 + 1 - omega_m)


def predict(z, q, amplitude=FIDUCIAL_A, omega_m=FIDUCIAL_OMEGA_M):
    """Predict a0 and conditional asymptotic deep-MOND BTFR shifts.

    Mass intercept means log10(M_b) at fixed velocity for slope four;
    velocity shift means log10(V) at fixed baryonic mass. Isolated systems
    in the deep-MOND asymptotic regime alone obey these translations.
    """
    _finite("q", q)
    _finite("amplitude", amplitude)
    if amplitude <= 0:
        raise ValueError("amplitude must be positive")
    e = expansion(z, omega_m)
    log_ratio = q * math.log10(e)
    try:
        ratio = e**q
        a0 = amplitude * ratio
    except OverflowError as exc:
        raise ValueError("prediction exceeds floating-point range") from exc
    if not all(math.isfinite(v) for v in (log_ratio, ratio, a0)) or ratio <= 0 or a0 <= 0:
        raise ValueError("prediction exceeds floating-point range")
    return {"z": z, "E": e, "a0_m_s2": a0, "a0_ratio_to_z0": ratio,
            "btfr_mass_intercept_shift_dex": -log_ratio,
            "velocity_at_fixed_baryonic_mass_shift_dex": log_ratio / 4}


def local_derivative(q, amplitude=FIDUCIAL_A, omega_m=FIDUCIAL_OMEGA_M):
    """Return da0/dz at z=0, in m s^-2 per unit redshift."""
    predict(0.0, q, amplitude, omega_m)  # shared validation
    result = 1.5 * omega_m * q * amplitude
    if not math.isfinite(result):
        raise ValueError("derivative exceeds floating-point range")
    return result


def radial_acceleration(gbar, z, amplitude=FIDUCIAL_A, q=0.0,
                        omega_m=FIDUCIAL_OMEGA_M):
    """Empirical isolated-galaxy RAR with the study's evolved acceleration scale.

    gtot = gbar / [1 - exp(-sqrt(gbar/a0(z)))], in m s^-2.
    This forward parameterization assumes applicability of the isolated-galaxy
    RAR; it does not model external fields or establish a covariant theory.
    Its redshift/background domain is the same as predict().
    """
    _finite("gbar", gbar)
    if gbar <= 0:
        raise ValueError("gbar must be positive")
    a0 = predict(z, q, amplitude, omega_m)["a0_m_s2"]
    # Dividing square roots avoids underflow of gbar/a0 for tiny positive gbar.
    x = math.sqrt(gbar) / math.sqrt(a0)
    denominator = -math.expm1(-x)
    result = gbar / denominator
    if not math.isfinite(result) or result <= 0:
        raise ValueError("radial acceleration exceeds floating-point range")
    return result


def dimensional_hubble_acceleration(z, h0_km_s_mpc, omega_m=FIDUCIAL_OMEGA_M):
    """c H(z)/(2 pi), separate from the calibrated a0=A E(z)^q model."""
    _finite("h0_km_s_mpc", h0_km_s_mpc)
    if h0_km_s_mpc <= 0:
        raise ValueError("h0_km_s_mpc must be positive")
    result = C * (h0_km_s_mpc * 1000 / MPC_METRES) * expansion(z, omega_m) / (2 * math.pi)
    if not math.isfinite(result) or result <= 0:
        raise ValueError("dimensional acceleration exceeds floating-point range")
    return result


def prediction_document():
    """Deterministic predictions only: no measurements, fit, or likelihood."""
    return {
        "schema_version": 1,
        "kind": "phenomenological_predictions",
        "parameters": {"A_m_s2": FIDUCIAL_A, "omega_m": FIDUCIAL_OMEGA_M},
        "domain": {"z_min": 0, "z_max": 5},
        "assumptions": [
            "Flat matter plus constant Lambda background; radiation neglected.",
            "a0(z) = A E(z)^q; A is calibrated independently of H0.",
            "q=0 is also degenerate with a constant-Lambda-normalized scale in this background.",
            "q=1 tracks instantaneous H(z), with independently calibrated amplitude A.",
            "BTFR shifts apply only to isolated asymptotic deep-MOND systems with slope four.",
            "No covariant theory, observational fit, likelihood, or discovery is asserted.",
            "c H(z)/(2 pi) is a separate dimensional relation and is not the normalization used here."
        ],
        "units": {"a0_m_s2": "m s^-2", "a0_ratio_to_z0": "dimensionless",
                  "btfr_mass_intercept_shift_dex": "dex in baryonic mass at fixed velocity",
                  "velocity_at_fixed_baryonic_mass_shift_dex": "dex in velocity at fixed baryonic mass",
                  "local_da0_dz_m_s2": "m s^-2 per unit redshift"},
        "models": [
            {"q": q, "label": label, "local_da0_dz_m_s2": local_derivative(q),
             "predictions": [predict(z, q) for z in GRID]}
            for q, label in ((0.0, "constant"), (1.0, "instantaneous_H_tracking"))
        ]
    }


def _strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError(f"nonfinite JSON constant: {value}")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid_constant)


def documents_equal(expected, actual):
    """Compare JSON documents with exact structure/types and tolerant finite floats.

    Float tolerance accommodates platform libm rounding: rel_tol=1e-12,
    abs_tol=1e-300. An expected zero must remain exactly zero. Integers,
    booleans, strings, and null are exact; int and float remain distinct types.
    """
    if type(expected) is not type(actual):
        return False
    if isinstance(expected, dict):
        return (expected.keys() == actual.keys()
                and all(documents_equal(value, actual[key]) for key, value in expected.items()))
    if isinstance(expected, list):
        return (len(expected) == len(actual)
                and all(documents_equal(a, b) for a, b in zip(expected, actual)))
    if isinstance(expected, float):
        return (math.isfinite(expected) and math.isfinite(actual)
                and (actual == 0 if expected == 0 else
                     math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-300)))
    if expected is None or isinstance(expected, (str, int, bool)):
        return expected == actual
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    parser.add_argument("--check", action="store_true", help="verify existing output against deterministic predictions")
    args = parser.parse_args(argv)
    expected = prediction_document()
    if args.check:
        try:
            actual = _strict_json(args.output.read_text(encoding="utf-8"))
            if not documents_equal(expected, actual):
                raise ValueError("artifact differs from expected predictions or schema")
        except (OSError, ValueError) as exc:
            parser.exit(1, f"check failed: {exc}\n")
        print(f"verified {args.output}")
    else:
        args.output.write_text(json.dumps(expected, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
