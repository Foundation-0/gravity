# Expedition Probes: AeST Helmholtz Schur-Complement Closure, Outside-Anchor Latch Audit & Zero-Float Inertia Box Certifier

Self-contained verification and research package for **`Foundation-0/gravity`**, independently audited under strict adversarial verification (`AUDIT-011R` **`VERIFIED` `N2`**, `AUDIT-012` **`VERIFIED` `N1`**, `AUDIT-013R` **`VERIFIED` `N1`**). All scripts are `-O`-safe (zero bare `assert`s), deterministic, LF-clean, and leave all existing repository files untouched.

## Contents

| File | Scope & Audit Status | Dependencies |
|---|---|---|
| `probe1_aest_helmholtz_closure.py` / `probe1_aest_results.json` | **`AUDIT-011R` (`VERIFIED`, `N2`)**: Exact non-local Helmholtz pressure closure for `research/aest-response-gate-20261112/slow-mode`, exact Hamiltonian Schur-Complement Theorem ($\min_{(\chi,p)} H_2 = \frac{1}{2}S_P P^2 \equiv -(G_{AA}/\widetilde{G})D^2/(2k^2)$), $\lambda_s=0$ zero-sound-speed Yukawa cutoff, $2\times 2$ baryon–AeST growth matrix, and recursive Chebyshev Fenichel lifts $H_0..H_3$ passing the 1% benchmark (`0.55%` at $H_0$, `0.000083%` at $H_3$ vs `24.6%–185%` local closures). | Python 3 + `numpy`, `scipy`, `sympy` |
| `probe2_latch_outside_anchors_and_chirp.py` / `probe2_latch_chirp_results.json` | **`AUDIT-012` (`VERIFIED`, `N1`)**: Sample-disjoint outside-anchor Leave-One-Catalog-Out + 5,000-trial permuted-null audit of Wave 7/9/10 (`~185 km/s` threshold collapses to `73.9 km/s` when holding out only the 6 galaxy anchors; SPARC `d_s=0.94` fails on disjoint KiDS-1000 1 Mpc `chi2=75.51` vs `31.53` for `d_s=1.00`), plus repaired scale-invariant derivative-free Box–Cox blind GW chirp estimator (`0` FPs across glitch/red-noise/parabolic/IAAFT). | Python 3 + `numpy`, `scipy` (reads repo's own `wave3`/`wave7` modules automatically) |
| `probe3_nonaffine_inertia_box_certifier.py` / `probe3_inertia_boxes_results.json` | **`AUDIT-013R` (`VERIFIED`, `N1`)**: 100% pure-stdlib zero-float exact-rational (`fractions.Fraction` + `math.isqrt`) Bunch–Kaufman non-affine Sylvester inertia box certifier across real piecewise `fibral-rigidity#5` (isolating $L_1+L_2=2$), 4 AeST Minkowski boxes (UV `[3,0,0]`, IR `[2,0,1]`, crossing, and $\lambda_s=0$ Yukawa boundary `[2,0,1]` in `907` boxes), and `Foundation-0/point-charges` $C_3/C_4$ 3D electrostatic Morse-index boxes (`m2 - m1 = n - 1`). | Pure Python 3 stdlib (zero external packages, zero floats) |
| `GRAVITY_EXPEDITION_REPORT.md` | Full technical derivations, benchmark tables, canonical SHA-256 digests, and falsification criteria. | — |
| `data/point-charges/{n3-triangle,n4-triangle-plus-centre}.json` | Read-only equilibrium enclosure certificates copied verbatim from [`Foundation-0/point-charges`](https://github.com/Foundation-0/point-charges) (Apache-2.0 / CC-BY-4.0) so `probe3` runs standalone; override via `POINT_CHARGES_DIR`. | — |

## Reproduction

From the repository root:

```sh
# Probe 1 (AeST Helmholtz closure + Hamiltonian Schur-Complement Theorem + 1% slow-mode gate)
python3 -I -O -B -W error studies/expedition-aest-helmholtz-probes/probe1_aest_helmholtz_closure.py

# Probe 2 (Gravity Latch LOCO outside anchors + SPARC->KiDS + Box-Cox blind chirp)
python3 -I -O -B -W error studies/expedition-aest-helmholtz-probes/probe2_latch_outside_anchors_and_chirp.py

# Probe 3 (Pure Python 3 stdlib — zero floats, zero NumPy/SciPy!)
python3 -I -O -B -W error studies/expedition-aest-helmholtz-probes/probe3_nonaffine_inertia_box_certifier.py
```

## Canonical SHA-256 Digests (`sha256_canonical`)

- `probe1_aest_results.json`: `bcde49380e1bc5ce8c2e23cc08257c022ed87658dd53265ecc9f1d7825934ff5`
- `probe2_latch_chirp_results.json`: `ed74a3a43d5af5a37856cbfde53dbb569690711a81cd3cf9ebbf05f8edc3e858`
- `probe3_inertia_boxes_results.json`: `6d46734781a86a84ba86f980b5b31579a3da5111eaa21330d1cb1735d8a63efb`
