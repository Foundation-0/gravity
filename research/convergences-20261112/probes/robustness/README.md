The probes independently test selected inferences in the convergence reports. They do not import peer scripts or change the four source repositories. NumPy is required.

```bash
cd research/convergences-20261112
python3 probes/robustness/robustness_probes.py
python3 probes/robustness/robustness_probes.py --check
```

The first command writes `results.json` beside the script. The second compares recomputed results without writing. No physical dataset is fitted. Floating-point comparisons use explicit tolerances. The Press-Schechter redshift values are read from the existing gravity artifact and identified as such.

**Spring derivation**

For a bond from site i to translated site j with vector b and unit direction e, its first-order extension at zero Bloch wavevector is e·(u_j−u_i). The corresponding row of C has entries −e and +e. With equal unit masses and spring constants, D=CᵀC.

The twelve internal octahedron bars give tr(D_int²)=60. The three bridges have disjoint site pairs and contribute tr(D_bridge²)=12. Their directions are e_i=(a unit_i+t C_i)/sqrt(2), with a²+2t²=2. Each bridge meets eight internal bar ends.

At either endpoint on coordinate axis i, the sum of internal direction outer products is diag(2,1,1), with 2 in direction i. For both endpoints the sum of squared bridge/internal dot products is 2+2(e_i)_i². Counting both cross terms in the trace and all bridges gives 12+6a².

Therefore tr(D²)=60+12+12+6a²=96−12t². Each of fifteen rows has squared norm two, so tr(D)=30.

The internal octahedron is infinitesimally rigid. At t=0 all three motif rotations stretch no bridge. At t≠0 the bridge constraints on rotation vector w are proportional to (0,1,−1)·w, (−1,0,−1)·w, and (1,1,0)·w. The third is the first minus the second, leaving w proportional to (−1,1,1).

Translations add three null modes. Thus the fixed-cell, zero-wavevector nullity is six at the open endpoint and four otherwise. Since C has fifteen rows and eighteen columns, the corresponding self-stress counts are three and one. This is an infinitesimal statement, not nonlinear stability or topological protection.

A separate check stretches the actual bonds by ±epsilon times a seeded displacement and computes the spring energy from their lengths. Its symmetric second difference agrees with the quadratic matrix energy. No new contacts are activated at the fcc endpoint.

**Quantum records**

The isometries map system basis states to either product branches |00>, |11> or Bell branches |Phi+>, |Phi−>. Orthogonality of the branch pair makes both maps complete dephasing channels. The script checks the image of every system matrix unit.

For an equal-amplitude input the two-qubit environment branches have identical one-qubit marginals in the Bell case. No local measurement reveals system Z. A joint Bell measurement does. Total system-fragment mutual information remains one bit for either one-qubit fragment in both examples.

The Bell example does contain information about a different system basis for the chosen input. The absence is explicitly about Z. The five-qubit example in the relations route addresses absence of all system information from smaller fragments.

An environment-only unitary relates the constructions. With fixed fragment access, implementing this entangling unitary is a physical change. A coordinate change that transforms states and all observables together changes no outcome probabilities.

**Information and calibration**

For known linear design A and independent Gaussian noise variance s², F=AᵀA/s². Joining rows adds constraints. Repeated rows increase precision in the same direction, leaving the same null space.

An unknown common gain preserves the scaling symmetry (q,b,g)→(a q,a b,g/a). A known-amplitude calibration measurement breaks it. This example concerns a known forward model and is not nonlinear independent component analysis.

Under theta'=S theta, F'=S^(-T) F S^(-1). Its eigenvalues can change while dthetaᵀ F dtheta is unchanged for corresponding displacements. The probe checks this identity directly.

For y_i=q+b+e_i with b Gaussian of unit variance and independent e_i of variance 0.01, marginal covariance is Sigma=11ᵀ+0.01 I. Thus 1ᵀSigma^(-1)1=n/(n+0.01). Independent-offset covariance instead gives n/1.01. The table compares two different noise assumptions.

**Gravity**

Steady spherical Jeans balance with constant radial dispersion gives Vc²=(gamma−2 beta)sigma_r². It does not directly supply the projected dispersion of a real disk or group.

The cooling formula is evaluated from dimensional constants, density, composition and the chosen clock. For free-free cooling, t_cool is proportional to sqrt(T)/n_e. With kT=mu m_p sigma², the boundary sigma is proportional to n_e t_available.

At density Delta rho_crit, n_e is proportional to Delta H². A Hubble clock gives sigma proportional to Delta H. A free-fall clock gives sigma proportional to sqrt(Delta) H, since t_ff=pi/(2 sqrt(Delta) H). Large clock changes may leave the ionized free-free regime, requiring a different cooling function.

For density proportional to r^(-gamma) and gamma<3, the mass fraction within xR is x^(3−gamma). Its derivative is finite at gamma=2. The separate trapped-fraction ansatz cannot be inferred from the smooth hydrostatic expression. No stability mode is calculated.

The collapse-dispersion column is read from the source certificate. It is not an independent Boltzmann-code or transfer-function validation. That source file's hash is stored in `results.json`.

**AeST derivative**

The published scalar terms are L=(2−KB)(2J·dphi−Y)−F(Y,Q), with Y=q^(mu nu)d_mu(phi)d_nu(phi) and Q=A^mu d_mu(phi). Varying the covector dphi gives the current in the report. Integration by parts yields its continuity equation.

The probe uses a generic polynomial depending on both Y and Q and sixteen seeded configurations with normalized timelike A and acceleration orthogonal to A. Finite differences independently check the algebraic derivative. This does not show the chosen polynomial is physically viable or supply a fluid closure, entropy law or energy-retention mechanism.
