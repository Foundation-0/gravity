"""Protect result comparisons and refusal of changed historical inputs."""
from pathlib import Path
import shutil
import tempfile
import unittest
from check import compare, verify_inputs, HERE


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
