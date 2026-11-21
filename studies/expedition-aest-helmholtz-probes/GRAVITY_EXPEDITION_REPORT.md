# Gravity & Physics Frontier Expedition Report

**Owner:** `gravity-probe`  
**Study Directory:** `studies/expedition-aest-helmholtz-probes/`  
**Cloned Physics Repos (read-only, verified clean):** `Foundation-0/{gravity,physics0,cosmic-denoising,relative-equilibria,certified-orbits,point-charges}`

---

## 1. Live Baseline Established

1. **`Foundation-0/gravity` (`8f96c4b`, `main`):**
   - `sha256sum -c SHA256SUMS`: **100% OK** across all manifest files.
   - All 10 root verification scripts (`verify_all.py`, `wave3`–`wave7`, `wave9`–`wave12`) passed `--check` byte-identically, plus `test_wave11_12_corrections.py` (`7/7 OK`).
   - Independently replayed `research/aest-response-gate-20261112/response.py` into `baseline_aest_response.json` (`15` FLRW preparations, max constraint residual `5.20e-12`, max 5-field vs 4-state discrepancy `5.48e-11`, all checks passed).
   - Audited open issues (`#1`–`#7`, `#20`) and open PRs (`#28` symbiosis 763-galaxy review & check-mode fix, `#29` `-O`-safe verifier assertions).
2. **Sibling Physics Repos Cloned & Indexed:**
   - `point-charges`: certified exact equilibrium counts for $C_3$ (4), $C_4$ (9), $C_5$ (24), $C_6$ (29), $C_7$ (44); used $C_3$ and $C_4$ JSON certificates directly in Probe 3.
   - `relative-equilibria`, `certified-orbits`, `physics0`, `cosmic-denoising`: inventoried open computer-assisted proof frontiers ($n=8$ equal-mass central configurations, $5$–$7$ vortices, Li–Liao periodic 3-body orbits).
3. **Cross-Repo Read-Only Reference:**
   - `Foundation-0/fractals/witness-map/{model.js,table.mjs}` calibrated directly in Probe 4 and reconciled quantitatively with `Foundation-0/gravity` `C-03`.

---

## 2. Probe 1 — Exact AeST Helmholtz-Screened Slow-Manifold Closure, Hamiltonian Schur-Complement Theorem & 2×2 Baryon–AeST Growth Law

- **Status:** **`VERIFIED` (`AUDIT-011`, confirmed `N2` major physics milestone)**; post-audit addition (#48 exact Hamiltonian Schur-Complement Theorem & $\lambda_s = 0$ exact minors) integrated and re-verified cleanly under `-O -B -W error`.
- **Script:** `studies/expedition-aest-helmholtz-probes/probe1_aest_helmholtz_closure.py`
- **Artifact:** `studies/expedition-aest-helmholtz-probes/probe1_aest_results.json`
- **Canonical Payload SHA-256 (`sha256_canonical`):** `bcde49380e1bc5ce8c2e23cc08257c022ed87658dd53265ecc9f1d7825934ff5` *(pre-addition `AUDIT-011` hash: `fa4d3a1beba8eb4f6efd7ee45420ddfedb6c2ff9a259431309e00f2221a09dcc`; on-disk file SHA-256: `5992f3d293842d173edb718c2b4f724771fb0e6920f19b99032e280f12587dec`)*
- **Repro (`-O -B -W error`, zero bare `assert`s):**
  ```sh
  python3 -I -O -B -W error \
    studies/expedition-aest-helmholtz-probes/probe1_aest_helmholtz_closure.py
  ```

### 2.1 New Exact Theorems Proved Symbolically (SymPy) & Verified Numerically / Over $\mathbb{Q}$

Starting from the exact constrained linear AeST quadratic ADM action (`research/aest-response-gate-20261112/derivation.md`) with $\mathcal{F}(\mathcal{Y},\mathcal{Q}) = (2-K_B)\lambda_s \mathcal{Y} - \mathcal{K}(\mathcal{Q})$ for arbitrary $(K_B, \lambda_s, \mathcal{K}'')$ ($0 < K_B < 2$, $\mathcal{K}'' > 0$):

1. **Non-Local Helmholtz Pressure Closure (Resolves `aest-response-gate/slow-mode`):**
   Eliminating the fast scalar-vector pair $(\chi, Z)$ on the slow manifold in the cold subhorizon regime ($H \ll k/a$, $K'/Q \to 0$) yields neither zero pressure ($\delta P = 0$) nor local adiabatic pressure ($\delta P = c_a^2 \delta\rho$), but the **exact non-local Helmholtz screening operator**:
   $$\left(M_{\mathrm{scr}}^2 - \frac{\nabla^2}{a^2}\right)\delta P = c_a^2 M_{\mathrm{scr}}^2\,\delta\rho, \qquad M_{\mathrm{scr}}^2 \equiv \frac{\mathcal{K}'' Q^2 (1 + \lambda_s)}{2 + K_B \lambda_s}.$$
2. **Exact Scale-Dependent AeST Self-Gravity, Pole-Zero Identity & Hamiltonian Schur-Complement Theorem (#48):**
   Substituting this screened pressure into the Euler equation yields $\ddot\delta_A + 2H\dot\delta_A = \frac{1}{2} G_{AA}(k/a) R_A \delta_A$ with:
   $$\frac{G_{AA}(k/a)}{\widetilde G} = \frac{\mathcal{K}'' Q^2 (1+\lambda_s) - (2-K_B)\lambda_s (k/a)^2}{\mathcal{K}'' Q^2 (1+\lambda_s) + (2+K_B\lambda_s)(k/a)^2}.$$
   - **IR limit ($H \ll k/a \ll Q_0$):** $G_{AA} \to +\widetilde G$ ($\Lambda$CDM clustering).
   - **UV limit ($k/a \gg Q_0$):** $G_{AA} \to -\frac{(2-K_B)\lambda_s}{2+K_B\lambda_s}\,\widetilde G$ (strictly **self-repulsive** whenever $\lambda_s > 0$, even as $c_a^2 \to 0$).
   - **Exact Hamiltonian Schur-Complement Theorem:** Eliminating the fast canonical pair $(\chi, p)$ from the Minkowski AeST quadratic Hamiltonian $H_2(\chi, p, P)$ ($P = -2D$) gives the exact Schur complement $S_P = M_{PP} - M_{Pf}M_{ff}^{-1}M_{fP} = \Delta_3 / \Delta_2$ with **zero symbolic residual**:
     $$\min_{(\chi,p)} H_2(\chi, p, P) = \frac{1}{2} S_P P^2 \equiv -\left(\frac{G_{AA}(k)}{\widetilde G}\right)\frac{P^2}{8k^2} = -\left(\frac{G_{AA}(k)}{\widetilde G}\right)\frac{D^2}{2k^2}.$$
     This explains *why* $r_{\mathrm{zero}}/\mu^2 \equiv 1$: Skordis–Zlosnik's Minkowski UV stability ($\Delta_3 > 0$, inertia `[3,0,0]` for $k > \mu$) IS mathematically identical to positive gravitational self-energy $\iff$ self-repulsive anti-gravity ($G_{AA} < 0$), while the IR `[2,0,1]` inertia ($k < \mu$) IS negative gravitational binding energy ($G_{AA} > 0$). Certified over $\mathbb{Q}$ at $K_B = \lambda_s = 1, \mathcal{K}'' = 4, Q = 1$: $r=9 \implies [3,0,0], G_{AA}=-1/35$; $r=8 \implies [2,1,0], G_{AA}=0$; $r=7 \implies [2,0,1], G_{AA}=+1/29$.
   - **$\lambda_s = 0$ Cosmological Yukawa Cutoff:** At $\lambda_s = 0$, $\mu^2 \to +\infty$, $G_{AA}(k/a)/\widetilde G = \frac{M_0^2}{M_0^2 + (k/a)^2}$ ($M_0^2 = \mathcal{K}'' Q^2 / 2$), and $S_P = -\frac{\mathcal{K}''}{4r(\mathcal{K}'' + 2r)} < 0$ strictly for all finite $r > 0$ — giving a **zero-sound-speed spatial Yukawa cutoff** with uniform inertia `[2,0,1]` (evading Wave-10's local barotropic sound-speed no-go `C-25`).
3. **Exact Static–Dynamical Baryon Duality & Coupled $2\times 2$ Growth Matrix:**
   Adding minimally coupled baryons leaves the fast $(\chi, Z)$ equations identically independent of $D_b$ (`diff == 0`), yielding $\mathbf{G}_{\mathrm{eff}}(k/a) = \begin{pmatrix} 1 & 1 \\ 1 & G_{AA}(k/a) \end{pmatrix}$. Static equilibrium of AeST dust ($D_{A,\mathrm{eq}} = -D_b / G_{AA}$) reproduces the exact static baryonic Poisson propagator $\Phi_{\mathrm{static}}/\Phi_{\mathrm{Newton}} \equiv 1 - 1/G_{AA}(k/a)$ with zero symbolic residual. Dynamically, for Planck $f_b = 0.1565$ and $k/a > \mu$, $\det \mathbf{M}_2 = f_b(1-f_b)(G_{AA}-1) < 0$ guarantees a **baryon-driven growing mode** with suppressed exponent $p_+ \in (0.45, 0.61)$ and dark-to-baryon segregation $\delta_A/\delta_b < 1$, verified to `0.003%–0.23%` against full 6-state relativistic action ODEs across $\lambda_s \in \{1, 0, -0.5\}$ and $k/Q_0 \in \{0.5, 2\sqrt{2}, 10, 50\}$.

### 2.2 Benchmark Results on `aest-response-gate-20261112/slow-mode/` (1% Pass Gate) & Quantitative Closure Defect (`SEAM-02` / `T5` / `S1:F[451]`)

Using smooth Chebyshev recursive Fenichel maps $H_0 \to H_1 \to H_2 \to H_3$ solving the invariance commutation defect $\mathcal{R}[H] := C + FH - \dot H - H(A + BH) = 0$ (zero fitted parameters):

| $k/Q_0$ | Zero-Pressure err (defect) | Adiabatic err | Our $H_0$ vs `probe.py` frozen IC | Our $H_3$ vs invariant IC (defect) |
|---:|---:|---:|---:|---:|
| 6 | 24.603% (`6.48e-1`) | 117.584% | **0.5479%** (PASS) | **0.001263%** (`1.23e-4`) |
| 9 | 26.193% (`5.18e-1`) | 151.239% | **0.5715%** (PASS) | **0.000610%** (`3.19e-5`) |
| 12 | 26.806% (`4.83e-1`) | 166.308% | **0.5805%** (PASS) | **0.000351%** (`1.45e-5`) |
| 18 | 27.263% (`4.63e-1`) | 179.572% | **0.5869%** (PASS) | **0.000154%** (`5.71e-6`) |
| 24 | 27.427% (`4.57e-1`) | 185.409% | **0.5891%** (PASS) | **0.000083%** (`3.12e-6`) |

- **Anti-shadow controls passed:** Random $GL(2)\times GL(2)$ basis invariance max diff `< 1e-11`; Chebyshev deg 24 vs 36 refinement diff `< 1e-8`; flipped-$H$ negative control error `> 100%`; wrong-sign Helmholtz ($M_{\mathrm{scr}}^2 \to -M_{\mathrm{scr}}^2$) error `> 25%`; deliberate fast-mode leakage $\eta_Z \in \{0, 0.01, 0.1, 1\}$ scales trajectory error linearly while leaving $\mathcal{R}[H_3]$ unchanged.
- **Falsification criterion:** Any symbolic residual $\ne 0$ (including `hamiltonian_schur_energy_residual` and `hamiltonian_schur_hessian_residual`); any $k/Q_0 \in \{6,9,12,18,24\}$ failing the 1% gate under $H_0$–$H_3$; any $GL(2)\times GL(2)$ transform changing observables $> 10^{-10}$; or any 6-state baryon+AeST trajectory disagreeing with the $2\times 2$ $\mathbf{G}_{\mathrm{eff}}(k/a)$ law by $> 0.3\%$ at $q_i = 10^{-4}$.

---

## 3. Probe 2 — Physics Latch + Truly Disjoint Outside Anchors (`SEAM-03` / `T4`) & Repaired Prior-Free GW Chirp Invariant (`ep-03`)

- **Status:** **`VERIFIED` (`AUDIT-012`, `N1`)**; minor unused-typing import (`Tuple`) patched cleanly with identical canonical hash.
- **Script:** `studies/expedition-aest-helmholtz-probes/probe2_latch_outside_anchors_and_chirp.py`
- **Artifact:** `studies/expedition-aest-helmholtz-probes/probe2_latch_chirp_results.json`
- **Canonical Payload SHA-256 (`sha256_canonical`):** `ed74a3a43d5af5a37856cbfde53dbb569690711a81cd3cf9ebbf05f8edc3e858` *(on-disk file SHA-256: `e6a6beb69a1800d88fd3fe274c3f5ca101865418ad24052866eae59f25ecff12`)*
- **Repro (`-O -B -W error`, zero bare `assert`s):**
  ```sh
  python3 -I -O -B -W error \
    studies/expedition-aest-helmholtz-probes/probe2_latch_outside_anchors_and_chirp.py
  ```

### 3.1 Part A — Real-Data Gravity Latch & 5,000-Trial Permuted-Null Audit (126 Systems + SPARC→KiDS)
1. **The `~185 km/s` threshold in Wave 7/9/10 is an anchor-driven Latch artifact:**
   - Exact inside-span probe has $\sin^2(w, \operatorname{Col}(\Phi)) < 10^{-14}$; the sharp-vs-smooth kink has $\sin^2 = 0.489$.
   - **Leave-One-Catalog-Out (truly sample-disjoint outside anchors):** Removing ONLY the 6 galaxy anchors (`SPARC_HSB` + `KiDS_WL`) and training on the 120 groups & clusters collapses the fitted threshold from `~190 km/s` to **`73.9 km/s`** (Hill) and **`131.0 km/s`** (Jeans 2p) — and even lower (**`60.15 km/s`**) under native Wave-10 ODR in `@verifier`'s independent check (`AUDIT-012`) — exploding holdout $\chi^2$ on the 6 galaxies to `130.24` (Hill) / `444.16` (Jeans 2p) vs `0.34` (MOND).
   - Conversely, on held-out `Kettula2015_WL` ($n=28$) and `Milgrom2019_opt` ($n=56$), a smooth threshold-free 3-parameter sigmoid (`127.28`, `61.01`) **beats** the sharp `185 km/s` Hill threshold (`129.25`, `62.71`), while `T4` 5,000-trial global permutation finds highly significant systematic cross-catalog offsets (**$p = 0.0002$**).
2. **SPARC 14-bin RAR $\to$ Disjoint KiDS-1000 1 Mpc WL Outside Anchor (`C-08`):**
   - Free-`d_s` SPARC fit prefers `d_s = 0.94, a0 = 1.25e-10` in-sample (`chi2 = 25.91` vs `30.49` for `d_s = 1.00`), yet **fails** on the truly disjoint KiDS-1000 1 Mpc anchor (`chi2 = 75.51` vs `31.53` for exact `d_s = 1.00`, $\Delta\chi^2 = -44.0$).

### 3.2 Part B — Repaired Scale-Invariant Box–Cox Integral Blind Chirp Estimator (`ep-03`)
Repairs all 3 bugs in Session 1 `pair_20_block_00.py` (bounds-safe lag slicing, median one-sided Welch PSD whitening, and removal of hardcoded `[30, 350]` Hz band and `-11/3` exponent) via the derivative-free Box–Cox integral null-equivalence $\hat\alpha = \arg\min_\alpha (1 - R^2(t, u_\alpha(f(t))))$:
- Newtonian inspiral $1\times$ ($\alpha_{\mathrm{true}} = 3.6667$): `corr = -0.980, lag = +28, alpha_hat = 3.62, nonlin = 2.47e-4` (**detected**).
- Newtonian inspiral $2.5\times$ (frequency-rescaled outside `[30, 350]` Hz): `corr = -0.990, lag = +28, alpha_hat = 3.68, nonlin = 3.19e-5` (**detected, scale-invariant**; verified by `@verifier` across `0.7x..3.0x`).
- Linear chirp ($\alpha = 0.0$): `alpha_hat = -0.01, nonlin = 4.98e-5`; Exponential chirp ($\alpha = 1.0$): `alpha_hat = 1.00, nonlin = 1.78e-5`.
- Sine-Gaussian glitch, independent $1/f^2$ colored noise, parabolic FM, and IAAFT phase-randomized surrogate: **100% rejected (`detected = False`)**.
- **Explicit Scope Boundary (`AUDIT-012`):** Designed as an **up-chirp** estimator (`corr_tf >= 0.85`) operating in the high-SNR matched-cross-power regime (verified 5/5 up to `noise <= 0.08`, degrades at `noise >= 0.10`).
- **Falsification criterion:** Any negative control falsely triggering `monotone_chirp_detected=True`; any failure to recover $\alpha$ within `0.25` across frequency rescaling in the high-SNR up-chirp regime; or any non-reproducible permutation $p$-value / LOCO $\chi^2$.

---

## 4. Probe 3 — Pure Zero-Float Exact-Rational Non-Affine Inertia & Morse-Index Box Certifier (`SEAM-04` / `ep-02`)

- **Status:** **`VERIFIED` (`AUDIT-013R`, `exact`, `N1`)** — both `AUDIT-013` defects patched (real piecewise `fibral-rigidity#5` Hessian + strict R3/symmetry guards) + Box D ($\lambda_s = 0$ Yukawa boundary) added and independently verified (`check_011_gravity_reaudit_and_probe4.py`). *(Honest scope note from `AUDIT-013R`: for a black-box callable `M_eval`, a skew-symmetric matrix `[[1, t], [-t, 1]]` over a symmetric box `[-1/2, 1/2]` produces identical off-diagonal intervals `[-1/2, 1/2]`, so interval equality alone certifies symmetry only when the caller supplies a genuine symmetric evaluator or symbolic matrix structure.)*
- **Script:** `studies/expedition-aest-helmholtz-probes/probe3_nonaffine_inertia_box_certifier.py`
- **Artifact:** `studies/expedition-aest-helmholtz-probes/probe3_inertia_boxes_results.json`
- **Canonical Payload SHA-256 (`sha256_canonical`):** `6d46734781a86a84ba86f980b5b31579a3da5111eaa21330d1cb1735d8a63efb` *(on-disk file SHA-256: `9fb40ac639f3c2b080e1a7523fd9461a66f873693942c6a09f9a98cdb7601968`)*
- **Repro (`-I -O -B -W error`, 100% pure Python 3 stdlib — zero NumPy/SciPy/floats, zero bare `assert`s):**
  ```sh
  python3 -I -O -B -W error \
    studies/expedition-aest-helmholtz-probes/probe3_nonaffine_inertia_box_certifier.py
  ```

### Method & Certified Results
Pure `fractions.Fraction` interval arithmetic (`QI`, with integer `math.isqrt` outer square-root brackets and strict R3 guards rejecting `bool`, `float`, `str`, ragged/non-square matrices, AND non-symmetric midpoint/box interval matrices via `_require_symmetric_qi_matrix` — never silently symmetrizing — verified by 9-case `r3_tcb_negative_controls()`), exact Bunch–Kaufman rational congruence $C M(t_c) C^T = \operatorname{diag}(D)$, power-of-2 diagonal balancing, exact Levy–Desplanques / Gershgorin strict diagonal dominance, and BFS box subdivision:
1. **Real Piecewise `aska-physical/fibral-rigidity#5` (`loom#7` `docs/10` §4.2):**
   - Replaces the earlier toy formula with the **exact piecewise equilibrium truss Hessian** (on-line $L_1 + L_2 < 2$, singular line $L_1 + L_2 = 2$ verified `(1,1,0)` at 5 points, off-line $L_1 + L_2 > 2$ evaluated both via exact congruent `[[A,B],[B,C]]` and raw Heron `isqrt` using $y^2 = (L_1+L_2+2)(L_1+L_2-2)(2+L_1-L_2)(2-L_1+L_2)/16$).
   - Replays all 5 exact published rational matrices verbatim (`4` corners `(2,0,0)`, interior `(9/10, 11/10)` singular `(1,1,0)`).
   - Full box `[7/10, 13/10] x [9/10, 15/10]` refuses uniform PD and isolates the singular line $L_1 + L_2 = 2$ (`373` boxes, `133` PD leaves, `54` boundary boxes); on-line sub-box `[7/10, 8/10] x [9/10, 1]` certifies `[2,0,0]` in **`1` box**; off-line sub-box `[11/10, 13/10] x [13/10, 15/10]` certifies `[2,0,0]` in **`3` boxes** (congruent) and **`7` boxes** (raw Heron `isqrt`).
2. **AeST Minkowski Hamiltonian $H_2(K_B, \lambda_s, r)$ (4 Boxes):**
   - Verifies exact unimodular tridiagonal congruence $U M_{\mathrm{AeST}} U^T = \widetilde M$ ($\det U = 1$).
   - **Box A (UV-stable self-repulsive):** `[9/10,11/10]^2 x [16,20]` certified uniformly **`[3,0,0]`** (`871` boxes).
   - **Box B (IR-clustering):** `[9/10,11/10]^2 x [2,4]` certified uniformly **`[2,0,1]`** (`163` boxes).
   - **Box C (Phase-crossing):** `[19/20,21/20]^2 x [3,18]` splits cleanly across $r = \mu^2(K_B, \lambda_s)$ (`71` IR leaves, `212` UV leaves).
   - **Box D ($\lambda_s = 0$ Yukawa boundary, #48):** `[9/10,11/10] x [-1/10,1/10] x [1,4]` certified uniformly **`[2,0,1]`** (`907` boxes, zero degenerate mode, zero floats!).
3. **`Foundation-0/point-charges` $C_3$ & $C_4$ 3D Electrostatic Morse-Index Boxes:**
   - Independently certifies with **ZERO FLOATS** every equilibrium enclosure box of `n3-triangle.json` (`4` zeros: $m_1=1, m_2=3$) and `n4-triangle-plus-centre.json` (`9` zeros: $m_1=3, m_2=6$), confirming exact Morse relations $m_2 - m_1 = n - 1$.
- **Falsification criterion:** Any box certified uniform inertia containing a point with $\det M(t) = 0$ or different Sylvester inertia; any `C @ M @ C^T != diag(D)` residual over $\mathbb{Q}$; any R3 negative control failing to raise `TypeError`/`ValueError`; or any disagreement with published `point-charges` Morse indices / `fibral-rigidity#5` inertias.

---

## 5. Probe 4 — Unified Witness-Map Operator, Tomita–Takesaki Modular Flow & Exact $16\times 16$ Zero-Float Lindblad Zeno Schur-Complement Theorem (`SEAM-09` / Portal 3)

- **Status:** **`VERIFIED` (`AUDIT-018`, `exact` Parts A–B + `anchor` Part C, CONFIRMED `N2` cross-repo milestone)** — independently verified via symbolic SymPy $16\times 16$ GKSL & live `node` execution of `repos/fractals/witness-map/model.js` (`check_011_gravity_reaudit_and_probe4.py`).
- **Script:** `studies/expedition-witness-zeno-schur/probe4_witness_zeno_schur.py`
- **Artifact:** `studies/expedition-witness-zeno-schur/probe4_witness_zeno_results.json`
- **On-Disk Canonical SHA-256 (`sha256sum`):** `899d65178959d397a1121ec0a494dbe9cf6a5e7fd2ef2ecb29ef4f22b30c3451` *(compact-JSON SHA-256: `62764f0206a250aed0bf4878f33ada2a38110653fe14f41ea74334a3bdb93b43`)*
- **Repro (`-I -O -B -W error`, 100% pure Python 3 stdlib — zero NumPy/SciPy, zero floats in Parts A & B, zero bare `assert`s):**
  ```sh
  python3 -I -O -B -W error \
    studies/expedition-witness-zeno-schur/probe4_witness_zeno_schur.py
  ```

### 5.1 Part A — Exact Multipole Scaling, Dipole Cancellation & Huygens–Steiner DSW Mass-Quadrupole Split (Pure $\mathbb{Q}$ / $\mathbb{Q}(i)$)
Across 6 nontrivial zero-CM rational $N$-particle configurations ($N \in \{2, 3, 4, 5, 7, 10\}$, $\sum_{j=1}^N \xi_j = 0$):
- **Macroscopic CM Cube Law:** $\Gamma_{\mathrm{CM}}^{(2)} = N^2 \Gamma_1^{(2)}$ and $t_{\mathrm{wave}}^{\mathrm{CM}} = N t_{\mathrm{wave}}^{(1)} \implies W_{\mathrm{CM}}(N) \equiv N^3 W_{\mathrm{single}}$ identically.
- **Exact Dipole Cancellation & Quadrupole Tidal Floor:** On pure internal shape superpositions ($\Delta R = 0, \sum \xi_j = \sum \xi'_j = 0$), BOTH $O(k^0)$ and $O(k^2)$ vanish identically over $\mathbb{Q}$, leaving $\Gamma_{\mathrm{int}}^{(4)} = \frac{\gamma_0 k^4}{8}(\Delta I_{\mathrm{int}})^2$ and exact protection ratio $\mathcal{P}_{\mathrm{inv}} = \frac{4 N^2 (\Delta R)^2}{k^2 (\Delta I_{\mathrm{int}})^2}$.
- **Observer-Invariant Subspace $\mathcal{F}^{\mathrm{inv}}$:** Isometric permutation modes vanish identically through $O(k^{10})$; asymmetric parity-reflected modes vanish identically through $O(k^4)$ (activating only at $O(k^6)$ octupole `27/40`).
- **Huygens–Steiner / DSW Black-Hole Mass-Quadrupole Separation Lemma:** $Q(R, \xi) = \sum_j m(R + \xi_j)^2 \equiv N m R^2 + m I_{\mathrm{int}}(\xi)$ with exact zero cross-term iff $\sum_j \xi_j = 0$, proving Danielson–Satishchandran–Wald gravitational horizon witnessing (`witness-map/model.js` line 105) obeys the exact $N^3$ CM cube law while leaving quadrupole-preserving internal modes ($\Delta I_{\mathrm{int}} = 0$) completely unwitnessed!
- **Negative Control (broken CM $\sum \xi_j = 1 \ne 0$):** Immediately restores $O(k^2)$ internal decoherence (`3/10`) and nonzero mass-quadrupole cross-term (`35/11`).

### 5.2 Part B — First-Principles $16\times 16$ GKSL Lindblad Superoperator, Tomita–Takesaki Modular Flow, Exact Schur Complement & EP2 Phase Boundary (Pure $\mathbb{Q}$ / $\mathbb{Q}(i)$ + `math.isqrt`)
Constructed directly from $4\times 4$ matrix commutators & dissipators over exact Gaussian rationals $\mathbb{Q}(i)$ in the orthonormal Pauli basis $\{I,Z\}\otimes\{I,X,Y,Z\}$ ($\mathcal{V}_{\mathrm{inv}}$) $\oplus$ $\{X,Y\}\otimes\{I,X,Y,Z\}$ ($\mathcal{V}_{\mathrm{wit}}$) for $H = g(X\otimes Z) + \omega_{\mathrm{rel}}(I\otimes Z)$, $L_{\mathrm{CM}} = Z\otimes I$ ($\gamma_{\mathrm{CM}} = N^2 \gamma_1$), $L_{\mathrm{tid}} = Z\otimes Z$ ($\gamma_{\mathrm{tid}}$):
1. **Exact Tomita–Takesaki Modular Flow Commutation (`S1:F[370]`):** On an explicit **non-diagonal, non-product** faithful density matrix $\rho_S = \frac{2}{5}|0\rangle\langle 0|\otimes\rho_0 + \frac{3}{5}|1\rangle\langle 1|\otimes\rho_1 \in \mathcal{V}_{\mathrm{inv}}$ with $[\rho_0, \rho_1] \ne 0$ (verified PD via exact Sylvester minors), the $16\times 16$ exact modular operator $\Delta_{\rho_S}(A) = \rho_S A \rho_S^{-1}$ satisfies $\Delta_{\rho_S} = \Delta_{\rho_S}^\dagger$, $[\mathcal{D}[Z\otimes I], \Delta_{\rho_S}] \equiv 0$ (all 256 entries exact `0` $\implies [\mathcal{E}_t, \sigma_s^{\rho_S}] = 0$ for all $s, t \in \mathbb{R}$), and exact KMS quantum detailed balance. All 3 negative controls (coherent CM state $\rho_S + \frac{1}{20}(X\otimes I)$; local witness $I\otimes Z$; entangling witness $Z\otimes X$) strictly break commutation!
2. **Exact $8\times 8$ Schur Complement Across $N \in \{1, 2, 3, 5, 10, 20, 50, 100\}$:** $\mathcal{L}_{\mathrm{eff}}^{\mathrm{inv}} = \mathcal{L}_{\mathrm{inv,inv}} - \mathcal{L}_{\mathrm{inv,wit}}\mathcal{L}_{\mathrm{wit,wit}}^{-1}\mathcal{L}_{\mathrm{wit,inv}}$ is identically diagonal with:
   - `II`, `IZ`: exact **`0`** for ALL $(N, g, \gamma_1, \gamma_{\mathrm{tid}})$ (exact $\mathcal{F}^{\mathrm{inv}}$ pointer conservation);
   - `IX`, `IY`: exact **`-(2\gamma_{\mathrm{tid}} + 2g^2/(N^2\gamma_1))`** ($1/N^2$ Zeno sealing!);
   - `ZI`, `ZZ`: exact **`-2g^2/(N^2\gamma_1 + \gamma_{\mathrm{tid}})`** (CM pointer freezing!);
   - `ZX`, `ZY`: exact **`-2\gamma_{\mathrm{tid}}`** (immune to $g$).
3. **Exact Exceptional-Point (EP2) Jordan Blocks & Zero-Float `isqrt` Eigenvalue Brackets:**
   - At $\gamma_{\mathrm{tid}} = 0, \gamma_{\mathrm{CM}} = 2g$ ($N_{\mathrm{EP}} = 4, g = 2, \gamma_1 = 1/4$): exact nilpotent $N_{\mathrm{EP}} \ne 0, N_{\mathrm{EP}}^2 = 0, \operatorname{rank}(N_{\mathrm{EP}}) = 1$, full $16\times 16$ ranks `(12, 8)` (4 simultaneous EP2 blocks); at $\gamma_{\mathrm{tid}} = 1, \gamma_{\mathrm{CM}} = 5, g = 2$: split EP2 isolates the 2 internal blocks `IX, IY` with exact ranks `(14, 12)`.
   - In the overdamped Zeno regime ($\gamma_{\mathrm{CM}} - \gamma_{\mathrm{tid}} > 2g$), 80-bit `isqrt` brackets certify $(-\lambda_{\mathrm{slow}})(-\lambda_{\mathrm{fast}}) = 2\gamma_{\mathrm{CM}}\Gamma_{\mathrm{Schur}}$ and $O(N^{-4})$ convergence $-\lambda_{\mathrm{slow}}/\Gamma_{\mathrm{Schur}} \to 1$ (`1.0655` at $N=5$ $\to$ `1.00000036` at $N=100$).
4. **Exact Riccati Slow-Manifold Bridge to Probe 1:** Running Probe 1's exact recursion $H_0 = g/\gamma_{\mathrm{CM}}$ (Schur complement) $\to H_{k+1} = (g + \gamma_{\mathrm{tid}} H_k + g H_k^2)/\gamma_{\mathrm{CM}}$ drives the exact Riccati commutation defect $\mathcal{R}[H_k]$ from `1.2e-2` down to `2.36e-15` in 6 steps (`rate_err = 1.43e-16`), proving Probe 1's AeST slow-manifold closure and Probe 4's Lindblad Zeno Schur complement obey the **same algebraic Riccati operator**.
5. **Soliton Clock Separation, $O(16,\mathbb{Q})$ Basis Invariance & Witness Negative Controls:** Adding coherent soliton clock $H_{\mathrm{rel}} = \omega(I\otimes Z)$ yields $[\mathcal{L}_{\mathrm{bare}}, \mathcal{L}_{\mathrm{clock}}] \equiv 0$ (zero Lamb shift in resonant rotating frame, Lorentzian static $s=0$ Schur complement); full $O(16,\mathbb{Q})$ Householder similarity preserves $\operatorname{tr}(\mathcal{L}^k)$ ($k=1..4$) and block $O(8,\mathbb{Q})$ preserves Schur covariance identically; replacing $Z\otimes I$ with local $I\otimes Z$ degrades internal coherence by `250.1x` at $N=10$, and entangling $Z\otimes X$ destroys `IZ` (`0 -> 50`).

### 5.3 Part C — Quantitative Calibration Against `fractals/witness-map/model.js` & `gravity` `C-03`
1. **Exact Cross-Repo Soliton Reconciliation (`witness-map/model.js` $\leftrightarrow$ `gravity` `C-03`):**
   Replaying `model.js` `SOL` ($h = 4\times 10^{-3}$) resolves an apparent factor-of-$1.465$ constant mismatch between the two repos: `model.js` evaluates $M_{\mathrm{sol}} r_c = 2.6794\,\hbar^2/(G m^2)$ at the **half-density** radius $x_c = 1.2993$, whereas `gravity` `C-03` evaluates $M_{\mathrm{sol}} r_{1/2} = 3.9251\,\hbar^2/(G m^2)$ at the **half-mass** radius $x_{1/2} = 1.9033$ (relative discrepancy **`1.45e-6`**, exact universal ratio $r_{1/2}/r_c = 1.4649$).
2. **Sgr A* Black-Hole Horizon Unification Across All 3 `CROWDS` (at $b = 8.18\text{ kpc}$, verifying $\Delta x < b/10$):**

| Crowd (`model.js`) | $m$ (eV) | $\log_{10} N$ | $\log_{10} W_{\mathrm{BH}}^{(1)}$ | $\log_{10} W_{\mathrm{BH}}^{\mathrm{CM}}$ | $1/N^2$ Zeno | $\tau_{\mathrm{BH}}^{\mathrm{CM}}$ (s) | Decoheres in $t_{\mathrm{lump}}$ / Age? |
|---|---:|---:|---:|---:|---:|---:|---|
| `sun` (MW halo) | $10^{-22}$ | `93.04` | `-159.10` | **`+120.01`** | `10^-186.1` | **`2.41e-14`** | **YES / YES** (`24 fs`!) |
| `sun-heavy` (MW halo) | $3\times 10^{-19}$ | `79.13` | `-169.53` | **`+67.85`** | `10^-158.3` | **`1.42e+21`** | **NO / NO** (`3263x` cosmic age!) |
| `core` (Eridanus II @ 8.18 kpc) | $8\times 10^{-23}$ | `96.85` | `-154.76` | **`+135.80`** | `10^-193.7` | **`7.14e-25`** | **YES / YES** |

3. **Sharp Physical Scaling Law Discovered:** Because $m_{\mathrm{lump}} \propto \rho \lambda^3 \propto m^{-3}$ and $\lambda \propto m^{-1}$, Sgr A*'s gravitational horizon rate obeys **$\Gamma_{\mathrm{BH}}^{\mathrm{CM}} \propto m^{-10}$**, $\Gamma_{\mathrm{BH}}^{\mathrm{CM}} t_{\mathrm{lump}} \propto m^{-11}$, and $W_{\mathrm{BH}}^{\mathrm{CM}} \propto m^{-15}$ (verified to `0.0` log10 residual). Thus, at the Sun's orbit (`8.18 kpc` from Sgr A*), **Sgr A*'s horizon alone** decoheres a $10^{-22}\text{ eV}$ lump's CM in **24 femtoseconds** (while Zeno-sealing internal interference by $10^{-186}$), whereas above **$m_* = 2.83\times 10^{-20}\text{ eV}$** ($\tau = t_{\mathrm{lump}}$) and **$m_{\mathrm{age}} = 1.34\times 10^{-19}\text{ eV}$** ($\tau = 13.8\text{ Gyr}$) — right inside Dalal & Kravtsov's ultra-light dark matter window — Sgr A*'s horizon is no longer fast enough to decohere the lump CM within a lump lifetime or cosmic age!
- **Falsification criterion:** Any nonzero entry in $[\mathcal{D}[Z\otimes I], \Delta_{\rho_S}]$, any nonzero residual in the $8\times 8$ exact Schur complement or $O(16,\mathbb{Q})$ invariance, any R3/modular/witness negative control failing to trigger, any violation of $W_{\mathrm{CM}} / W_1 = N^3$, or any discrepancy $> 5\times 10^{-4}$ between `SOL` half-mass invariant and `gravity` `C-03`.

---

## 6. Cross-Domain Unification & High-Leverage Next Branches

Probes 1, 3, and 4 directly supply two of the seven exact algebraic fiber-elimination / Schur-complement laws documented in `cartography/frontier_portals.md` Portal 10 (AeST fast-scalar Hamiltonian Schur complement + Riccati lift $\mathcal{R}[H]=0$; Lindblad CM-witness Zeno Schur complement + Riccati lift), while Probe 2 executes the real-data Outside-Anchor Latch test (`SEAM-03`) and repairs Session 1's blind chirp estimator (`ep-03`). High-leverage follow-on branches for dedicated workers:
1. **Nonlinear AeST Caustic & Baryon-Segregation Evolution (`gravity/research/value-assessment-20261112/closure/caustic_control.py`):** Test whether the $\lambda_s = 0$ zero-sound-speed Yukawa cutoff $G_{AA} = M_0^2/(M_0^2+k^2/a^2)$ survives spherical collapse without developing the caustic instabilities that afflict $\lambda_s > 0$ anti-gravity.
2. **Dark-Matter Horizon-vs-Stellar Decoherence Map (`fractals/witness-map`):** Extend Probe 4 Part C's $\Gamma_{\mathrm{BH}}^{\mathrm{CM}} \propto m^{-10}$ crossover (`m* = 2.83e-20 eV` at Sgr A*) by adding stellar gravitational scattering (`tStir` in `model.js`) to determine the exact boson mass boundary where galactic wave dark matter transitions from horizon-decohered to star-decohered CM classicality.
3. **Exact Zero-Float Morse/Hessian Certification for `relative-equilibria` ($n=8$) & `certified-orbits`:** Combine Probe 3's exact Bunch–Kaufman rational box certifier with `@spectral-prover`'s Track B complex-Hermitian Bernstein box certifier (`branches/spectral-inertia/`).
