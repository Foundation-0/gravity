# Checksum snapshot provenance

Source commit: `364fa3e9f740f42acaa1991428ce043f547e10dd`. Manifest last changed at `f8030d6`.

This snapshot records file bytes only. It does not establish proof compilation, generator agreement, or physical validity. No scientific values or source files are changed.

## Certificate metadata repair

The Wave 4 JSON used `sha_26_canonical` instead of the expected `sha256_canonical` key. Regeneration changes only that key. Its value, `1a7f2ff0182b66d1a081e59e750b493afa6beaab0d976c5af2c6c72652d4452d`, and every scientific field remain unchanged. The existing generator now passes `--check`. The previous outer file hash was `824d1a5d68f16a2383d6afd3397776d3f3ae99361595379eb827fa71d69321ea`.

## Inherited fingerprint mismatches

| File | Previous SHA-256 | Source-commit SHA-256 | Last file commit |
| --- | --- | --- | --- |
| `lakefile.toml` | `0ef38cabbe87049f2f99abc3fe0c45578d2c72ec7fd417dc562e50a2dbf133d9` | `31431d19675149705eb32b27f85c600ed6df022d5eac661fb55fe0488f55bfaa` | `3f7a5b1 Wave 12: register Wave12QuasarCollapse target in lakefile.toml` |
| `verify_all.py` | `1e907f6af0b1dcc633feec478aebd4997e52f048f6d3ba99974f6c03a707dac1` | `49bd79489023aed0f6d1b325734012a6b6e0bf4b0b20755e83f20e7fd332583c` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `wave5_unified_forces_stochastic_qm.py` | `290a9bbb1ddd8140e7e27c25a46ebf30012cf1c4c796e0d354f95a0a9f0ca327` | `effc8ef25d4489d9cf2d6ea0c0af78d7707fb2c246038f191c8cda22e2a8762d` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `formal/verify_exact_rational_proofs.py` | `606431af2e1366cff43a658c65080f146789fe6e7159f317648cc621f7a8cb28` | `d0acfe8ea3ab801f5538999979c3e4f69545b1734b02a998451d4263f69b3ce6` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `formal/GravityClaims.lean` | `db6e4a202d357b5bd175b20b971b3a79e3b34a573382e2f0e5ed4341d0507562` | `c2e635f3af901aef8b51b529f46d2c16742c06c597a543e8cf518f4eb636f70e` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `formal/Wave5StochasticForces.lean` | `a097c2ea83cf1ad0788d8969427737c6e5b1d2250d6c1f3f529178e39903eeda` | `8702c37822bcc1178d5d5cade50d59929f8550a61a45cb38ebcc3c5e1d48b9f9` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `formal/Wave6Convergence.lean` | `fd52c8d997ccf9873cfd020f19f62b27dbfbdecda0234075ddd571193e0a9385` | `4474b263b026d97089dcd8cc154b4ec5964212554901e66a63b16f88094a106d` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `formal/Wave7ThresholdAudit.lean` | `41cd166341b517f3ab316ad5987cd9c74e5a2d443d763d948cde869d285a0672` | `f8b168944f4364fe6eb2b1af64695b224e5dd8f5ba8f086168b08fcc2bce3fd6` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `results/wave4_unified_certificates.json` | `7bb2326b36aab2c09c542a112317e4afccd0ffee2f74cdd6a8cc2a65b230255e` | `824d1a5d68f16a2383d6afd3397776d3f3ae99361595379eb827fa71d69321ea` | `7f388db Add Wave-10 assumptions, M-08 cross-epoch method, and certificate checksum` |
| `README.md` | `5e882f682fd25e980a7f933668fd177b8136208185095b747dc327bc1806f078` | `b72f86c977c4b2052d70f4a82b4980db947f6c573e7bfae7e288d561c38b91ae` | `70a1204 Wave 12: index Wave 12 solver, Lean target & C-31..C-33 in README.md` |
| `CLAIMS.md` | `c459b23829444a125fd0b682ab01dc34441088566292b9dad13566ee3b29b6df` | `223059cc0b79fbc1dfe4c2ab801c2610ee898316e66409084f059a9b1aac1a23` | `364fa3e Wave 12: add audited claims C-31..C-33 to CLAIMS.md` |
| `RESEARCH_NOTEBOOK_AND_REASONING.md` | `3c4427c87d5c53ac62bbb1a8b41836b6a567485f1716d5c29329d6809f24e45e` | `407c4cfbda5ac32e35dfc234530436b15fb963e28971f82888377c0a268751f4` | `c5809bc Add Wave 11 hypotheseWave 11: document Machian inertia, DESI turnaround & CPT pair reasoning in notebooks on inertia and dark matter` |

Nine of these mismatches also exist on the Wave 11/12 audit branch at `e5d7ee813e33de03c91857e48a2d55a0caf55506`. That branch has refreshed README, CLAIMS, and the reasoning notebook.

The eight entries last changed at `7f388db` already disagree with the later `f8030d6` manifest. The other four entries changed after that manifest. This history establishes stale or incorrect file fingerprints. It does not establish the scientific correctness of the file contents.

## Coverage and checks

The existing 30 manifest entries are retained. Six tracked files are added: the Wave 11 and Wave 12 generator scripts, their JSON certificates, and their Lean libraries. `SHA256SUMS` and this provenance note are excluded to avoid self-referential hashes.

Existing generator `--check` runs pass for Waves 3, 4, 5, 6, 7, 9, 10, 11, and 12. `verify_all.py --check` and `formal/verify_exact_rational_proofs.py --check` also pass and regenerate byte-identical certificate files.

The full Lean build on the source commit fails. The separate corrections in PRs 10 and 14 are required for a successful full build. Adding Lean files to this byte inventory does not establish that they compile.

Manifest values describe this branch snapshot. Recompute hashes for files subsequently changed by PRs 10, 12, 13, or 14. These independent changes have not been composed on main.

Recompute the listed bytes with `shasum -a 256 -c SHA256SUMS`. A successful result means only that the listed bytes match this snapshot.
