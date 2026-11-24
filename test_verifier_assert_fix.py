"""Regression test for the verifier assert fault (Foundation-0/gravity).

Stacked on PR #28, which already fixed the two named faults
(``verify_all.py --check`` rewriting its certificate, and the bare
``assert`` comparisons in the nine wave scripts' ``emit_or_verify``).
This test covers the remainder only: the 71 bare asserts left in the
standing verifiers (``run_assertions`` in ``verify_all.py``, the wave
``main()`` value-range checks, and the formal rational verifier), plus
the JSON-decode / non-dict / missing-sha guards added to
``emit_or_verify`` on top of #28.

The fault: proof checks written as bare ``assert`` are skipped under
``python3 -O``, so a corrupted certificate printed CHECK OK / VERIFIED
and exited 0.

This test follows the original probe: corrupt one digit of a certificate
in a scratch copy, run the tool bare and under ``-O``, and require a
non-zero exit with the file unchanged. It also requires valid
certificates to still verify and ``--check`` runs to leave every checked
file byte-identical. It does not duplicate ``test_check_modes.py``
(#28's corruption probe for ``emit_or_verify``).

Only the standard library is used. No bare ``assert`` appears in this
file: every check uses ``unittest`` assertion methods, which ``-O``
cannot remove.

Wave 7 is excluded from the automated sweep: its ``--check`` run takes
about 155 seconds (it refits the catalog). Its ``emit_or_verify`` is
byte-identical to the other waves' and was verified by hand instead.
"""
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# (script, certificate file) pairs in the standing verification chain.
FAST_CHECKS = [
    ("verify_all.py", "results/certificates.json"),
    ("wave3_empirical_audit.py", "results/wave3_empirical_certificates.json"),
    ("wave4_unified_field_solver.py", "results/wave4_unified_certificates.json"),
    ("wave5_unified_forces_stochastic_qm.py", "results/wave5_forces_stochastic_certificates.json"),
    ("wave6_convergence_unification.py", "results/wave6_convergence_certificates.json"),
    ("wave9_scale_convergence_audit.py", "results/wave9_scale_convergence_certificates.json"),
    ("wave10_covariant_jeans_unification.py", "results/wave10_covariant_jeans_certificates.json"),
    ("wave11_machian_pairing_unification.py", "results/wave11_machian_pairing_certificates.json"),
    ("wave12_cosmic_dawn_quasar_collapse.py", "results/wave12_cosmic_dawn_quasar_certificates.json"),
]

STANDING_VERIFIERS = [
    "verify_all.py",
    "wave3_empirical_audit.py",
    "wave4_unified_field_solver.py",
    "wave5_unified_forces_stochastic_qm.py",
    "wave6_convergence_unification.py",
    "wave7_group_cluster_threshold_audit.py",
    "wave9_scale_convergence_audit.py",
    "wave10_covariant_jeans_unification.py",
    "wave11_machian_pairing_unification.py",
    "wave12_cosmic_dawn_quasar_collapse.py",
    "formal/verify_exact_rational_proofs.py",
]

BARE_ASSERT = re.compile(r"(?m)^\s*assert[ (]")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VerifierAssertFixTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="gravity-assert-fix-"))
        shutil.copytree(
            ROOT, self.tmp, ignore=shutil.ignore_patterns(".git", "__pycache__"),
            dirs_exist_ok=True,
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_tool(self, script, args=(), optimise=False):
        cmd = [sys.executable]
        if optimise:
            cmd.append("-O")
        cmd += [str(self.tmp / script), *args]
        return subprocess.run(cmd, cwd=self.tmp, capture_output=True, text=True, timeout=600)

    def corrupt_one_digit(self, cert_rel, pattern, replacement):
        path = self.tmp / cert_rel
        text = path.read_text(encoding="utf-8")
        new_text, n = re.subn(pattern, replacement, text, count=1)
        self.assertEqual(n, 1, f"corruption pattern did not match once in {cert_rel}")
        self.assertNotEqual(new_text, text)
        path.write_text(new_text, encoding="utf-8")
        return sha256(path)

    def test_no_bare_asserts_in_standing_verifiers(self):
        for rel in STANDING_VERIFIERS:
            text = (ROOT / rel).read_text(encoding="utf-8")
            found = BARE_ASSERT.findall(text)
            self.assertEqual(found, [], f"{rel} still contains bare assert statements")

    def test_valid_certificates_still_verify(self):
        for script, cert_rel in FAST_CHECKS:
            before = sha256(self.tmp / cert_rel)
            result = self.run_tool(script, ("--check",))
            self.assertEqual(result.returncode, 0, f"{script} --check failed on a valid certificate: {result.stdout} {result.stderr}")
            self.assertIn("CHECK OK", result.stdout, f"{script} --check did not print CHECK OK")
            self.assertEqual(sha256(self.tmp / cert_rel), before, f"{script} --check rewrote {cert_rel}")

    def test_valid_certificates_still_verify_under_O(self):
        for script, cert_rel in [
            ("verify_all.py", "results/certificates.json"),
            ("wave10_covariant_jeans_unification.py", "results/wave10_covariant_jeans_certificates.json"),
        ]:
            result = self.run_tool(script, ("--check",), optimise=True)
            self.assertEqual(result.returncode, 0, f"{script} --check under -O failed on a valid certificate: {result.stdout} {result.stderr}")
            self.assertIn("CHECK OK", result.stdout)

    def test_formal_verifier_still_verifies_bare_and_O(self):
        for optimise in (False, True):
            result = self.run_tool("formal/verify_exact_rational_proofs.py", optimise=optimise)
            self.assertEqual(result.returncode, 0, f"formal verifier failed (optimise={optimise}): {result.stdout} {result.stderr}")
            self.assertIn("VERIFIED", result.stdout)

    def test_corrupted_verify_all_check_fails_bare_and_O(self):
        corrupted_hash = self.corrupt_one_digit(
            "results/certificates.json",
            r'"coord_fractal_Df2_btfr_slope": 2',
            '"coord_fractal_Df2_btfr_slope": 9',
        )
        for optimise in (False, True):
            result = self.run_tool("verify_all.py", ("--check",), optimise=optimise)
            self.assertNotEqual(result.returncode, 0, f"verify_all.py --check passed a corrupted certificate (optimise={optimise})")
            self.assertIn("CHECK FAILED", result.stdout + result.stderr)
            self.assertEqual(
                sha256(self.tmp / "results/certificates.json"),
                corrupted_hash,
                "verify_all.py --check rewrote the corrupted certificate",
            )

    def test_corrupted_wave10_check_fails_bare_and_O(self):
        corrupted_hash = self.corrupt_one_digit(
            "results/wave10_covariant_jeans_certificates.json",
            r'"sigma_star_z0_kms": 185\.59',
            '"sigma_star_z0_kms": 195.59',
        )
        for optimise in (False, True):
            result = self.run_tool(
                "wave10_covariant_jeans_unification.py", ("--check",), optimise=optimise
            )
            self.assertNotEqual(result.returncode, 0, f"wave10 --check passed a corrupted certificate (optimise={optimise})")
            self.assertIn("CHECK FAILED", result.stdout + result.stderr)
            self.assertEqual(
                sha256(self.tmp / "results/wave10_covariant_jeans_certificates.json"),
                corrupted_hash,
                "wave10 --check rewrote the corrupted certificate",
            )

    def test_run_assertions_rejects_tampered_cert_bare_and_O(self):
        # Remainder behaviour: run_assertions held 13 bare asserts.
        # Under -O the old code accepted a tampered certificate silently.
        driver = (
            "import json, sys\n"
            f"sys.path.insert(0, {str(self.tmp)!r})\n"
            "import verify_all\n"
            f"cert = json.loads(open({str(self.tmp / 'results/certificates.json')!r}).read())\n"
            "cert['check_1_dichotomy']['coord_fractal_Df2_btfr_slope'] = 9.0\n"
            "try:\n"
            "    verify_all.run_assertions(cert)\n"
            "except SystemExit as exc:\n"
            "    print(f'REJECTED: {exc}')\n"
            "    raise SystemExit(1)\n"
            "print('ACCEPTED')\n"
        )
        driver_path = self.tmp / "_run_assertions_driver.py"
        driver_path.write_text(driver, encoding="utf-8")
        for optimise in (False, True):
            cmd = [sys.executable]
            if optimise:
                cmd.append("-O")
            cmd.append(str(driver_path))
            result = subprocess.run(cmd, cwd=self.tmp, capture_output=True,
                                    text=True, timeout=600)
            self.assertNotEqual(result.returncode, 0,
                                f"run_assertions accepted a tampered cert (optimise={optimise})")
            self.assertIn("REJECTED", result.stdout,
                          f"run_assertions did not reject explicitly (optimise={optimise})")

    def test_rat_interval_rejects_invalid_bounds(self):
        # Remainder behaviour: RatInterval input checks were bare asserts.
        spec = importlib.util.spec_from_file_location(
            "formal_verifier", self.tmp / "formal/verify_exact_rational_proofs.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["formal_verifier"] = mod
        spec.loader.exec_module(mod)
        with self.assertRaises(ValueError):
            mod.RatInterval(Fraction(2), Fraction(1))
        with self.assertRaises(ValueError):
            mod.RatInterval(Fraction(-1), Fraction(1)) * mod.RatInterval(Fraction(1), Fraction(2))
        with self.assertRaises(ValueError):
            mod.RatInterval(Fraction(1), Fraction(2)) / mod.RatInterval(Fraction(0), Fraction(1))
        # Valid bounds still construct.
        iv = mod.RatInterval(Fraction(1), Fraction(2))
        self.assertEqual(iv.lo, Fraction(1))
        self.assertEqual(iv.hi, Fraction(2))

    def test_emit_or_verify_guards_bare_and_O(self):
        # Guards added on top of #28's emit_or_verify: non-JSON input,
        # a JSON value that is not an object, and a missing sha field
        # must all fail explicitly instead of raising a bare traceback.
        cert_rel = "results/wave10_covariant_jeans_certificates.json"
        path = self.tmp / cert_rel
        original = path.read_bytes()
        cases = [
            (b"not json at all\n", "not valid JSON"),
            (b"[1, 2, 3]\n", "not a JSON object"),
        ]
        obj = json.loads(original)
        obj.pop("sha256_canonical", None)
        cases.append((json.dumps(obj, indent=2).encode("utf-8") + b"\n",
                      "no sha256_canonical field"))
        try:
            for payload, fragment in cases:
                path.write_bytes(payload)
                corrupted_hash = sha256(path)
                for optimise in (False, True):
                    result = self.run_tool(
                        "wave10_covariant_jeans_unification.py", ("--check",),
                        optimise=optimise)
                    self.assertNotEqual(result.returncode, 0,
                                        f"wave10 --check passed malformed input {fragment!r} (optimise={optimise})")
                    self.assertIn("CHECK FAILED", result.stdout + result.stderr)
                    self.assertIn(fragment, result.stdout + result.stderr)
                    self.assertEqual(sha256(path), corrupted_hash,
                                     "wave10 --check rewrote the malformed certificate")
        finally:
            path.write_bytes(original)
        self.assertEqual(sha256(path), sha256(self.tmp / cert_rel))

    def test_missing_certificate_fails_bare_and_O(self):
        for script, cert_rel in [
            ("verify_all.py", "results/certificates.json"),
            ("wave10_covariant_jeans_unification.py", "results/wave10_covariant_jeans_certificates.json"),
        ]:
            (self.tmp / cert_rel).unlink()
            for optimise in (False, True):
                result = self.run_tool(script, ("--check",), optimise=optimise)
                self.assertNotEqual(result.returncode, 0, f"{script} --check passed with a missing certificate (optimise={optimise})")
                self.assertIn("CHECK FAILED", result.stdout + result.stderr)
                self.assertIn("missing certificate file", (result.stdout + result.stderr).lower())
            self.assertFalse((self.tmp / cert_rel).exists(), f"{script} --check recreated the missing certificate")


if __name__ == "__main__":
    unittest.main()
