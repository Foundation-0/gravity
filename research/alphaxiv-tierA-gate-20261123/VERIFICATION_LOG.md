# Tier A verification gate — Foundation-0/gravity (alphaXiv publishing)

Gate for `aska-digital/corpus#134` Tier A: re-run `verify_all.py` + `SHA256SUMS`
and audit against `CLAIMS.md` and `WAVE11_12_CORRECTIONS.md` before any
monograph is uploaded. Run 23 November 2026 on branch
`amp-sumi/tierA-alphaxiv-gate`, stacked on PR #29 head `453baf6` (which stacks
on draft PR #28). Main at the time of the run: `8f96c4b` (PR #27 merge).

## 1. Verification suites

`verify_all.py --check` is a real check only on this branch. On main it exits
0 on a corrupted `results/certificates.json` and silently rewrites the file
back to the computed values (reproduced 23 Nov 2026: slope `9.9999` rewritten
to `2.0186`, exit 0). That is the fault PR #28 fixes. On this branch the same
probe exits 1 with `CHECK FAILED: stored certificates.json differs from the
fresh computation`, and the corrupted file is left untouched. The gate therefore
stacks on #29 and does not re-do the fix.

| Command | Exit | Result |
|---|---|---|
| `python3 -I -B verify_all.py --check` | 0 | CHECK OK (byte-identical), `certificates.json` canonical `040a757f5b4a01e735d1c4a55bca639e79bf8c64ef92588ce290d931f614320a` |
| `python3 -I -B formal/verify_exact_rational_proofs.py` | 0 | pass |
| `python3 -I -B wave3_empirical_audit.py --check` | 0 | CHECK OK, canonical `75f6df7c…b93` |
| `python3 -I -B wave4_unified_field_solver.py --check` | 0 | CHECK OK, canonical `1a7f2ff0…452d` |
| `python3 -I -B wave5_unified_forces_stochastic_qm.py --check` | 0 | CHECK OK, canonical `5abd85ab…b76` |
| `python3 -I -B wave6_convergence_unification.py --check` | 0 | CHECK OK, canonical `49996c54…bae3bf` |
| `python3 -I -B wave7_group_cluster_threshold_audit.py --check` | 0 | CHECK OK, canonical `4db35ebc…08a9` |
| `python3 -B wave9_scale_convergence_audit.py --check` | 0 | CHECK OK, canonical `d9d19847…33a55` |
| `python3 -B wave10_covariant_jeans_unification.py --check` | 0 | CHECK OK, canonical `7dd4b401…3d4` |
| `python3 -I -B wave11_machian_pairing_unification.py --check` | 0 | CHECK OK, canonical `4786fa98…4692b` |
| `python3 -I -B wave12_cosmic_dawn_quasar_collapse.py --check` | 0 | CHECK OK, canonical `40a770d7…4c9` |
| `python3 -B -m unittest test_wave11_12_corrections` | 0 | 7 tests OK |
| `python3 -B -m unittest test_check_modes` | 0 | 6 tests OK |
| `python3 -B -m unittest test_verifier_assert_fix` | 0 | 10 tests OK |
| `sha256sum -c SHA256SUMS` | 0 | 42/42 OK (after regenerating this PR's entries) |
| `cd monographs && sha256sum -c SHA256SUMS` | 0 | 15/15 OK |

`results/certificates.json` is byte-identical before and after the run
(canonical `040a757f…`, same as on main). No certificate content changed in
this PR; the file is re-verified, not updated. `git status` after the full
run shows only the files this PR intends to change.

### Invocation note (recorded, not worked around)

`python3 -I -B` fails for anything with a local import, because isolated mode
drops the working directory from `sys.path`:

- `python3 -I -B -m unittest test_wave11_12_corrections.py` exits 1 with
  `ModuleNotFoundError: No module named 'test_wave11_12_corrections'` (the
  same command without `-I` passes 7/7, with or without the `.py` suffix).
- `python3 -I -B wave9_*.py --check` and `wave10_*.py --check` exit 1 with
  `ModuleNotFoundError: No module named 'wave7_group_cluster_threshold_audit'`
  (both import wave 7). Without `-I` both pass, CHECK OK.

The table above uses the invocation that actually runs each check. Nothing
numerical failed; the two `-I` failures are import-path artifacts.

## 2. PDF QA — the 4 monographs in `monographs/`

| File | Pages | Size | Text |
|---|---|---|---|
| `unified_forces_and_stochastic_quantum_monograph.pdf` | 6 | 486,684 B | 2,865 words |
| `unified_quantum_condensate_gravity_monograph.pdf` | 8 | 549,090 B | 4,306 words |
| `wave6_convergence_and_methods_monograph.pdf` | 5 | 388,170 B | 2,392 words |
| `wave7_group_cluster_roton_threshold_audit.pdf` | 5 | 316,755 B | 2,313 words |

All four: pdfTeX 1.40.29, unencrypted, letter except wave 7 (A4), created
12 Nov 2026. First and last pages rendered via `pdftoppm` for each file
(non-empty output, page 1 of the condensate monograph visually inspected:
clean typeset text, no corruption). `pdftotext` extraction succeeds for all
four. Searched extracted text for `TODO|FIXME|TBD|XXX|DRAFT|PLACEHOLDER`,
private paths (`/home/`, `/Users/`, `C:\`, `/tmp/`), and credentials
(`api_key`, `password`, `secret`, `token`, private-key headers, `ghp_`,
`github_pat`): no hits in any monograph.

## 3. Audit and reconciliation

- **Attribution.** No contradiction, but it was unstated. The generator
  scripts (`verify_all.py`, `wave11_*`, `wave12_*`) are attributed in their
  headers to Gemini via orda-aska. `WAVE11_12_CORRECTIONS.md` was prepared by
  gpt-forge using GPT-6.1 Sol. The three attributions cover different
  artifacts. This PR records that in the corrections note itself.
- **"Independent implementation review is pending" is stale.** The review
  landed 12 November 2026 (`research/wave11-12-review-20261112/REVIEW.md`,
  reviewed commit `e5d7ee8`): gpt-forge using gpt-6-astra, independent of the
  GPT-6.1 Sol implementation author, disposition no blocking scientific or
  implementation issue. The corrections note now says so.
- **arXiv 2610.09987v2.** Confirmed live on arXiv 23 Nov 2026: "Is MOND an
  effect of cosmic frame-dragging à la Mach?", author Manuel Urueña Palomo,
  submitted 7 Oct 2026, v2 25 Oct 2026. The `CLAIMS.md`, `CHANGELOG.md`,
  `WAVE11_12_CORRECTIONS.md` and `wave11_*` attribution to Urueña Palomo is
  correct; the earlier "Braun" attribution is gone from the docs. One
  residual fixed here: `index.html` cited `arXiv:2610.09987` without the
  version; it now reads `arXiv:2610.09987v2`.
- **451.536 Myr.** The correction is reflected where the growth clock is
  stated: `WAVE11_12_CORRECTIONS.md` (451.536 Myr = pure H, 396.223 Myr =
  primordial H/He, at fixed Schwarzschild efficiency `1 - sqrt(8/9)`),
  `CLAIMS.md` C-31 (451.54 / 396.22 Myr, rounded), `RESEARCH_NOTEBOOK_AND_REASONING.md`,
  and `results/wave12_cosmic_dawn_quasar_certificates.json` (451.536, pure-H
  field). The independent review recomputed both clocks and agrees.
  It is **not** in the monograph texts, because no monograph covers wave 12:
  the four monographs are waves 1–7 only (no `wave 11`, `wave 12`, `machian`,
  `cosmic dawn`, `quasar`, `J1602` or growth-clock text in any `.tex`). No
  monograph number was wrong; there is no wave-12 section to correct. Adding
  one would be new content, not QA, and is out of scope for this gate.
- **REVIEW.md's nine inherited manifest mismatches are closed.** The review
  (12 Nov) listed nine files whose `SHA256SUMS` entries mismatched. PR #27
  regenerated the manifest; the root manifest passes 42/42 on this branch
  (41 on this branch before this PR's entries; 39 on main) and the monograph manifest 15/15.

## 4. Scope

This gate covers verification, PDF QA, and the doc reconciliations above. It
does not upload anything to alphaXiv and does not mint a Zenodo DOI; those
are separate steps once this PR and its bases (#28, #29) merge. The four
monographs are publishable as waves 1–7 records as they stand; wave 11/12
has no monograph.
