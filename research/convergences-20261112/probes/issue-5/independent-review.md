**Independent review of the issue #5 research pass**

Prepared by gpt-forge, robustness route, using the requested gpt-6-astra configuration with ultra reasoning effort, 12 November 2026. This is a focused independent check of the mathematical examples and physical bridge. It is not a nonlinear AeST simulation or approval of a particular higher-derivative completion.

The checked claims support a useful next experiment: determine whether collapse transfers energy into persistent local stress, then test whether that stress predicts later response. The reviewed report preserves the distinction between such a result and a thermal entropy floor. I found no outstanding algebraic correction in the checked examples.

**What was independently checked**

1. **Perfect caustic.** I read section 3.5 and equations 3.36–3.44 of [Arkani-Hamed and colleagues](https://arxiv.org/pdf/hep-ph/0507120), then independently varied the stated reduced Lagrangian before substituting the proposed profile. For \(\tau=T-t>0\),

   \[
   \pi=x^2/(2\tau),\quad
   \Sigma=\dot\pi-(\partial_x\pi)^2/2=0,\quad
   \partial_x^4\pi=0,\quad
   \partial_x^2\pi=1/\tau.
   \]

   The Euler–Lagrange residual and the corresponding inviscid Burgers residual vanish. The gradient term's energy density grows as \(\tau^{-2}\), even though its interior restoring term vanishes. Energetic cost alone therefore does not guarantee regularization.

   This is a local, specially symmetric solution of the specified ghost-condensate truncation. Its global boundaries and the eventual loss of derivative control prevent treating it as an AeST halo or a theorem against every completion. The report states those limits correctly.

2. **Compensated linear AeST pair.** I checked the definitions and signs against [Skordis and Zlosnik, equations 7–12](https://arxiv.org/html/2007.00082v3). Independently differentiating the observable map in variables \((\gamma,E,\varphi,\alpha)\), the proposed direction

   \[
   n=\left(\frac{Bk^2K_B\bar{\mathcal Q}c_{\rm ad}^2}{1+w},1,0,0\right)
   \]

   obeys \(D(\delta,\theta)n=0\), while \(D\Pi\,n=Bc_{\rm ad}^2K_Bk^2\). The kinematic derivative \(\Delta\dot\varphi/\bar{\mathcal Q}\) also equals the acceleration difference inferred from equation 10.

   Equal density and momentum sources preserve the stated initial Einstein constraints. The source says the shear equation retains its GR form. A solver-specific canonical constraint check remains necessary. Singular dust limits and restricted initial ensembles cannot be inferred from this regular-branch construction.

   I checked the added equation-12 expression for \(\Delta\dot E\) against the source. It supplies evolution rather than setting the initial difference to zero. The effect scales with \(c_{\rm ad}^2\) at fixed difference amplitude, so this witness does not exclude an accurate dust approximation.

3. **Equal-moment streaming control.** Starting from \(f(x,v,t)=f(x-vt,v,0)\), I independently evaluated the Gaussian Fourier integral. The density response is \(e^{-(k\sigma t)^2/2}\), whereas equal streams at \(\pm\sigma\) give \(\cos(k\sigma t)\). Their initial zeroth, first and second moments agree.

   This exact example supports the report's limited conclusion: matching stress at one time does not establish a predictive thermal closure. No gravitational or collisional behavior follows from this toy.

4. **Positive laboratory precedent.** I read sections I.1–I.3, the discussion and methods of [Mossman and colleagues](https://arxiv.org/html/1712.06689). The evidence supports a driven three-dimensional condensate developing transverse instability, vortex structure and coarse shock behavior consistent with effective dissipation.

   Parameter-free agreement refers to the GP simulation. The viscous comparison fits an effective sound speed and, for the filtered profile, a filtering scale, shock width and upstream mean flow. Eddy viscosity is an interpretation, not a derived thermodynamic entropy law.

   The piston supplies continued driving and the trap confines the system. The paper does not demonstrate undriven halo retention. Strict planar or spherical symmetry excludes its transverse route. AeST's different fields do not inherit condensate vortices by analogy. These qualifications are present in the reviewed final report.

The symbolic work above was performed in a separate one-off SymPy calculation. I did not import or rerun the author's script, which writes its own results file. The independent outputs were zero caustic residual, zero observable-map residual, pressure difference \(Bc_{\rm ad}^2K_Bk^2\), and the Gaussian response above.

**A useful physical discriminator**

An independent work-balance check sharpens the interpretation of the BEC bridge. For GP evolution with a time-dependent external potential and vanishing boundary flux,

\[
E=\int\left[\frac{\hbar^2}{2m}|\nabla\psi|^2+V|\psi|^2
+\frac{g}{2}|\psi|^4\right]d^3x,
\qquad
\frac{dE}{dt}=\int |\psi|^2\partial_tV\,d^3x.
\]

This follows by differentiating the Hamiltonian and substituting the conservative field equation. A conservative generator with a moving piston need not conserve the field's instantaneous energy. The corresponding AeST balance must be derived from its own action and approximation, with flux and expansion or external work included.

For the proposed collapse test, use a finite episode of infall and measure what remains after coherent forcing subsides. Separate the following outcomes with measured flux, stress and response:

- Local stress persists, while outgoing wave energy is small enough for continued support.
- Stress follows active compression and decays once that supply ends.
- Energy remains locally but produces coherent oscillations, anisotropic stress or preparation-dependent response.
- Apparent retention changes with boundaries, filtering or unresolved physical wavelengths.

The third outcome would still be useful physics. It calls for additional state variables rather than immediate rejection or a thermal interpretation. A perturbation applied after collapse can measure the stress response. A later transverse-mode test should begin with the selected AeST extension's actual mode spectrum. The condensate example motivates that test without specifying its answer.

**Scope and provenance**

I read the completed [issue report](../../reports/issue-5.md), its [technical specification](model-and-tests.md) and [check script](issue5_checks.py).

Recommendations about fitting, dimensionality, continuing driving and field content were sent to the author and are incorporated in the reviewed report. No peer artifact was edited. I rechecked the final additions concerning equation 12 and suppression at small sound speed.

Reviewed SHA-256 snapshots, in the same order:

```text
780ce13da10123bb0c1433a255a91c4ec40c6871c16c297a34a5e6d328010d57
907347f115bc998eebdb2572fcc1a33807e2235a4846897e39f02487ee1c2a1e
0153b487a59138251824e66358f729282771937a5d069ccae1360213a70a0cae
```

Uncomputed in this review: the complete AeST canonical constraint map, a healthy specified scordatura extension, its cutoff and nonlinear characteristics, actual transverse instabilities, collapse evolution, stress lifetime, entropy production, and any cosmological selection of a 185 km/s scale. The review verifies the proposed discriminators and their mathematical examples, not those physical outcomes.
