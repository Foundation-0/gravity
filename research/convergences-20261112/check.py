#!/usr/bin/env python3
"""Regenerate nine probes in a temporary copy and check saved scientific results."""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PROBES = {
    'evidence': ('evidence_join.py', ['results.json']),
    'hidden-dynamics': ('hidden_dynamics.py', ['results.json', 'trajectories.csv']),
    'issue-5': ('issue5_checks.py', ['results.json']),
    'persistence': ('persistence_probes.py', ['results.json']),
    'relations': ('correlation_probe.py', ['results.json']),
    'repetition': ('graph_vs_geometry.py', ['graph-results.json']),
    'robustness': ('robustness_probes.py', ['results.json']),
    'scales': ('scale_probes.py', ['results.json']),
    'unclaimed': ('constraint_probes.py', ['results.json']),
}
# Environment labels do not describe a scientific result. All other keys count.
ENVIRONMENT_KEYS = {'numpy_version', 'sympy_version', 'python_version', 'python_executable'}
# These five residuals measure agreement of a finite-displacement Hessian with
# C.T @ C, not physical observables. At epsilon=1e-4 the symmetric difference
# has truncation and platform rounding error. Use the original probe's strict
# acceptance bound for both regenerated and saved residuals.
HESSIAN_RESIDUAL_LOCATIONS = {
    f'robustness/results.json.mechanics.rows[{index}].energy_hessian_discrepancy'
    for index in range(5)
}
HESSIAN_RESIDUAL_LIMIT = 3e-8


def compare(actual, expected, location):
    if isinstance(expected, dict):
        assert isinstance(actual, dict) and actual.keys() == expected.keys(), location
        for key in expected:
            if key not in ENVIRONMENT_KEYS:
                compare(actual[key], expected[key], f'{location}.{key}')
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), location
        for index, (a, e) in enumerate(zip(actual, expected)):
            compare(a, e, f'{location}[{index}]')
    elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
        assert isinstance(actual, (float, int)) and not isinstance(actual, bool), location
        assert math.isfinite(actual) and math.isfinite(expected), location
        if location in HESSIAN_RESIDUAL_LOCATIONS:
            assert 0 <= actual < HESSIAN_RESIDUAL_LIMIT, (location, actual)
            assert 0 <= expected < HESSIAN_RESIDUAL_LIMIT, (location, expected)
        else:
            assert math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-12), (location, actual, expected)
    else:
        assert actual == expected, (location, actual, expected)


def main():
    # Refuse changed historical inputs before any probe imports them.
    manifest = json.loads((HERE / 'inputs/manifest.json').read_text())
    for item in manifest['files']:
        path = HERE / item['bundle_path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], path
    with tempfile.TemporaryDirectory(prefix='convergences-check-') as directory:
        temporary = Path(directory) / 'bundle'
        shutil.copytree(HERE, temporary)
        for name, (script, outputs) in PROBES.items():
            work = temporary / 'probes' / name
            for output in outputs:
                (work / output).unlink()
            result = subprocess.run([sys.executable, '-B', str(work / script)], capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f'{name}: {result.stdout}\n{result.stderr}')
            for output in outputs:
                reference = HERE / 'probes' / name / output
                generated = work / output
                if output.endswith('.json'):
                    compare(json.loads(generated.read_text()), json.loads(reference.read_text()), f'{name}/{output}')
                else:
                    with generated.open(newline='') as stream:
                        actual = list(csv.reader(stream))
                    with reference.open(newline='') as stream:
                        expected = list(csv.reader(stream))
                    assert actual[0] == expected[0] and len(actual) == len(expected), output
                    compare([[float(v) for v in row] for row in actual[1:]],
                            [[float(v) for v in row] for row in expected[1:]], f'{name}/{output}')
            print(f'PASS {name}: {", ".join(outputs)}')
    print('PASS all nine probes; historical inputs match pinned SHA-256 digests')


if __name__ == '__main__':
    main()
