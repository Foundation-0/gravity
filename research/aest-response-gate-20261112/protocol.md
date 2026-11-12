# AeST scalar constraints and response: a fixed benchmark

This calculation tests whether two AeST field preparations with the same initial effective gravitational sources are distinct physical states. It starts from a published AeST action and sets the checks for its linear constraints. The first benchmark is Minkowski vacuum, so it cannot establish a cosmological fluid closure or a collapse outcome.

Prepared 12 November 2026 by gpt-forge using the requested gpt-6-astra research model. Status: protocol fixed; derivation and response checks in progress; not yet independently reviewed. The companion derivation and executable results will record which gates pass.

## Action, background and units

Use signature \((-+++ )\), \(c=1\), and the action

\[
S=\frac{1}{16\pi\widetilde G}\int d^4x\sqrt{-g}
\{R-\tfrac12 K_B F_{\mu\nu}F^{\mu\nu}
+(2-K_B)(2J^\mu\nabla_\mu\phi-\mathcal Y)
-\mathcal F(\mathcal Y,\mathcal Q)-\lambda(A^\mu A_\mu+1)\}.
\]

Here \(F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}\), \(J^\mu=A^\nu\nabla_\nu A^\mu\), \(\mathcal Q=A^\mu\nabla_\mu\phi\), and \(\mathcal Y=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\phi\nabla_\nu\phi\). There is no matter source or cosmological constant in this benchmark.

Fix the full function to

\[
\mathcal F=(2-K_B)\lambda_s\mathcal Y-2\mathcal K_2(\mathcal Q-\mathcal Q_0)^2,
\quad K_B=1,\quad \mathcal K_2=2,\quad\lambda_s=1,\quad\mathcal Q_0>0.
\]

This is the explicit function in equation 84 of [Bataki, Skordis and Zlosnik](https://arxiv.org/html/2307.15126v3). It is a classical tracking benchmark. It is not a complete interpolating MOND function or a fit to the observed cosmology. No higher-derivative operator or ultraviolet completion is added.

The exact background is \(g_{\mu\nu}=\eta_{\mu\nu}\), \(A^\mu=(1,0,0,0)\), \(\phi=\mathcal Q_0 t\). The scalar is dimensionless. Thus \(\mathcal Q_0\) and physical wave number have units of inverse length, \(\mathcal F\) has units of inverse length squared, and the three selected constants are dimensionless. Numerical time is \(\mathcal Q_0t\) and numerical wave number is \(k/\mathcal Q_0\).

## Gauge and retained states

For each nonzero scalar Fourier mode use Newtonian gauge,

\[
ds^2=-(1+2\Psi)dt^2+(1-2\Phi)d\mathbf x^2,
\quad A_0=-1-\Psi,\quad A_i=\partial_i\alpha,
\quad\phi=\mathcal Q_0t+\varphi.
\]

The unit-vector constraint is imposed to first order. Define \(\chi=\varphi+\mathcal Q_0\alpha\), \(E=\dot\alpha+\Psi\), \(\gamma=\dot\varphi-\mathcal Q_0\Psi\), and \(Z=K_BE+(2-K_B)\chi\). Real fields contain conjugate Fourier amplitudes.

The primary comparison retains absolute effective density, momentum and spatial stress, defined by moving the AeST terms to the right side of Einstein's equation with the bare \(\widetilde G\). It also records both metric potentials and their lensing sum. Density contrast and fluid velocity divided by background enthalpy are excluded because that enthalpy vanishes here.

## Canonical gate

Derive the quadratic scalar action, retaining lapse and shift constraints before gauge reduction. Match its canonical momenta and constraints to equations 106–115 of the Hamiltonian source. In the normalization where the action is multiplied by \(16\pi\widetilde G\), the expected field momentum map is

\[
P_\varphi=4\mathcal K_2\gamma,
\qquad P_\alpha=2k^2 Z,
\qquad P_\alpha-\mathcal Q_0P_\varphi=4k^2\Phi.
\]

The spatial scalar shear and momentum constraint must also be imposed. Auxiliary variables, if used, must change consistently with \(\mathcal Q\). A linear function of \(\mathcal Y\) has a degenerate Legendre transform in that argument, so \(\mu=\mathcal F_{\mathcal Y}\) is fixed rather than independently varied.

Test the compensated initial difference

\[
\Delta\alpha=\Delta\varphi=\Delta\Phi=\Delta\Psi=0,
\quad\Delta E=\varepsilon,
\quad\Delta\gamma=\frac{K_B k^2}{2\mathcal K_2\mathcal Q_0}\varepsilon.
\]

This is a nonsingular absolute-density counterpart of the earlier fluid-variable construction. Verify each constraint and show whether a nonzero gauge-invariant field perturbation remains. Do not infer a stress response from physical distinctness alone.

## Response and stability gates

Use the exact reduced Hamiltonian to propagate all four physical scalar phase-space data. Check its quadratic energy signature before choosing the wave-number interval. The initial test interval is \(3\leq k/\mathcal Q_0\leq12\), subject to the explicit positivity calculation.

Compute the response for compensated velocity data, independent field-phase data and mixtures held out from any proposed reduced law. Report metric, density, momentum and spatial stress separately from the conserved scalar shift current. A conserved shift current is not the stress-energy momentum current.

Verify the published propagating dispersion relation, the nonpropagating branch, canonical constraint preservation, linear amplitude scaling and independent numerical integration against the exact propagator. Compare at least three numerical tolerances. A real obstruction or a vanishing physical response is a result.

The [original action paper](https://arxiv.org/html/2007.00082v3) already identifies the extra cosmological pressure variables. The [Minkowski stability paper](https://arxiv.org/abs/2109.13287) already derives the spectrum and reduced Hamiltonian. This work claims only a reproducible preparation and observable map built on those results.

The [2025 mimetic connection](https://arxiv.org/html/2503.11174v1) supplies alternate formulations under stated assumptions. It does not supply a regularizer for this benchmark. No three-dimensional collapse calculation begins from a successful flat-space constraint test alone.
