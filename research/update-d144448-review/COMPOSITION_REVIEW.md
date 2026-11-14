# Review of the reconciled documentation

No blocking scientific or provenance issue was found in the five-file documentation change. It resolves or removes the nine repeated claims identified in [REVIEW.md](REVIEW.md). No new physical test or parameter search is justified by the four upstream commits.

This review covers the staged composition of main `d1444481cdefc59a275ede2fef740ea2cf48eeec` with correction head `03f96e977c1852930c85d7568aff087e093e4d50`. It was checked before commit on 12 November 2026. The exact bytes are recorded in [composition-evidence.json](composition-evidence.json). Later publication can add this review without changing the reviewed files.

The author retained the corrected numerical implementation. The new notebook and methods now describe conditional growth and radial clocks. They distinguish total halo mass from a seed, an assigned trapping fraction from capture, and isolated Peters clocks from a hardening history or gravitational-wave population prediction.

M-09 and the standalone changelog both restrict positive dust density to selected supercritical polynomial states. They preserve current-conservation and stability limits. No production mechanism, symmetry-protected remnant or relic abundance is established. The corrected source attribution and conditional CPL interpretation are retained.

| Finding in the upstream delta | Resolution in the composition |
|---|---|
| D01: author attribution and induction | Urueña Palomo is identified. The partition remains illustrative. |
| D02: future expansion and constraint | Density closure is stated. Future continuation and origin limits remain explicit. |
| D03: polynomial states | Positivity has a branch condition. Production, full mixing stability and portal rates remain unresolved. |
| D04: growth wall | Opacity and fixed Schwarzschild counterexamples are stated. The unequal-convention seed comparison is removed. |
| D05: clustering likelihood | The notebook says extrapolated clustering and Gaussian tails supply no comparative cosmological likelihood. |
| D06: seed and capture | The total halo scale and prescribed trapping fraction are distinguished from formation dynamics. |
| D07: infall and friction | The force-integrated numbers and individual force cases replace the shortcut. Missing dynamics are stated. |
| D08: slim-disk retention | The stated inflow subtracts radiated energy. Corrected clocks are 273.78 and 161.23 Myr. |
| D09: projection and hardening | Both are conditional benchmarks. No merger path or background is predicted. |

Independent byte checks found the five staged files identical to the files on disk and the author's final hash packet. All 31 tracked Python, Lean and results-certificate files are unchanged from the prior correction head. The ten protected source, certificate, test, note and frozen-review files are also unchanged.

The four changed documents covered by the manifest match their entries. The Wave 11 and Wave 12 canonical certificate hashes were recomputed independently and agree with the methods table. The wrapper now directs replay of the earlier frozen review to its original source revision.

Eight inherited manifest mismatches remain. Their file bytes and expected hashes are unchanged from the prior correction head. This review does not certify the full manifest, rerun the earlier seven numerical controls or claim a new Lean build. The exact mismatch list is in the evidence file.

The physics0 cross-repository addendum also passes a scientific scope check at its recorded hash. It distinguishes the corrected method from main, preserves the clustering caveat and concludes that these commits add no new test inputs. Its operational assertions about the separate checksum and Lean repair PRs rely on their respective reviewers' evidence.

| Reviewed file | SHA-256 |
|---|---|
| `CHANGELOG.md` | `30661fc8aca473bc136f2c251509868d16c973c8ea572f3d574ebd31bd1d88a6` |
| `METHODS_AND_PLAYBOOK.md` | `ecdb12077d8ddfb1b8a787064f07e5028adcd308c6a11274600e596f8e4a6bd7` |
| `RESEARCH_NOTEBOOK_AND_REASONING.md` | `3e512058fd3107ccd904bb8bfa58ea0c2e168fd053b0c05b0b891030d10e701f` |
| `SHA256SUMS` | `8559c0e2ff5f74693d4ea00cd4dabce7ce09bf08648d450c5d9e42d87f2083a4` |
| `research/wave11-12-review-20261112/README.md` | `df1bb88416f672c6b9a97ab75d5d7056b823bf8bda261888d076d98737db00e4` |
