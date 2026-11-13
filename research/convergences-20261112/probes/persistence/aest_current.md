# What AeST shift symmetry conserves

This is a direct variation of the action in Bataki, Skordis and Zlosnik, [Aether scalar tensor theory: Hamiltonian Formalism](https://arxiv.org/html/2307.15126v3), equations 1–4. It is not a nonlinear collapse solution or a derivation of a dark-fluid entropy equation.

Use signature (−,+,+,+), a unit timelike vector A, its acceleration J^μ = A^ν∇_ν A^μ, and q^μν = g^μν + A^μA^ν. Set Q = A^μ∇_μ φ and Y = q^μν∇_μ φ∇_ν φ. The scalar-dependent terms inside the action's common prefactor are

```
L_phi = (2-K_B)(2 J^mu partial_mu phi - Y) - F(Y,Q).
```

There is no undifferentiated φ. Varying φ while holding the metric and vector fixed gives

```
P^mu = partial L_phi / partial(partial_mu phi)
     = 2(2-K_B) J^mu
       - 2[(2-K_B) + F_Y] q^(mu nu) partial_nu phi
       - F_Q A^mu

nabla_mu P^mu = 0.
```

The common constant 1/(16π G_tilde) can be restored in P. The overall sign of the defined current is conventional. The expressions follow from δY = 2q^μν∇_νφ ∇_μδφ and δQ = A^μ∇_μδφ, followed by integration by parts.

On a homogeneous FLRW background with proper time, A^μ = (1,0,0,0), J^μ = 0 and q^μν∇_νφ = 0. Defining K(Q) = −F(0,Q)/2 gives P^0 = 2K_Q. Therefore

```
partial_t(a^3 K_Q) = 0
K_Q = I0 / a^3.
```

This agrees with the first paragraph of Cosmological observables in [Skordis and Zlosnik's original AeST paper](https://arxiv.org/html/2007.00082v3). The homogeneous dustlike component inherits an integration constant. The shift symmetry does not predict its value.

For a fixed coordinate volume in a general background,

```
partial_t integral_V sqrt(-g) P^0 d^3x
  = - integral_boundary(V) sqrt(-g) P^i dS_i.
```

A conserved total charge can leave a chosen region. Charge conservation is also a different statement from energy retention. Neither equation provides a thermodynamic entropy, a heat conductivity, an irreversible shock law or a local equation of state after shell crossing.

The vector and metric have their own equations and constraints. A numerical test must choose F(Y,Q), parameters and initial data, retain the relevant fields, and track the energy carried by permitted perturbations across a specified boundary. A higher-derivative completion changes the variational current and must be included explicitly.

The Schrödinger-Poisson counterexample in the main report does not supply those missing equations. It only invalidates a universal inference from a single-valued wave field to absent multistream phase-space behavior.
