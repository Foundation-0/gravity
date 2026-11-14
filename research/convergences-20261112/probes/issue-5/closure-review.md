# Independent review of the compensated AeST initial pair

**Verdict: valid conditional algebraic witness. No correction to the proposed signs or factors is needed.** The construction is consistent with the definitions and evolution equations displayed in the original AeST paper. It preserves the stated linear Einstein initial sources and vector normalization. It has not been mapped through every canonical constraint, so it should retain that qualification.

Reviewed by gpt-forge, gpt-6-astra with requested ultra reasoning, 12 November 2026. Sources were independently reopened. This review concerns the original action's linear scalar perturbations around FLRW, not the proposed higher-derivative extension or nonlinear collapse.

Write \(Q=\dot{\bar\phi}\), \(c=c_{\rm ad}^{2}\), \(B=(8\pi\widetilde G a^2\bar\rho)^{-1}\), and \(A_f=(1+w)/(Qc)\). For a comoving Fourier mode, \(\nabla^2\rightarrow-k^2\). Equations 7–11 then give

\[
Z=K_BE+(2-K_B)\chi,\quad
\delta=A_f\gamma-Bk^2Z,\quad
\theta=\varphi/Q,\quad
\Pi=c\delta+cBk^2Z.
\]

At one initial time, keep the background, other matter data, \(\varphi,\alpha,\Phi,\Psi,\dot\Phi\) fixed. Set

\[
\Delta E=\epsilon,\qquad
\Delta\gamma=\frac{Bk^2K_B}{A_f}\epsilon.
\]

Because \(\Delta\chi=0\), direct substitution gives

\[
\Delta\delta=\Delta\theta=0,\qquad
\Delta\Pi=cBk^2K_B\epsilon,
\]

\[
\Delta\dot\theta=\frac{\Delta\Pi}{1+w},\qquad
\Delta\dot\delta=-3H\Delta\Pi.
\]

The factor \(a^{-2}\) is already in \(B\). Adding another to these expressions would be incorrect. The changes represent compensated scalar and vector velocities: \(\Delta\dot\varphi=\Delta\gamma\) and \(\Delta\dot\alpha=\epsilon\).

An independent consistency check comes from combining equations 7 and 11:

\[
\Pi=\frac{1+w}{Q}\gamma.
\]

Direct differentiation of \(\theta=\varphi/Q\), using identical initial \(\varphi\), gives \(\Delta\dot\theta=\Delta\gamma/Q\). This agrees with equation 10. The published background relation \(\dot Q/Q=-3Hc\) also makes the full definitions consistent with that equation.

Equation 12 supplies an evolution equation, not an additional instantaneous restriction on \(\epsilon\):

\[
\Delta\dot E=-H\epsilon
-\frac{(2-K_B)Q}{K_B(1+w)}\Delta\Pi.
\]

These results follow from the [original AeST paper, equations 7–12 and the preceding background equations](https://arxiv.org/html/2007.00082v3). Independently evaluated SymPy residuals were zero for the density cancellation, pressure formula, direct versus evolution-equation value of \(\Delta\dot\theta\), scalar-velocity pressure relation, and vector equation 12.

The displayed initial constraints support the construction:

- The linear Einstein density and momentum sources are unchanged because \(\delta,\theta\) and all other matter data match. Fixing \(\Phi,\Psi,\dot\Phi\) also fixes their geometric sides in Newtonian gauge.
- The paper's shear equation has the GR form. Matching the other species' anisotropic stress and metric potentials preserves it initially. Different isotropic pressure can change later metric derivatives without violating an initial constraint.
- The vector has \(A_\mu=(-1-\Psi,\partial_i\alpha)\) at first order. Its normalization fixes the same temporal component. Around a background with \(A_i=0\), that normalization imposes no additional linear restriction on the changed longitudinal velocity \(\dot\alpha\).

The remaining canonical check is specific. The Hamiltonian formulation introduces auxiliary fields \(\mu,\nu\), whose constraints include \(\mathcal Y+\mathcal U_\mu=0\) and \(-\mathcal Q^2+\mathcal U_\nu=0\). The compensated scalar velocity changes the perturbation of \(\mathcal Q\).

An implementation must solve for the corresponding auxiliary values and canonical momenta, not hold all auxiliaries fixed.

On the generic regular branch these conditions determine auxiliaries, but this review does not certify the full map or exceptional branches. [Hamiltonian paper, section V.4, equations 62–75](https://arxiv.org/html/2307.15126v3).

The witness requires nonzero \(k\), finite nonzero \(Q,c,K_B\), positive finite background density, \(1+w\neq0\), and a sufficiently small perturbation.

For a real field, include the conjugate Fourier mode. The exactly dustlike or other singular limits require different variables.

With fixed \(\epsilon\), the effect is suppressed as \(c\) becomes small, so this does not disprove an accurate dust approximation. If \(H=0\), \(\Delta\dot\delta=0\) initially while \(\Delta\dot\theta\) can remain nonzero.

A restriction to the particular adiabatic initial family used in a cosmological calculation can remove this freedom. The conclusion therefore concerns a proposed universal two-variable closure across the allowed preparations, not every restricted effective model.

It establishes no memory timescale, entropy law, thermal pressure, stability threshold or nonlinear result. Added scordatura operators require their own equations and constraint review.

Recommended wording: **The published linear equations admit this compensated algebraic pair with identical initial effective density and velocity but different retained derivatives. The complete canonical initial-data map remains to be checked.**
