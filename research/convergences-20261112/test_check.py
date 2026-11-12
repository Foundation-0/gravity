"""Regression checks for the observed Linux/Mac finite-difference residual."""
import unittest

from check import compare


class ComparisonPolicyTests(unittest.TestCase):
    location = 'robustness/results.json.mechanics.rows[0].energy_hessian_discrepancy'
    saved = 7.645866162420134e-10

    def test_observed_platform_residual_passes(self):
        compare(7.631495435589386e-10, self.saved, self.location)

    def test_material_deterioration_fails(self):
        for residual in (3e-8, 1e-6, -1e-10, float('nan'), float('inf')):
            with self.subTest(residual=residual), self.assertRaises(AssertionError):
                compare(residual, self.saved, self.location)
        with self.assertRaises(AssertionError):
            compare(self.saved, 1e-6, self.location)

    def test_other_fields_keep_strict_comparison(self):
        with self.assertRaises(AssertionError):
            compare(7.631495435589386e-10, self.saved,
                    'robustness/results.json.mechanics.rows[0].sum_omega_fourth')
        with self.assertRaises(AssertionError):
            compare('changed', 'original', 'evidence/results.json.status')


if __name__ == '__main__':
    unittest.main()
