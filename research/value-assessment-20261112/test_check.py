"""Protect result comparisons and refusal of changed historical inputs."""
from pathlib import Path
import shutil
import tempfile
import unittest
from check import compare, verify_inputs, HERE, mismatches


class ComparisonTests(unittest.TestCase):
    def test_roundoff_and_environment(self):
        compare({'x': 1 + 1e-9, 'environment': {'numpy': 'new'}},
                {'x': 1., 'environment': {'numpy': 'old'}})

    def test_changed_science_or_structure_is_rejected(self):
        for actual in ({'x': 1.01}, {'x': True}, {'x': float('nan')}, {'y': 1.}):
            with self.assertRaises(AssertionError):
                compare(actual, {'x': 1.})
        with self.assertRaises(AssertionError):
            compare(False, True)

    def test_small_scientific_signal_is_preserved(self):
        for actual in (0., 8e-11):
            with self.assertRaises(AssertionError):
                compare(actual, 4.19e-11, "wave12.compactness")
        with self.assertRaises(AssertionError):
            compare(0., 1e-16, "convergences.eta")

    def test_large_roundoff_diagnostic_is_rejected(self):
        with self.assertRaises(AssertionError):
            compare(1e-4, 1e-12, 'closure.momentum_relative_residual')

    def test_all_mismatches_are_collected(self):
        errors = mismatches({"x": 0., "y": False}, {"x": 4.19e-11, "y": True}, "probe")
        self.assertEqual(len(errors), 2)

    def test_native_finite_length_diagnostic_boundary(self):
        path = "convergences.mechanics.finite_length_checks[0].relative_energy_hessian_error"
        compare(3.1972696962664237e-7, 3.197457694573648e-7, path)
        with self.assertRaises(AssertionError):
            compare(1e-3, 3.197457694573648e-7, path)

    def test_observation_null_controls_stay_scoped(self):
        with self.assertRaises(AssertionError):
            compare(False, 5.5284e-14, "observations.designs.exact_deep_limit.singular_values[2]")
        compare(5.6785e-14, 5.5284e-14, "observations.designs.exact_deep_limit.singular_values[2]")
        compare(-6e-16, 9e-16, "observations.injections.physical_evolution.exact_deep_fit_assuming_B1_C1_s0_u0.theta[0]")
        compare(3.3e-16, 1.9e-16, "observations.checks[13].evidence")
        for path, actual, expected in [
            ("observations.designs.exact_deep_limit.singular_values[2]", 1e-5, 5e-14),
            ("observations.checks[13].evidence", 1e-5, 1.9e-16),
            ("observations.heldout.training_max_residual_dex", 0., .00109),
            ("observations.heldout.held_out_high_acceleration_max_residual_dex", 0., .360),
            ("observations.injections.mass_drift_only.finite_deep_fit_assuming_B1_C1_s0_u0.theta[0]", 0., .001),
        ]:
            with self.assertRaises(AssertionError):
                compare(actual, expected, path)

    def test_changed_input_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(HERE / 'inputs', root / 'inputs')
            verify_inputs(root)
            path = root / 'inputs/wave12_cosmic_dawn_quasar_collapse.py'
            path.write_text(path.read_text() + '\n# changed\n')
            with self.assertRaises(AssertionError):
                verify_inputs(root)


if __name__ == '__main__':
    unittest.main()
