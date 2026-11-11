# Claims, Proofs, and Falsification Ledger (`Foundation-0/gravity`)

Every mathematical and numerical claim in this repository carries an explicit `Foundation-0` epistemic label:
- **`KNOWN`** — Published literature result with direct citation.
- **`PROVEN`** — Exact analytical derivation or mathematical inequality stated with all assumptions.
- **`VERIFIED`** — Independently checked by `verify_all.py` against analytical benchmarks.
- **`NEW-COMPUTATION`** — Quantitative numerical evaluation or parameter-space bound produced in `results/certificates.json`.
- **`CONJECTURE`** — Testable physical hypothesis with an explicit observational falsification criterion.

## C-01: Coordinate-Fractal vs. Field-Gradient Dichotomy (`PROVEN` / `VERIFIED`)

- **Statement:** Let a compact baryonic distribution of mass $M_b$ source a modified radial gravitational acceleration via an isotropic coordinate-space fractal measure of Hausdorff dimension $D_f$ above a universal length scale $\ell_*$ (Calcagni 2010, Phys. Rev. Lett. 104, 251301; Briscese & Calcagni 2026, arXiv:2603.24593):
  $$g_{\text{coord}}(r) = \frac{G M_b}{r^2}\left(1 + \frac{r}{\ell_*}\right)^{3 - D_f}.$$
  For $r \gg \ell_*$, $v^2(r) = r g_{\text{coord}}(r) \simeq (G M_b / \ell_*^{3 - D_f})\, r^{2 - D_f}$. Requiring asymptotically flat rotation curves ($\lim_{r\to\infty} d\ln v / d\ln r = 0$) uniquely fixes $D_f = 2$, which forces $v_{\text{flat}}^2 = G M_b / \ell_*$, locking the Baryonic Tully-Fisher exponent to $\beta_{\text{BTFR}} \equiv d\ln M_b / d\ln v_{\text{flat}} = 2$.
- **Numerical Verification (`verify_all.py` -> `check_1_dichotomy`):** Across 51 galaxies spanning $M_b \in [10^7, 10^{12}]\,M_\odot$ with $R_b \propto M_b^{0.28}$ and $\ell_* = 3.0\text{ kpc}$, least-squares yields $\beta_{\text{BTFR}} = 2.0186$ and a 2D radial-acceleration RMS residual of $0.6234\text{ dex}$ against the empirical SPARC Radial Acceleration Relation (McGaugh, Lelli & Schombert 2016, Phys. Rev. Lett. 117, 201101).
- **Implication:** Dimensional reduction $D_{\text{eff}}: 3 \to 2$ must be driven by the **local field gradient** $|\nabla\Phi| / a_0$ (selecting $r_M(M_b) = \sqrt{G M_b / a_0}$), never a fixed coordinate scale $\ell_*$.

## C-02: Spectral Dimension $d_s = 1$ Selection of the $q = 3/2$ Superfluid Action (`PROVEN` / `VERIFIED`)

- **Background (`KNOWN`):** Quantum trajectories exhibit Hausdorff dimension $D_H = 2$ below $\lambda_{\text{dB}}$ (Abbott & Wise 1981, Am. J. Phys. 49, 37). In 3D conformal non-relativistic superfluids, scale invariance fixes the phonon Lagrangian to $\mathcal{L}(X) = P(X) \propto |X|^{5/2}$ (Son & Wingate 2006, Ann. Phys. 321, 197, arXiv:cond-mat/0509786), whereas galactic superfluid dark matter requires $\mathcal{L}(X) \propto |X|^{3/2}$ (Berezhiani & Khoury 2015, Phys. Rev. D 92, 103510).
- **Derivation (`PROVEN`):** For a scale-invariant non-relativistic quantum condensate whose low-energy collective modes occupy spectral dimension $d_s$ ($N(k) \propto k^{d_s}$, $\varepsilon_k \propto \hbar^2 k^2 / 2m$), $n = \partial P / \partial \mu \propto \mu^{d_s / 2}$ integrates to:
  $$\mathcal{L}_{\text{eff}}(X) = P(X) \propto \left(\frac{2 m}{\hbar^2}\right)^{d_s / 2} |X|^{1 + d_s / 2}, \qquad q(d_s) = 1 + \frac{d_s}{2}.$$
  In the static phonon regime ($|X| \propto |\nabla\theta|^2$), varying $\int d^3x\,[c_0 |\nabla\theta|^{2 + d_s} - \lambda \theta \rho_b]$ yields the $p$-Laplacian $\nabla \cdot (|\nabla\theta|^{d_s}\nabla\theta) \propto \rho_b$ ($p = 2 + d_s$). By 3D Gauss flux conservation, $4\pi r^2 |\theta'(r)|^{1 + d_s} \propto M_b$, giving $v^2(r) = r g_{\text{ph}}(r) \propto (G M_b)^{1/(1 + d_s)} r^{1 - 2/(1 + d_s)}$. Setting $1 - 2/(1 + d_s) = 0$ uniquely selects **$d_s = 1$** ($q = 3/2$, $p = 3$, 1D filamentary / Tonks-Girardeau scaling $P \propto n^3$), simultaneously locking $M_b \propto v_{\text{flat}}^4$ ($\beta = 4$).
- **Numerical Verification (`verify_all.py` -> `check_1_dichotomy`):** Sweeping $d_s \in [0.0, 3.0]$ confirms only $d_s = 1.00$ yields both $d\ln v / d\ln r = -0.01468$ ($100\text{--}300\text{ kpc}$) and $\beta = 3.8945$, matching SPARC RAR to $0.0096\text{ dex}$ RMS.

## C-03: Macro-Quantum "Gravitational Atom" Soliton Bound (`VERIFIED`)

- **Verification (`verify_all.py` -> `check_2_gravitational_atom`):** Pure-stdlib RK4 shooting of $\nabla_\xi^2 \hat{\psi} = 2(\hat{\Phi} - \hat{\varepsilon})\hat{\psi}$, $\nabla_\xi^2 \hat{\Phi} = \hat{\psi}^2$ certifies $\hat{\varepsilon}_0 = 0.64953399$, $\xi_c = 1.299271$, $\xi_{1/2} = 1.903322$, and $M_{\text{sol}} r_{1/2} = 3.9251\,\hbar^2 / (G m_\psi^2)$ (matching $3.925$ in Hui et al. 2017, Phys. Rev. D 95, 043541; cf. Schive et al. 2014, arXiv:1406.6586; Chavanis 2018, arXiv:1706.05900). Outside $2.5\,\xi_{\text{peak}}$, the pure ground state decays with Keplerian slope $d\ln v / d\ln r = -0.4994$.

## C-04: Single-Boson 1 Mpc vs. Bullet Cluster Phase-Space Inversion (`PROVEN` / `NEW-COMPUTATION`)

- **Statement:** Bose-Einstein condensation of a single thermalized species of mass $m_\psi$ requires $\mathcal{N}_{\text{deg}} \equiv n \lambda_{\text{th}}^3 = (2\pi)^{3/2}\hbar^3 m_\psi^{-4} (\rho / \sigma_{\text{1D}}^3) \ge \zeta(3/2) \approx 2.6124$, monotonic in $Q \equiv \rho / \sigma_{\text{1D}}^3$.
- **Evaluation (`verify_all.py` -> `check_3_phase_space_and_tower`):**
  1. Condensing at $r = 1\text{ Mpc}$ around an isolated $L_*$ spiral ($M_b = 6 \times 10^{10}\,M_\odot$, $v_{\text{flat}} = 175.82\text{ km/s}$; Mistele et al. 2024, arXiv:2406.09685) requires $m_\psi \le 1.9379\text{ eV}$ (unbroken $r^{-2}$ profile) and **$m_\psi \le 1.0306\text{ eV}$** (NFW outer tail).
  2. Melting out of degeneracy ($\mathcal{N}_{\text{deg}} < \zeta(3/2)$) inside the Bullet Cluster core ($r = 250\text{ kpc}$, $\sigma_{\text{1D}} = 1000\text{ km/s}$; Clowe et al. 2006, arXiv:astro-ph/0608407) requires **$m_\psi \ge 2.3015\text{ eV}$**.
  3. Since $1.0306\text{ eV} < 1.9379\text{ eV} < 2.3015\text{ eV}$, no single thermalized boson species satisfies both regimes simultaneously.

## C-05: Two-Tier Hybrid Condensate + Normal Dark Sector (`NEW-COMPUTATION` / `CONJECTURE`)

- **Evaluation (`verify_all.py` -> `check_3_phase_space_and_tower`):** Partitioning dark matter into a light condensate mode ($m_L = 0.05\text{ eV}$, $f_L = 0.02$) and a heavy mode ($m_H = 3.0\text{ eV}$, $f_H = 0.98$) yields $\mathcal{N}_{\text{deg},L}(1\text{ Mpc NFW}) = 9{,}432.49 \gg \zeta(3/2)$ (sustaining galactic Mpc phonon coherence) while $\mathcal{N}_{\text{deg},H}(\text{Bullet}) = 0.8867 < \zeta(3/2)$ (collisionless cluster lensing peak, with internal $g_{\text{cl}} = 2.161\,a_0$ screens the light-mode phonon force). Alternatively, a relativistic $T = 0$ vacuum condensate (Skordis & Zlosnik 2021, Phys. Rev. Lett. 127, 161302) avoids thermal occupancy constraints via vacuum coherence.
- **Falsification Criterion:** Test environmental dependence of $0.3\text{--}1.5\text{ Mpc}$ weak-lensing rotation curves between void/field galaxies and group satellites in Euclid DR1/DR2.

## C-06: Discrete Scale-Invariant Soliton Tower Smoothness Bound (`NEW-COMPUTATION`)

- **Evaluation (`verify_all.py` -> `check_3_phase_space_and_tower`):** Superposing self-similar solitons $m_k = m_0 b^{-k}$ (Arvanitaki et al. 2010, Phys. Rev. D 81, 123530) with $R_k = R_0 b^k, M_k \propto R_k$ yields log-periodic velocity ripples across $10\text{--}200\text{ kpc}$ of $\pm 0.036\%$ ($b=2$), $\pm 1.572\%$ ($b=4$), $\pm 4.561\%$ ($b=6$), and $\pm 6.084\%$ ($b=7$), requiring **$b \le 6.2$** for $\le 5\%$ smoothness.

## C-07: External-Field Rollover at ~0.83 Mpc & Wide-Binary UV-Crossover Sensitivity (`VERIFIED` / `NEW-COMPUTATION`)

- **Evaluation (`verify_all.py` -> `check_4_efe_and_wide_binaries`):**
  1. For an $L_*$ galaxy ($r_M = 8.348\text{ kpc}$) in a cosmic external field $e = g_{\text{ext}}/a_0 = 0.010$, $R_{\text{EFE}} = r_M / e = 834.8\text{ kpc}$, matching the $\sim 1\text{ Mpc}$ flatness horizon of Mistele et al. (2024) alongside $c H_0 / (2\pi) = 1.042 \times 10^{-10}\text{ m/s}^2$ (Planck Collaboration 2020, arXiv:1807.06209) and $c H_0 / 6 = 1.091 \times 10^{-10}\text{ m/s}^2$ (Verlinde 2017, SciPost Phys. 2, 016).
  2. At the Solar circle ($e_{\text{MW}} = 1.8101$, $r_M(\odot) = 7{,}029.9\text{ AU}$), 3D AQUAL quadrature gives an asymptotic wide-binary velocity boost of **$+18.31\%$** for $\mu_1(x) = x/(1+x)$ versus **$+3.16\%$** for $\mu_2(x) = x/\sqrt{1+x^2}$, showing Gaia DR3 wide binaries (Banik et al. 2024, arXiv:2311.03436) directly probe the UV crossover sharpness of $\mathcal{L}(X)$.

## C-08: Empirical Scale-Flow Convergence onto d_s* = 1.00 Across 2,630 SPARC RAR Points and 139,027 KiDS 1-Mpc Lenses (`VERIFIED` / `NEW-COMPUTATION`)

- **Evaluation (`wave3_empirical_audit.py` -> `fit_1_sparc_rar_spectral_dimension`, `fit_2_scale_flow_and_btfr`, `fit_3_cosmic_efe_bound`):**
  1. On the 14 empirical SPARC RAR bins (2,630 points), joint profile likelihood gives $\hat{d}_s = 0.94 \pm 0.02$ ($\hat{a}_0 = 1.2525 \times 10^{-10}\text{ m/s}^2$; canonical $d_s = 1.0$ gives $\hat{a}_0 = 1.1793 \times 10^{-10}\text{ m/s}^2$), rejecting Newtonian no-DM ($\chi^2 = 31,125.1$) and rejecting frozen $d_s = 0.75$ by $\Delta\chi^2 = +73.84$.
  2. Splitting inner kinematic SPARC bins ($10\text{--}30\text{ kpc}$, $\hat{\beta} = 3.83 \iff d_s^{\text{eff}} = 0.915$) from outer KiDS-1000 spherical weak-lensing bins ($50\text{--}1000\text{ kpc}$, unconstrained fit $\hat{\beta} = 4.00 \iff d_s^{\text{IR}} = 1.00$, $\chi^2 = 0.634$ for 2 dof) shows direct convergence onto the $d_s^* = 1$ infrared fixed point once finite-disk geometry and UV crossover vanish, while rejecting coordinate-fractal $D_f = 2$ by $\Delta\text{BIC} = +402.59$ and $d_s = 0.75$ ($\beta = 3.5$) by $\Delta\text{BIC} = +9.10$.
  3. Comparing KiDS $V_{\text{flat}}(50\text{--}300\text{ kpc})$ vs. $V_{\text{flat}}(50\text{--}1000\text{ kpc})$ bounds the cosmic external field around isolated lenses to $e_{\text{cosmic}} = g_{\text{ext}} / a_0 \le 0.0160$ (95% CL; $R_{\text{EFE}}(L_*) \ge 521.8\text{ kpc}$).
