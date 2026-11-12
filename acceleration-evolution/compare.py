"""Reproduce central-curve diagnostics without inventing an observation likelihood."""
import argparse
import hashlib
import json
import math
from pathlib import Path

from model import FIDUCIAL_A, FIDUCIAL_OMEGA_M, _strict_json, documents_equal, expansion, predict

ROOT = Path(__file__).resolve().parent


def comparison_document(evidence_path=ROOT / "evidence.json"):
    raw = evidence_path.read_bytes()
    data = _strict_json(raw.decode("utf-8"))
    lo, hi = data["primary_source"]["sample_redshift_limits"]
    e_growth = expansion(hi) / expansion(lo)
    curves = []
    grid = [lo, 0.5, 0.75, 1.0, hi]
    for item in data["published_linear_curves"]:
        a, b = item["intercept_m_s2"], item["slope_m_s2_per_redshift"]
        values = [a + b * z for z in grid]
        if any(not math.isfinite(v) or v <= 0 for v in values):
            raise ValueError("published central curve must remain positive and finite")
        growth = values[-1] / values[0]
        curves.append({
            "id": item["id"], "independence_group": item["independence_group"],
            "interval_growth": growth,
            "growth_relative_to_H_tracking": growth / e_growth,
            "endpoint_equivalent_q_NOT_a_fit": math.log(growth) / math.log(e_growth),
            "values": [{"z": z, "a0_m_s2": value,
                        "ratio_to_low_boundary": value / values[0]}
                       for z, value in zip(grid, values)],
        })
    return {
        "schema_version": 1,
        "kind": "published_central_curve_diagnostic",
        "evidence_sha256": hashlib.sha256(raw).hexdigest(),
        "parameters": {"omega_m": FIDUCIAL_OMEGA_M, "benchmark_A_m_s2": FIDUCIAL_A},
        "interval": [lo, hi],
        "interpretation": [
            "Endpoints evaluate published fitted curves at sample boundaries, not measured endpoint galaxies.",
            "The equivalent q reproduces only endpoint growth; it is not a best fit or posterior estimate.",
            "Both reconstructions use the same galaxies and are not independent observations.",
            "No covariance, confidence band, chi-squared, p-value, Bayes factor or discovery significance is computed.",
            "Summary intervals are preserved in evidence.json without converting 95 percent coverage to 1 sigma."
        ],
        "constant_interval_growth": 1.0,
        "H_tracking_interval_growth": e_growth,
        "published_curves": curves,
        "benchmark_predictions": [predict(z, 1) for z in grid],
        "H_shape_background_sensitivity": [
            {"omega_m": om, "interval_growth": expansion(hi, om) / expansion(lo, om)}
            for om in (0.30, 0.315, 0.33)
        ],
        "inference_status": "Raw-data and covariance inference not performed; publication-summary comparison only"
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "comparison.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    expected = comparison_document()
    if args.check:
        try:
            actual = _strict_json(args.output.read_text())
            if not documents_equal(expected, actual):
                raise ValueError("stale comparison or changed source transcription")
        except (OSError, ValueError) as exc:
            parser.exit(1, f"check failed: {exc}\n")
        print("verified comparison")
    else:
        args.output.write_text(json.dumps(expected, indent=2, allow_nan=False) + "\n")
        print("wrote comparison")


if __name__ == "__main__":
    main()
