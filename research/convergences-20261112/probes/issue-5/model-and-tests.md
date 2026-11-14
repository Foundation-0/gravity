# Model and test specification for issue #5

Prepared by gpt-forge with gpt-6-astra, requested reasoning effort ultra, 12 November 2026. This is a research specification and a set of analytic checks. No AeST collapse has been simulated.

**The reference action and what remains unspecified**

Use signature (−,+,+,+). Write the unit timelike vector as A throughout this note. The original AeST action is

\[
S=\frac{1}{16\pi\widetilde G}\int d^4x\sqrt{-g}\left[
R-2\Lambda-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu}
+(2-K_B)(2J^\mu\nabla_\mu\phi-\mathcal Y)
-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^\mu A_\mu+1)\right]+S_m[g],
\]

\[
F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]},\quad
J^\mu=A^\nu\nabla_\nu A^\mu,\quad
q^{\mu\nu}=g^{\mu\nu}+A^\mu A^\nu,
\quad\mathcal Q=A^\mu\nabla_\mu\phi,\quad
\mathcal Y=q^{\mu\nu}\nabla_\mu\phi\nabla_\nu\phi.
\]

The Hamiltonian paper gives the full canonical system and constraint algebra for this action: equations 1–4, sections IV–V and table 1. It has six physical degrees of freedom. Its section VII treats added higher derivatives as extensions requiring further analysis. [Bataki, Skordis and Zlosnik](https://arxiv.org/html/2307.15126v3).

Selecting only the homogeneous expansion of \(\mathcal K(\mathcal Q)=-\mathcal F(0,\mathcal Q)/2\) does not specify \(\mathcal F\) away from \(\mathcal Y=0\). A collapse model needs the full function, all constants, the matter sector and boundary/initial data. It also needs a precise reduction of the metric and vector equations, rather than an assumed scalar equation with a Poisson source attached.

For the original action the scalar equation is \(\nabla_\mu P^\mu=0\), where

\[
P^\mu=2(2-K_B)J^\mu
-2[(2-K_B)+\mathcal F_{\mathcal Y}]q^{\mu\nu}\nabla_\nu\phi
-\mathcal F_{\mathcal Q}A^\mu.
\]

The persistence route derives this directly. Adding a second-derivative operator changes the current and the stress tensor. The new current generally includes a term of the form \(-\nabla_\nu[\partial L/\partial(\nabla_\mu\nabla_\nu\phi)]\). Charge conservation supplies a balance equation, not an entropy law.

**A minimal linear obstruction to a two-variable closure**

The following is our algebraic consequence of the published linear equations, not a nonlinear result. In Newtonian gauge define

\[
B=(8\pi\widetilde G a^2\bar\rho)^{-1},\quad
A_f=\frac{1+w}{\bar{\mathcal Q}c_{\rm ad}^2},\quad
Z=K_BE+(2-K_B)\chi.
\]

For one nonzero Fourier mode, equations 7–11 give

\[
\delta=A_f\gamma-Bk^2Z,\quad
\theta=\varphi/\bar{\mathcal Q},\quad
\Pi=c_{\rm ad}^2\delta+c_{\rm ad}^2Bk^2Z,
\]

where \(\gamma=\dot\varphi-\bar{\mathcal Q}\Psi\), \(E=\dot\alpha+\Psi\), and \(\chi=\varphi+\bar{\mathcal Q}\alpha\). Equation 12 evolves E. [Skordis and Zlosnik](https://arxiv.org/html/2007.00082v3).

Consider a difference between two initial states:

\[
\Delta\varphi=\Delta\alpha=\Delta\Phi=\Delta\Psi
=\Delta\dot\Phi=0,\qquad
\Delta E=\epsilon,\qquad
\Delta\gamma=\frac{Bk^2K_B}{A_f}\epsilon.
\]

Then

\[
\Delta\delta=\Delta\theta=0,\qquad
\Delta\Pi=c_{\rm ad}^2Bk^2K_B\epsilon,
\]

\[
\Delta\dot\theta=\frac{\Delta\Pi}{1+w},\qquad
\Delta\dot\delta=-3H\Delta\Pi.
\]

All other matter data are held fixed. The linear Einstein density and momentum constraints see the same initial sources. The vector norm fixes the same temporal perturbation. The difference is a compensated choice of scalar and vector velocities. It produces different immediate accelerations despite equal density and velocity variables.

This construction assumes a regular branch with finite nonzero \(\bar{\mathcal Q}\), \(c_{\rm ad}^2\), \(K_B\), positive background density and \(1+w\ne0\). Take ε small enough for linear theory. The exactly dustlike limit needs a different set of nonsingular variables. Restricting initial states to a particular adiabatic mode can remove this freedom. The calculation does not refute such a restricted approximation.

The symbolic probe verifies the identities. It does not independently implement the full constraint algebra. The next implementation should map these data into its canonical variables, solve every constraint and confirm they represent distinct physical states. This is a small, decisive validation task.

Independent checks by the hidden-dynamics and robustness agents also recover \(\Delta\dot\theta=\Delta\gamma/\bar{\mathcal Q}\) directly from the definition of θ. Equation 12 determines \(\Delta\dot E=-H\epsilon-(2-K_B)\bar{\mathcal Q}\Delta\Pi/[K_B(1+w)]\). It supplies evolution rather than an immediate condition setting ε to zero.

At H=0 the immediate density derivative difference vanishes, while the velocity derivative difference remains. For fixed ε, the effect decreases with \(c_{\rm ad}^2\), so this witness does not disprove an accurate dust approximation. Include conjugate Fourier amplitudes when constructing real fields.

The canonical map must also update any auxiliary fields. In the Hamiltonian paper's section V.4, equations 62–63 determine μ and ν through \(\mathcal Y+\mathcal U_\mu=0\) and \(-\mathcal Q^2+\mathcal U_\nu=0\). Changing γ changes the scalar Q perturbation, so holding those auxiliaries fixed would generally violate the map. This is a specific remaining validation step.

More generally, after gauge fixing let z be the physical linear state, Rz the retained fluid variables and U(t,t₀) the full evolution matrix. Find differences n with R(t₀)n=0. A nonzero R(t)U(t,t₀)n establishes that the retained variables alone do not predict every allowed preparation. A closure for a selected ensemble must state that selection and its approximation error.

**A caustic that the proposed spatial regularizer misses**

This benchmark belongs to a nonrelativistic ghost-condensate truncation, not to full AeST. With external potential zero, take

\[
L=M^4\left[\frac12\Sigma^2-\frac{\alpha}{2M^2}(\partial_x^2\pi)^2\right],
\qquad\Sigma=\partial_t\pi-\frac12(\partial_x\pi)^2.
\]

Variation gives

\[
\partial_t\Sigma-\partial_x(\Sigma\partial_x\pi)
+\frac{\alpha}{M^2}\partial_x^4\pi=0.
\]

For \(t<T\), substitute

\[
\pi=\frac{x^2}{2(T-t)},\quad
v=-\partial_x\pi=-\frac{x}{T-t},\quad
\Sigma=0,\quad
\partial_x^4\pi=0,\quad
\partial_x^2\pi=\frac{1}{T-t}.
\]

The equation remains satisfied while curvature diverges. Characteristics \(x=x_0(1-t/T)\) meet at T. This reproduces the perfect-caustic construction in section 3.5, equations 3.36–3.44 of [Arkani-Hamed and colleagues](https://arxiv.org/pdf/hep-ph/0507120).

The profile is local and specially symmetric. Extending it over all space gives unsuitable boundary/energy behavior for a halo. A compact or periodic perturbation is a different problem. Its use is to test whether a claimed regularizer really acts on a given singularity. Near T the derivative expansion fails. Continuing the truncated equation is not a controlled prediction of the ultraviolet theory.

**Equal stress can conceal different dynamics**

As a separate exact toy, solve free streaming \(\partial_t f+v\partial_x f=0\). Let

\[
f(x,v,0)=[1+\varepsilon\cos(kx)]f_0(v).
\]

Compare equal-weight streams at \(v=\pm\sigma\) with a zero-mean Gaussian of variance \(\sigma^2\). Initial density, mean velocity and pressure are identical at every x. Their fourth velocity moments are \(\sigma^4\) and \(3\sigma^4\).

The later density-mode amplitudes, divided by their initial amplitude, are respectively

\[
\cos(k\sigma t),\qquad \exp[-(k\sigma t)^2/2].
\]

At \(k\sigma t=\pi/2\) they are 0 and 0.291213. At π they are −1 and 0.007192. This is our exact calculation from the streaming equation. It demonstrates why a nonzero pressure moment, or even matched pressure, does not establish a thermal constitutive law. It is neither an AeST model nor a collisional-fluid comparison.

**The smallest nonlinear initial condition after the model is fixed**

Start with a periodic planar perturbation in a declared expanding background. An initial displacement \(x(q,t_i)=q-D_i\sin(kq)/k\) gives Jacobian \(1-D_i\cos(kq)\) and density proportional to its inverse. In a pressureless ballistic or Zel'dovich reference, crossing occurs when D reaches 1. This is a benchmark time for the reference approximation, not a predicted AeST crossing time.

Use the growing eigenmode of the selected full AeST model to assign scalar, vector, metric and matter perturbations. A density sine wave alone is incomplete initial data. Before collapse, verify linear growth and constraint propagation against the mode calculation. Then retain the full field stress through the nonlinear phase.

A periodic box diagnoses redistribution among modes. It cannot establish escape from the entire system. A separate localized spherical experiment with a sufficiently large exterior and measured outgoing flux is needed for retention. Compare larger outer radii and reflecting boundaries as diagnostics. Keep the evolution time shorter than boundary-return contamination when possible.

For each geometry, fix physical coefficients and increase resolution independently. Vary the filtering length within \(\Delta x\ll\ell_{\rm micro}\ll\ell\ll L\), where such a hierarchy exists. Compare physical coefficients and allowed higher operators only after resolving each model. An unresolved dispersive wavelength or appreciable power at the effective-theory cutoff makes the proposed continuation inconclusive.

Use an exact Hamiltonian balance in a stationary setting, or the appropriate expansion/work terms in FLRW. Constraint residuals, charge balance and energy balance should be reported separately. A solver can preserve charge while losing energy numerically.
