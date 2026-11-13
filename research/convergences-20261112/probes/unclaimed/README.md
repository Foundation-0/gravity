# Constraint probes

Run:

```sh
python3 research/convergences-20261112/probes/unclaimed/constraint_probes.py
```

Python 3 and its standard library are sufficient. The script writes `results.json` beside itself. The examples are known-model consequences, not new physical discoveries.

## Shape cycle

Three equal unit masses have zero center of mass. Their mass-weighted Jacobi vectors are `x = exp(i theta)` and `y = r exp(i(theta + phi))`. The inverse transform in the script is orthonormal, so kinetic energy and angular momentum can be evaluated in either representation.

Total angular momentum is `(1+r²) theta_dot + r² phi_dot`. Setting it to zero determines the orientation rate. The prescribed rectangle in `(r,phi)` space gives a 27-degree net turn. A quintic time parameterization gives zero shape velocity at the ends of each leg.

The calculation assumes internal actuation and does not solve Newtonian three-body attraction. The trajectory has nonzero kinetic energy during deformation. No energy-free motion or self-powered device is asserted. Changing the duration of the prescribed path leaves its geometric turn unchanged while changing kinetic energy and required forces.

Controls verify the inverse Jacobi reconstruction, center of mass, angular momentum, closing side lengths, rotation of final positions, reversed path and a retraced path. This is a kinematic calculation without a discretized dynamics solver.

## Wave snapshots

Units set hbar and particle mass to one. The states are two-dimensional and square-integrable. No potential or stationary-state condition is imposed.

The anisotropic Gaussian has a globally smooth phase `alpha*x*y` and velocity `alpha*(y,x)`. Its curl is zero, but its density-weighted angular momentum is nonzero. Its expected angular momentum per particle is `alpha*(a²-b²)/2`.

The polynomial Gaussian has zeros at `(1,0)` and `(-1,0)`. The loop windings are +1 and -1, respectively. Reflection symmetry makes the integrated angular momentum vanish. Its unnormalized density integral is `3*pi`.

The script checks the analytic normalization integrals and angular momenta by midpoint quadrature on `[-12,12]²`. It checks winding through successive complex phase increments along loops. No claim is made about the subsequent lifetime, stability or cosmological production of these snapshots.

## Force balance and driven support

The center of an equilateral arrangement of three fixed positive unit charges has potential Hessian `diag(1.5,1.5,-3)` when its circumradius is one. Source charges are treated as externally held. A positive test charge is confined by the quadratic potential only if motion is restricted to the plane.

The alternating potential is `cos(Omega*t)*(x²+y²-2*z²)/2`. Its Laplacian vanishes at every time. Each Cartesian equation is linear with a periodic coefficient. RK4 integrates two independent initial conditions over one period to produce its monodromy matrix.

For determinant one and distinct multipliers, `abs(trace)<2` gives the elliptic, bounded linear case. A multiplier outside the unit circle gives linear instability. The script verifies determinants, compares a doubled resolution, and checks a static saddle against its exact hyperbolic-cosine trace. Finite traps, noise, nonlinear terms and interactions between test particles are outside the calculation.

## Sources

The source ledger is `../../reports/unclaimed-sources.json`. Downloaded papers and rendered reading copies are omitted from this publication. The calculation script is an independent pedagogical implementation of the stated equations.
