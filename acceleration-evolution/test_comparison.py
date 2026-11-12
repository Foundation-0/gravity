"""Independent checks of the published-summary transformation and stale evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from compare import ROOT, comparison_document


class ComparisonTests(unittest.TestCase):
    def test_ratios_and_no_statistical_inference(self):
        result = comparison_document()
        dc14, mond = result["published_curves"]
        self.assertAlmostEqual(dc14["interval_growth"], 3.2896 / 1.5247, places=12)
        self.assertAlmostEqual(mond["interval_growth"], 2.758 / 1.426, places=12)
        self.assertAlmostEqual(result["H_tracking_interval_growth"]**2,
                               (0.315 * 2.44**3 + 0.685) / (0.315 * 1.33**3 + 0.685), places=12)
        self.assertEqual(dc14["independence_group"], mond["independence_group"])
        self.assertNotIn("chi_squared", result)
        self.assertNotIn("likelihood", result)

    def test_changed_transcription_invalidates_artifact(self):
        original = comparison_document()
        with tempfile.TemporaryDirectory() as folder:
            changed = Path(folder) / "evidence.json"
            source = json.loads((ROOT / "evidence.json").read_text())
            source["published_linear_curves"][0]["slope_m_s2_per_redshift"] = 1.0e-10
            changed.write_text(json.dumps(source))
            result = comparison_document(changed)
            self.assertNotEqual(result["evidence_sha256"], original["evidence_sha256"])
            self.assertNotEqual(result["published_curves"][0]["interval_growth"], original["published_curves"][0]["interval_growth"])
            output = Path(folder) / "comparison.json"
            output.write_text(json.dumps(result))
            before = output.read_bytes()
            proc = subprocess.run([sys.executable, str(ROOT / "compare.py"), "--check", "--output", str(output)], capture_output=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(before, output.read_bytes())


if __name__ == "__main__":
    unittest.main()
