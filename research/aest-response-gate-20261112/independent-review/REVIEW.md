# Independent scalar-action review

No blocking error was found in the submitted AeST scalar constraint and response calculation. A separate ADM reduction, with lapse and shift retained in spatially flat gauge, reproduces the two physical scalar coordinates and their positive kinetic Hessian. Its integrated Newtonian observables agree with the submitted equations to 1.06e-12 normalized error over three wave numbers.

Reviewer: gpt-forge, separate gpt-6-astra agent. This is an independent implementation within the same project and model family, not outside peer review. Reviewed script SHA256: `e28c8f4ada1e41924e6317f8932de4d065307516cd57c5ff83a0cf23b72397ef`. Reviewed derivation SHA256: `5700296d3d35b09b6101f8695dd57abfc86863a3287f9f050beb2828513a93fe`.

## Independent construction

Use the source [AeST action](https://arxiv.org/html/2307.15126v3), normalized by multiplying by 16 pi G, with the submitted constants. In spatially flat gauge set `h_ij=a^2 delta_ij`, lapse `N=1+n`, shift `N_i=partial_i beta`, and normalized aether spatial component `A_i=partial_i alpha`.

The quadratic action, after spatial integration of one real Fourier component, is

```text
L = -6*a^3*H^2*n^2 + 4*a*k^2*H*n*beta
  + a^3*K''*(vdot-Q*n)^2
  + a*k^2*[K_B*(alphadot+n)^2
           + 2*b*(alphadot+n)*(v+Q*alpha)
           - b*(1+lambda_s)*(v+Q*alpha)^2
           + K'*(2*alpha*v+Q*alpha^2) - 2*K'*beta*v].
```

The shift equation is `2H*n-K'*v=0`. It fixes the lapse without eliminating a field velocity. Substitution gives the velocity Hessian `diag(8a^3,2ak^2)` for the selected constants. Both entries are positive for a>0 and k>0. The two remaining field coordinates have four phase-space data. No scalar mode has been discarded by imposing a density closure.

The script derives Euler-Lagrange equations from this reduced action rather than importing the submitted evolution. The submitted module is used only for the final comparison. The Newtonian metric is reconstructed by the density constraint after changing gauge.

Comparison covers density, momentum, both response variables, pressure, the potential and the original scalar/vector coordinates at k/Q0=6,12,24, from a=1 to a=2.

A separate direct expansion of the Newtonian-gauge ADM extrinsic-curvature term verifies the submitted `-12a^3 H(Phi+Psi) Phidot` term. Thus its canonical momentum convention is consistent without an unreported integration by parts. [adm_check.py](adm_check.py) records these checks and [adm-evidence.json](adm-evidence.json) records the exact submitted hashes and residuals.

The spatial-gradient and aether terms were checked from the normalized vector. In particular, the constant nonzero Y slope supplies the extra lambda_s contribution. Using the original cosmological zero-slope vector equation without that term would describe a different action.

## Physical and numerical interpretation

The compensated data change gauge-invariant E and/or chi while preserving initial retained density and momentum. The reported pressure response therefore has a physical scalar preparation behind it. The vacuum limit and the finite-density continuation are distinct. Their contrast is consistent with the vanishing linear vacuum stress response, rather than evidence for an extra mode absent from the established theory.

The [published cosmological equations](https://arxiv.org/html/2007.00082v3) already state that pressure depends on additional aether variables. The submitted work supplies a bounded preparation map and executable response. It does not establish a new general failure of a fluid description or of AeST cosmology.

The dust-inspired density preparation has chi=Z=0 and is not a verified growing slow mode. At the chosen finite sound speed and short wavelengths, large closure errors can arise from ordinary pressure and excitation of the fast scalar. The README retains this limit and makes no observational-failure claim. Its 35-preparation test should be read as a test of those specified preparations and normalizations.

The useful next test is the same action and background with an explicitly selected slow-mode preparation. The fast and slow spectral subspaces must remain separated during the interval. An instantaneous eigenvector is an initial condition, not an exact time-dependent invariant mode. Controlled fast-mode contamination would show how accurately that preparation must be made for a two-variable approximation to work.

No global nonlinear stability, ultraviolet validity, thermalization or observational accuracy was reviewed. The positive kinetic Hessian and short-wavelength scalar sign do not exclude slow gravitational growth.

## Reproduce

Run `python3 adm_check.py` from this directory. It verifies the frozen source hashes and requires NumPy, SciPy and SymPy. It reads the adjacent `public-checkpoint/` when present, or the parent directory in a published bundle.
