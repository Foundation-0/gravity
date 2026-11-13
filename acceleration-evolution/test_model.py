"""Analytic and artifact-contract tests; no external packages or data."""
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import model


class PredictionTests(unittest.TestCase):
    def test_present_epoch_normalization_and_constant_model(self):
        for q in (-3, 0, 1, 2.5):
            self.assertEqual(model.predict(0, q)["a0_m_s2"], model.FIDUCIAL_A)
        for z in model.GRID:
            p = model.predict(z, 0)
            self.assertEqual(p["a0_ratio_to_z0"], 1)
            self.assertEqual(p["btfr_mass_intercept_shift_dex"], 0)

    def test_matter_dominated_limit(self):
        # Independent matter-only result E=(1+z)^(3/2), approached from allowed Om<1.
        z = 3
        self.assertAlmostEqual(model.expansion(z, 1 - 1e-12), (1 + z)**1.5, places=10)

    def test_btfr_shifts(self):
        p = model.predict(1.44, 1.7)
        r = p["a0_ratio_to_z0"]
        # M_b=V^4/(G a0): fixed-V mass ratio=1/r; fixed-M V ratio=r^(1/4).
        self.assertAlmostEqual(10**p["btfr_mass_intercept_shift_dex"], 1/r)
        self.assertAlmostEqual(10**p["velocity_at_fixed_baryonic_mass_shift_dex"], r**0.25)

    def test_local_derivative(self):
        for q in (-1.2, 0, 1, 2.3):
            h = 1e-5
            f = lambda z: model.predict(z, q)["a0_m_s2"]
            numerical = (-3*f(0) + 4*f(h) - f(2*h))/(2*h)
            self.assertAlmostEqual(numerical/model.FIDUCIAL_A,
                                   model.local_derivative(q)/model.FIDUCIAL_A, places=8)

    def test_hubble_relation_is_separate(self):
        expected = 299792458 * (70 * 1000 / 3.085677581491367e22)/(2*math.pi)
        self.assertAlmostEqual(model.dimensional_hubble_acceleration(0, 70)/expected, 1)
        self.assertNotEqual(expected, model.predict(0, 1)["a0_m_s2"])
        self.assertAlmostEqual(model.dimensional_hubble_acceleration(2, 70)/expected,
                               model.predict(2, 1)["a0_ratio_to_z0"])

    def test_rar_acceleration_limits(self):
        a0 = model.FIDUCIAL_A
        high = a0 * 1e6
        self.assertEqual(model.radial_acceleration(high, 0), high)
        deep = a0 * 1e-16
        self.assertAlmostEqual(model.radial_acceleration(deep, 0)/math.sqrt(deep*a0),
                               1, places=7)
        # expm1 and square-root division retain subnormal positive inputs.
        self.assertGreater(model.radial_acceleration(5e-324, 0), 0)

    def test_rar_evolution_and_invalid_inputs(self):
        values = [model.radial_acceleration(1e-11, 1, q=q) for q in (-1, 0, 1)]
        self.assertLess(values[0], values[1])
        self.assertLess(values[1], values[2])
        for bad in (0, -1, float("nan"), float("inf"), True, None, "1"):
            with self.subTest(gbar=bad), self.assertRaises(ValueError):
                model.radial_acceleration(bad, 0)
        for kwargs in ({"z": 6}, {"q": float("nan")}, {"amplitude": -1},
                       {"omega_m": 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                model.radial_acceleration(**({"gbar": 1e-11, "z": 1} | kwargs))

    def test_invalid_inputs(self):
        for bad in (float("nan"), float("inf"), -float("inf"), True, "1", None):
            for kwargs in ({"z": bad, "q": 1}, {"z": 1, "q": bad},
                           {"z": 1, "q": 1, "amplitude": bad},
                           {"z": 1, "q": 1, "omega_m": bad}):
                with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                    model.predict(**kwargs)
        for kwargs in ({"z": -0.1}, {"z": 5.1}, {"amplitude": 0},
                       {"amplitude": -1}, {"omega_m": 0}, {"omega_m": 1}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                model.predict(**({"z": 1, "q": 1} | kwargs))
        for q in (1e308, -1e308):
            with self.assertRaises(ValueError):
                model.predict(5, q)

    def test_artifact_check_is_strict_and_read_only(self):
        script = Path(model.__file__).resolve()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/"predictions.json"
            command = [sys.executable, str(script), "--output", str(output)]
            def run(*args):
                return subprocess.run(command + list(args), capture_output=True, text=True)
            self.assertNotEqual(run("--check").returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(run().returncode, 0)
            original = output.read_bytes()
            self.assertEqual(run("--check").returncode, 0)
            self.assertEqual(output.read_bytes(), original)
            doc = json.loads(original)
            doc["schema_version"] = True
            output.write_text(json.dumps(doc))
            stale = output.read_bytes()
            self.assertNotEqual(run("--check").returncode, 0)
            self.assertEqual(output.read_bytes(), stale)
            doc["schema_version"] = 1
            doc["models"][1]["predictions"][2]["a0_m_s2"] *= 2
            output.write_text(json.dumps(doc))
            self.assertNotEqual(run("--check").returncode, 0)
            output.write_text('{"schema_version":1,"schema_version":1}')
            self.assertNotEqual(run("--check").returncode, 0)

    def test_documents_equal_float_rounding(self):
        expected = {"schema": 1, "rows": [1.2e-10, 0.0, "value", None, True]}
        actual = {"schema": 1, "rows": [math.nextafter(1.2e-10, math.inf), 0.0, "value", None, True]}
        self.assertTrue(model.documents_equal(expected, actual))
        actual["rows"][0] = 1.2e-10 * (1 + 1e-9)
        self.assertFalse(model.documents_equal(expected, actual))
        self.assertFalse(model.documents_equal(0.0, 1e-310))
        self.assertFalse(model.documents_equal(float("nan"), float("nan")))
        self.assertFalse(model.documents_equal(float("inf"), float("inf")))

    def test_documents_equal_exact_schema(self):
        for expected, actual in ((1, True), (1, 1.0), (False, 0),
                                 ({"a": 1}, {"b": 1}),
                                 ({"a": 1}, {"a": 1, "b": 2}),
                                 ([1], [1, 2]), ([1], (1,)), (None, "null")):
            with self.subTest(expected=expected, actual=actual):
                self.assertFalse(model.documents_equal(expected, actual))


if __name__ == "__main__":
    unittest.main()
