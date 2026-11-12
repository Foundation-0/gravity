"""Regression checks for the observed Linux/Mac finite-difference residual."""
import unittest

from check import DIAGNOSTIC_LIMITS, compare


class ComparisonPolicyTests(unittest.TestCase):
    location = 'robustness/results.json.mechanics.rows[0].energy_hessian_discrepancy'
    saved = 7.645866162420134e-10

    def test_observed_platform_residual_passes(self):
        compare(7.631495435589386e-10, self.saved, self.location)

    def test_observed_aest_platform_residual_passes(self):
        compare(5.862759167030163e-10, 5.410445425013677e-10,
                'robustness/results.json.aest_current.maximum_absolute_component_error')

    def test_all_six_diagnostic_bounds_reject_deterioration(self):
        self.assertEqual(len(DIAGNOSTIC_LIMITS), 6)
        for location, limit in DIAGNOSTIC_LIMITS.items():
            for value in (limit, 10 * limit, -1e-10, float('nan'), float('inf'), True, False, None):
                with self.subTest(location=location, value=value):
                    with self.assertRaises(AssertionError):
                        compare(value, 0., location)
                    with self.assertRaises(AssertionError):
                        compare(0., value, location)

    def test_material_deterioration_fails(self):
        for residual in (3e-8, 1e-6, -1e-10, float('nan'), float('inf')):
            with self.subTest(residual=residual), self.assertRaises(AssertionError):
                compare(residual, self.saved, self.location)
        with self.assertRaises(AssertionError):
            compare(self.saved, 1e-6, self.location)

    def test_boolean_outputs_require_booleans(self):
        for actual, expected in ((1, True), (0, False), (True, 1), (False, 0)):
            with self.subTest(actual=actual, expected=expected), self.assertRaises(AssertionError):
                compare(actual, expected, 'hidden-dynamics/results.json.all_assertions_passed')
        compare(True, True, 'hidden-dynamics/results.json.all_assertions_passed')
        compare(False, False, 'example.false_output')

    def test_other_fields_keep_strict_comparison(self):
        with self.assertRaises(AssertionError):
            compare(7.631495435589386e-10, self.saved,
                    'robustness/results.json.mechanics.rows[0].sum_omega_fourth')
        with self.assertRaises(AssertionError):
            compare('changed', 'original', 'evidence/results.json.status')


if __name__ == '__main__':
    unittest.main()
