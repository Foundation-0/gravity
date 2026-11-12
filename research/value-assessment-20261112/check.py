#!/usr/bin/env python3
"""Reproduce the four assessment probes without changing saved evidence."""
from __future__ import annotations
import hashlib
import json
import math
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
# Version labels do not describe scientific output.
ENVIRONMENT_KEYS = {'environment'}
# Roundoff diagnostics retain the control's accuracy boundary. Scientific
# observables, error curves, and all other numbers use the tighter comparison.
DIAGNOSTIC_LIMITS = {
    'continuity_relative_residual': 1e-9,
    'momentum_relative_residual': 1e-9,
    'time_reversal_relative_field_error': 1e-12,
    'modal_occupation_max_change': 1e-12,
    'high_k_mass_fraction_abs_k_gt_n_over_4': 1e-20,
    'resolution_2048_4096_max_absolute_difference': 1e-10,
    'max_formula_matrix_error': 2e-11,
    'max_self_stress_force_error': 2e-12,
    'quadrature_refinement_max_error': 1e-12,
}


def compare(actual, expected, location='root'):
    key = location.rsplit('.', 1)[-1]
    # Only the analytically null eigenvalues of the ideal fold are roundoff.
    match = re.fullmatch(r'convergences.mechanics.fold_rows\[(\d+)\].mandel_elastic_eigenvalues\[(\d+)\]', location)
    if match and int(match[2]) < (3 if int(match[1]) == 0 else 5):
        assert all(math.isfinite(v) and abs(v) < 1e-12 for v in (actual, expected)), location
        return
    match = re.fullmatch(r'convergences.mechanics.fold_rows\[(\d+)\].compatibility_smallest_three_singular_values\[(\d+)\]', location)
    if match and (int(match[1]) == 0 or int(match[2]) == 2):
        assert all(math.isfinite(v) and 0 <= v < 1e-12 for v in (actual, expected)), location
        return
    # Momentum and symmetry-center velocity vanish analytically in this control.
    if location.startswith('closure.') and key in {'momentum_mean', 'mean_velocity', 'central_velocity'}:
        assert all(math.isfinite(v) and abs(v) < 2e-12 for v in (actual, expected)), location
        return
    # Native finite-length verification differentiates nearly equal energies.
    # Its analytic acceptance criterion is 1e-4 in the author probe.
    if re.fullmatch(r'convergences.mechanics.finite_length_checks\[[0-2]\].relative_energy_hessian_error', location):
        assert all(math.isfinite(v) and 0 <= v < 1e-4 for v in (actual, expected)), location
        return
    if key in DIAGNOSTIC_LIMITS:
        for value in (actual, expected):
            assert isinstance(value, (float, int)) and not isinstance(value, bool), location
            assert math.isfinite(value) and 0 <= value < DIAGNOSTIC_LIMITS[key], (location, value)
    elif isinstance(expected, bool):
        assert isinstance(actual, bool) and actual == expected, (location, actual, expected)
    elif isinstance(expected, dict):
        assert isinstance(actual, dict) and actual.keys() == expected.keys(), location
        for key in expected:
            if key not in ENVIRONMENT_KEYS:
                compare(actual[key], expected[key], f'{location}.{key}')
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), location
        for i, (a, e) in enumerate(zip(actual, expected)):
            compare(a, e, f'{location}[{i}]')
    elif isinstance(expected, int):
        assert isinstance(actual, int) and not isinstance(actual, bool) and actual == expected, (location, actual, expected)
    elif isinstance(expected, float):
        assert isinstance(actual, (float, int)) and not isinstance(actual, bool), location
        assert math.isfinite(actual) and math.isfinite(expected), location
        assert math.isclose(actual, expected, rel_tol=1e-7, abs_tol=1e-20), (location, actual, expected)
    else:
        assert actual == expected, (location, actual, expected)



def mismatches(actual, expected, location):
    """Collect every leaf mismatch so a hosted run reports all portability gaps."""
    if isinstance(expected, dict) and isinstance(actual, dict) and actual.keys() == expected.keys():
        return [error for key in expected if key not in ENVIRONMENT_KEYS
                for error in mismatches(actual[key], expected[key], f'{location}.{key}')]
    if isinstance(expected, list) and isinstance(actual, list) and len(actual) == len(expected):
        return [error for i, (a, e) in enumerate(zip(actual, expected))
                for error in mismatches(a, e, f'{location}[{i}]')]
    try:
        compare(actual, expected, location)
        return []
    except AssertionError as error:
        return [str(error)]


def verify_inputs(root=HERE):
    manifest = json.loads((root / 'inputs/manifest.json').read_text())
    for item in manifest['files']:
        path = root / 'inputs' / item['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], item['path']


def main():
    verify_inputs()
    with tempfile.TemporaryDirectory(prefix='value-assessment-check-') as directory:
        temporary = Path(directory) / 'bundle'
        shutil.copytree(HERE, temporary)
        probes = [
            ('wave12', 'probe.py', 'evidence.json', ['--repo', str(temporary / 'inputs'), '--output', 'evidence.json']),
            ('closure', 'caustic_control.py', 'results.json', []),
            ('convergences', 'probe.py', 'evidence.json', []),
            ('observations', 'probe.py', 'results.json', ['--output', 'results.json']),
        ]
        failures = []
        for name, script, output, arguments in probes:
            work = temporary / name
            (work / output).unlink()
            result = subprocess.run([sys.executable, '-B', script, *arguments], cwd=work, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f'{name}: {result.stdout}\n{result.stderr}')
            errors = mismatches(json.loads((work / output).read_text()), json.loads((HERE / name / output).read_text()), name)
            failures.extend(errors)
            print(f'{"FAIL" if errors else "PASS"} {name}: regenerated {output}')
        assert not failures, '\n'.join(failures)
    print('PASS four probes and six immutable source hashes')


if __name__ == '__main__':
    main()
