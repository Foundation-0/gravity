# Physical AeST preparations and their linear gravitational response

Two AeST field states can satisfy all linear constraints and have the same initial effective density, momentum and metric while producing different pressure and later gravitational potentials. The calculation below establishes this for one specified expanding background. It also shows why the corresponding Minkowski test has no linear stress response.

This is a classical linear calculation for the tracking action fixed in [protocol.md](protocol.md). Independent review of the expanding-background action and constraint map is pending. It does not establish thermalization, caustic regularization, a halo pressure law or a fit to cosmological observations.

The new contribution is the explicit constraint map and reproducible preparation response. The underlying action, mode count and Minkowski spectrum are published results. The analytical stability arguments below are author calculations awaiting independent review.

## 1. A background with nonzero effective density

Retain \(K_B=1\), \(\lambda_s=1\), \(\mathcal K_2=2\), no matter and no cosmological constant. Write

\[
\mathcal K(Q)=2(Q-Q_0)^2,\quad K'=4(Q-Q_0),\quad K''=4,
\quad Q=\dot{\bar\phi},\quad Q_0>0.
\]

Primes here differentiate \(\mathcal K\) with respect to \(Q\). They are not time or scale-factor derivatives. The homogeneous scalar equation and Einstein equations give

\[
a^3K'=\text{constant},\quad
Q=Q_0+q_i a^{-3},\quad
3H^2=R\equiv QK'-\mathcal K,
\quad\dot H=-\frac{QK'}2.
\]

Choose \(a_i=1\) and \(q_i=0.01Q_0\), with the expanding root \(H>0\). In units \(Q_0=1\), \(R_i=0.0402\), \(H_i=0.115758369\), \(w_i=\mathcal K/R_i=0.004975124\), and \(c_{\rm ad,i}^2=K'/(QK'')=0.009900990\).

Here \(R=8\pi\widetilde G\bar\rho\). In dimensionless units the exact solution satisfies \(a^3=1+3H_it+3q_it^2\). The finite interval \(1\leq a\leq2\) lasts \(10.547115474/Q_0\). This is an AeST-only FLRW solution of the stated background equations. It is not the observed matter era, and the quadratic \(\mathcal K\) is not extrapolated to the early universe.

The homogeneous equations follow from the action and agree with the background relations in [Skordis and Zlosnik, Cosmological observables](https://arxiv.org/html/2007.00082v3). Their displayed cosmological vector equation uses the zero-gradient-slope branch. Our nonzero \(\lambda_s\) contributes an extra term derived below.

## 2. Quadratic action and canonical map

Use cosmic time and Newtonian gauge. Define \(v=\varphi\), \(\chi=v+Q\alpha\), \(E=\dot\alpha+\Psi\), \(\gamma=\dot v-Q\Psi\), \(b=2-K_B\), and \(r=k^2/a^2\). Multiplying the action by \(16\pi\widetilde G\), the quadratic Lagrangian for one real Fourier component is

\[
\begin{aligned}
L_g^{(2)}={}&a^3[-6\dot\Phi^2-12H(\Phi+\Psi)\dot\Phi
-9H^2(\Phi+\Psi)^2]+ak^2(2\Phi^2-4\Phi\Psi),\\
L_A^{(2)}={}&a^3[K''\gamma^2+(QK'-\mathcal K)\Psi^2
-6K'\Phi\gamma-6\mathcal K\Psi\Phi+3\mathcal K\Phi^2]\\
&+ak^2[K_BE^2+2bE\chi-b(1+\lambda_s)\chi^2
+K'(2\alpha v+Q\alpha^2)].
\end{aligned}
\]

The common positive Fourier-volume factor is suppressed. The gravitational part uses the ADM action with its usual boundary term removed. Its remaining \(H\Phi\dot\Phi\) term has not been integrated by parts. This choice fixes the canonical momentum convention.

The scalar gradient part follows from \(\mathcal Y^{(2)}=a^{-2}|\nabla\chi|^2\), \(J^i\nabla_i\phi+J^0\dot\phi=a^{-2}\nabla E\cdot\nabla\chi\), and the second-order expansion of \(Q\). The last bracket contains the terms proportional to the nonzero background \(K'\). Omitting them would silently return to the vacuum benchmark.

For clarity, the displayed action has zero shift and spatial shear. The lapse equation is varied before imposing \(\Psi=\Phi\). The missing shift and shear equations are retained from the ADM constraints: they give the momentum equation and the equality of metric potentials below. Varying only the displayed, gauge-fixed action would not recover the missing shift constraint.

The scalar momenta are

\[
p_v=2a^3K''\gamma-6a^3K'\Phi,\quad
p_\alpha=2ak^2 Z,\quad Z=K_BE+b\chi,
\]

\[
p_\Phi=-12a^3[\dot\Phi+H(\Phi+\Psi)].
\]

In Newtonian gauge the scalar shear and its conjugate momentum vanish. Lapse and shift have vanishing canonical momenta. The remaining scalar constraints are

\[
C_M=p_\Phi+12a^3H\Phi+6a^3K'v=0,
\]

\[
C_H=-Hp_\Phi+Qp_v-p_\alpha+4ak^2\Phi
+6a^3(QK'-2H^2)\Phi=0.
\]

They are equivalent to

\[
\dot\Phi+H\Psi=\tfrac12K'v,\quad\Psi=\Phi,
\quad C\equiv D+2r\Phi+3HK'v=0,
\]

\[
D\equiv8\pi\widetilde G\delta\rho=QK''\gamma-rZ.
\]

The lapse variation of \(L_g^{(2)}+L_A^{(2)}\) gives
\(-2a^3[6H(\dot\Phi+H\Psi)+2r\Phi+D]\). Substituting the momentum constraint yields \(-2a^3C\). The script verifies this identity symbolically, including the background terms.

The unit-vector constraint is solved by taking the future-directed normalized vector before variation. Its multiplier is then fixed by the temporal vector equation and is not independent initial data. In the auxiliary formulation, \(\mu=b\lambda_s\) is fixed because the chosen function is linear in \(\mathcal Y\). It must not be varied as an independent auxiliary coordinate imposing \(\mathcal Y=0\).

The other auxiliary variable is \(\nu=K'/Q\), with

\[
\delta\nu=\frac{K''Q-K'}{Q^2}\gamma
=\frac{4Q_0}{Q^2}\gamma.
\]

Thus the compensated pair changes this auxiliary variable. Holding it fixed would invalidate the canonical map. The construction agrees with the vacuum limit of [Bataki, Skordis and Zlosnik, equations 84–115](https://arxiv.org/html/2307.15126v3).

## 3. Evolution derived from the action

Variation with respect to \(v\) and \(\alpha\), followed by the constraints, gives

\[
\begin{aligned}
\dot v&=\gamma+Q\Phi,&\dot\alpha&=E-\Phi,\\
\dot\Phi&=-H\Phi+\tfrac12K'v,\\
\dot\gamma&=-3H\gamma+\frac{3K'}{K''}\dot\Phi
+\frac r{K''}[bE-b(1+\lambda_s)\chi+K'\alpha],\\
K_B(\dot E+HE)&=-b[\gamma+\dot Q\alpha+
(H+(1+\lambda_s)Q)\chi]+K'\chi.
\end{aligned}
\]

Here \(\dot Q=-3HK'/K''\). The script evolves these five field variables and checks the constraint separately. It also evolves a second, four-variable formulation with the constraint already eliminated. Agreement checks both the elimination and its numerical propagation.

Define the scaled momentum potential \(m=K'v\) and pressure perturbation \(p=8\pi\widetilde G\delta P=K'\gamma\). The mixed momentum tensor is \(\delta T^0{}_i=-\partial_i m/(8\pi\widetilde G)\). There is no scalar anisotropic stress at this order. The physical momentum amplitude in an orthonormal frame has magnitude \(k|m|/(8\pi\widetilde G a)\).

For the selected constants, let \(W=QK'\), \(c_a^2=K'/(QK'')\). The closed four-state system is

\[
\Phi=-\frac{D+3Hm}{2r},\quad
\gamma=\frac{D+rZ}{QK''},\quad p=c_a^2(D+rZ),
\]

\[
\begin{aligned}
\dot D&=-3H(D+p)+3W(-H\Phi+m/2)-rm,\\
\dot m&=-3Hm+p+W\Phi,\\
\dot\chi&=\gamma+QZ+(\dot Q/Q-Q)\chi
-\frac{\dot Q}{QK'}m,\\
\dot Z&=(-H+Q)Z+(K'-3Q)\chi.
\end{aligned}
\]

The ratio \(\dot Q/K'=-3H/K''\) is regular as the background density tends to zero. Quantities divided by \(\bar\rho\) or \(\bar\rho+\bar P\) are used only on the finite-density branch.

The following checks vanish symbolically for arbitrary \(k,a,H,Q,K',K'',K_B,\lambda_s\) on this quadratic branch:

- \(\dot C+3HC=0\), so constraint-satisfying data remain admissible.
- \(\dot D+3H(D+p)-3QK'\dot\Phi+rm=0\), the effective energy balance.
- \(2[\ddot\Phi+4H\dot\Phi+(2\dot H+3H^2)\Phi]-p=0\), the spatial Einstein trace.

The lensing combination is \(\Phi+\Psi=2\Phi\). Reporting this combination is legitimate here because matter would couple minimally to this metric. No light-ray integration or measured lensing signal is claimed.

## 4. Physical compensated data

At the initial time set the differences in \(v,\alpha,\Phi,\Psi\) and \(\dot\Phi\) to zero. Choose

\[
\Delta E=\varepsilon_E,\qquad
\Delta\gamma=\frac{rK_B}{QK''}\varepsilon_E.
\]

Then \(\Delta p_\Phi=0\), \(\Delta p_\alpha=Q\Delta p_v\), and both canonical constraints vanish. Initially \(\Delta D=\Delta m=0\). Nevertheless

\[
\Delta p=\frac{K'rK_B}{QK''}\varepsilon_E,\quad
\Delta\dot m=\Delta p,\quad
\Delta\dot D=-3H\Delta p.
\]

These states are not related by a gauge transformation. Both \(E\) and \(\chi\) are gauge invariant at linear order. Under a time shift \(T\), \(\alpha\mapsto\alpha+T\), \(v\mapsto v-QT\), \(\Psi\mapsto\Psi-\dot T\), and \(\Phi\mapsto\Phi+HT\). The changed \(E\) cannot be removed this way.

The pressure comparison also has a gauge-independent form:

\[
\delta P-c_a^2\delta\rho=\frac{c_a^2rZ}{8\pi\widetilde G}.
\]

A second allowed preparation has \(D=m=Z=0\) but \(\chi\ne0\). It starts with the same pressure as the unperturbed state, yet

\[
\dot p=c_a^2r(K'-3Q)\chi\ne0.
\]

Consequently, even adding instantaneous pressure to density and momentum does not give an exact autonomous law for every allowed preparation. The fourth variable carries information about the later pressure. A restricted initial ensemble may remove this freedom, but that restriction must be specified and checked.

## 5. Stability scope and the vacuum limit

The flat-space reduced Hamiltonian has canonical pairs \((\chi,p_\chi)\) and \((\alpha,P)\), with \(P=p_\alpha-Q_0p_\varphi\). In units \(Q_0=1\),

\[
H_2=\frac{p_\chi^2}{16}+\frac{(p_\chi+P)^2}{4k^2}
-(p_\chi+P)\chi+3k^2\chi^2-\frac{P^2}{8k^2}.
\]

The three nonzero-coordinate Hessian principal minors are \(6k^2\), \((3k^2+8)/4\), and \((k^2-8)/(16k^2)\). The energy is nonnegative for \(k^2>8\), with the expected flat direction in \(\alpha\). The propagating frequency is \(\omega^2=3k^2/4+2\). The other branch has constant and linear-time solutions.

This reproduces the result of [Skordis and Zlosnik, equations 53–60](https://arxiv.org/html/2109.13287v2). The threshold is not a new stability bound. The Minkowski runs use \(3\leq k/Q_0\leq12\), above that threshold.

On the expanding branch the kinetic terms can be checked in spatially flat gauge. The shift equation fixes the lapse by \(H\Psi=K'v/2\), which contains no field velocities. Eliminating lapse and shift leaves the velocity Hessian \(\operatorname{diag}(2a^3K'',2aK_Bk^2)\) for \((v,\alpha)\). Both entries are positive on the tested branch.

The short-wavelength propagating scalar has positive squared speed \(b(2+K_B\lambda_s)/(K_BK'')=3/4\). Tensor and transverse-vector kinetic signs retain \(0<K_B<2\). Subject to independent verification of the reduction, these checks exclude a scalar kinetic ghost and the fast scalar gradient instability on this background. They do not prove nonlinear stability or exclude slow gravitational growth.

The FLRW runs use \(6\leq k/Q_0\leq24\) and \(1\leq a\leq2\), so \(k/(aQ_0)\geq3\) and \(k/(aH)\geq51.8\). The flat-space threshold provides a comparison scale, not a replacement for the expanding-background kinetic check. No physical cutoff for an ultraviolet completion has been specified, so these are classical benchmark scales.

At \(q_i=0\), \(K'=H=0\), the compensated pair remains physical. The metric is constant, \(\Phi=\Psi=P/(4k^2)\), and \(D=-P/2\). For the compensated difference \(P=0\), all linear density, momentum, stress and metric differences vanish for all times. The scalar shift charge and its spatial current still oscillate.

In that vacuum limit the action-derived shift-current perturbations are \(\delta\mathcal J^0=4\mathcal K_2\gamma=p_\chi\) and \(\delta\mathcal J^i=2\partial_i[bE-b(1+\lambda_s)\chi]\). They obey \(\partial_t\delta\mathcal J^0+\partial_i\delta\mathcal J^i=0\). This shift current is distinct from stress-energy momentum. Its oscillation is not a gravitational pressure response.

## 6. Reproduction and remaining scope

Run `python3 response.py --output results.json`. The script records symbolic identities, five vacuum wave numbers, fifteen expanding preparations, independent formulations, numerical tolerance controls, amplitude scaling and a fixed-time small-density limit. [results.json](results.json) contains the machine-readable values.

The evolving field amplitudes remain in linear perturbation theory. The calculation contains no numerical damping term, filtering, collision operator or claimed thermal state. Its next quantitative use is to bound the error of a specified restricted preparation or to retain the extra response variables in a later solver.
