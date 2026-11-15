"""Check modes must fail on a corrupted certificate, with and without `python -O`.

Run from the repository root:
    python3 -B -m unittest test_check_modes -v

Each case copies one generator and its certificate into a temporary directory,
changes one stored value, and runs the generator's `--check`. The run must exit
non-zero, and the stored file must stay as it was (check modes do not write).
`wave7_group_cluster_threshold_audit.py` takes about a minute per run, so it is
covered only by the static test that its `emit_or_verify` has no bare `assert`.
"""
import ast
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (script, certificate file) pairs. All have a `--check` mode.
CASES = [
    ("verify_all.py", "certificates.json"),
    ("wave3_empirical_audit.py", "wave3_empirical_certificates.json"),
    ("wave4_unified_field_solver.py", "wave4_unified_certificates.json"),
    ("wave5_unified_forces_stochastic_qm.py", "wave5_forces_stochastic_certificates.json"),
    ("wave6_convergence_unification.py", "wave6_convergence_certificates.json"),
    ("wave9_scale_convergence_audit.py", "wave9_scale_convergence_certificates.json"),
    ("wave10_covariant_jeans_unification.py", "wave10_covariant_jeans_certificates.json"),
    ("wave11_machian_pairing_unification.py", "wave11_machian_pairing_certificates.json"),
    ("wave12_cosmic_dawn_quasar_collapse.py", "wave12_cosmic_dawn_quasar_certificates.json"),
]
ALL_WAVE_SCRIPTS = sorted(p.name for p in ROOT.glob("wave*.py"))


def bump_first_number(obj):
    """Change the first float or int found (not a bool) and report whether one was found."""
    items = obj.items() if isinstance(obj, dict) else enumerate(obj)
    for key, value in list(items):
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            obj[key] = value + 1
            return True
        if isinstance(value, (dict, list)) and bump_first_number(value):
            return True
    return False


def run_check(workdir: Path, script: str, optimized: bool):
    cmd = [sys.executable, "-B"] + (["-O"] if optimized else []) + [str(workdir / script), "--check"]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=workdir)


class CorruptedCertificate(unittest.TestCase):
    def prepare(self, script: str, cert_name: str) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="check-modes-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        for source in ROOT.glob("*.py"):  # scripts import one another
            shutil.copy(source, tmp / source.name)
        (tmp / "results").mkdir()
        shutil.copy(ROOT / "results" / cert_name, tmp / "results" / cert_name)
        return tmp

    def test_clean_certificates_pass(self):
        for script, cert_name in CASES:
            with self.subTest(script=script):
                tmp = self.prepare(script, cert_name)
                result = run_check(tmp, script, optimized=False)
                self.assertEqual(result.returncode, 0, result.stderr[-400:])
                self.assertIn("CHECK OK", result.stdout)

    def test_corrupted_value_fails_with_and_without_optimize(self):
        for script, cert_name in CASES:
            for optimized in (False, True):
                with self.subTest(script=script, optimized=optimized):
                    tmp = self.prepare(script, cert_name)
                    path = tmp / "results" / cert_name
                    data = json.loads(path.read_text(encoding="utf-8"))
                    self.assertTrue(bump_first_number(data))
                    # Keep the stored sha256_canonical so only the data differs.
                    corrupted = json.dumps(data, indent=2) + "\n"
                    path.write_text(corrupted, encoding="utf-8")
                    result = run_check(tmp, script, optimized)
                    self.assertNotEqual(result.returncode, 0, result.stdout[-400:])
                    self.assertNotIn("CHECK OK", result.stdout)
                    self.assertEqual(path.read_text(encoding="utf-8"), corrupted, "check mode wrote the file")

    def test_recomputed_sha_alone_does_not_hide_a_value_change(self):
        # A corrupted value with a matching, recomputed checksum must still fail the
        # byte comparison against the fresh computation.
        import hashlib
        script, cert_name = "wave6_convergence_unification.py", "wave6_convergence_certificates.json"
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                tmp = self.prepare(script, cert_name)
                path = tmp / "results" / cert_name
                data = json.loads(path.read_text(encoding="utf-8"))
                data.pop("sha256_canonical")
                self.assertTrue(bump_first_number(data))
                canonical = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
                data["sha256_canonical"] = hashlib.sha256(canonical).hexdigest()
                path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                result = run_check(tmp, script, optimized)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("CHECK OK", result.stdout)

    def test_missing_certificate_fails_with_optimize(self):
        script, cert_name = "wave6_convergence_unification.py", "wave6_convergence_certificates.json"
        tmp = self.prepare(script, cert_name)
        (tmp / "results" / cert_name).unlink()
        result = run_check(tmp, script, optimized=True)
        self.assertNotEqual(result.returncode, 0)

    def test_verify_all_check_does_not_rewrite(self):
        tmp = self.prepare("verify_all.py", "certificates.json")
        path = tmp / "results" / "certificates.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["schema"] = "stale"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        before = path.read_bytes()
        result = run_check(tmp, "verify_all.py", optimized=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(path.read_bytes(), before)


class NoBareAssertInEmitOrVerify(unittest.TestCase):
    def test_every_wave_script(self):
        self.assertEqual(len(ALL_WAVE_SCRIPTS), 9)
        for name in ALL_WAVE_SCRIPTS:
            with self.subTest(script=name):
                tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
                funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "emit_or_verify"]
                self.assertEqual(len(funcs), 1)
                asserts = [n for n in ast.walk(funcs[0]) if isinstance(n, ast.Assert)]
                self.assertEqual(asserts, [])


if __name__ == "__main__":
    unittest.main()
