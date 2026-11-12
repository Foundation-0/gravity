# Folded homogeneous elastic tensor

This note derives the formula in `research.md` for the declared ideal spring model. It uses linear internal relaxation within one periodic cell. It does not establish nonlinear stability or historical priority.

The motif is pᵢ± = ±eᵢ, i = 1,2,3. The twelve intra-cell edges connect vertices on different axes. Bridge i joins +eᵢ to −eᵢ in the next cell along row i of L. Let

```text
C = [[0,-1,-1], [1,0,-1], [1,-1,0]]
a = √2(1-s²)/(1+s²),  t = 2s/(1+s²)
L = (a+2)I + tC,     D = aI + tC.
```

The bridge vectors are the rows of D, whose length is √2 because a² + 2t² = 2. The original octahedron edges have the same length. All spring rest lengths equal √2 and the reference configuration has zero tension.

**Rank of the compatibility matrix.**

The octahedron edges give rank 12. Their kernel consists of its three translations and three rotations. Under a rotation vector ω, the relative displacement across bridge i at zero wavevector is −2ω × eᵢ. Its extension is proportional to t ω·(eᵢ × Cᵢ).

The three row vectors eᵢ × Cᵢ are (0,1,−1), (−1,0,−1) and (1,1,0). They have rank two, their only left dependence being row 1 minus row 2 minus row 3. Thus the full 15-by-18 compatibility matrix has rank 14 whenever t > 0, and its self-stress space has dimension one. At t = 0 its rank is 12.

**An explicit equilibrium tension vector.**

Set the three bridge tensions to (1,−1,−1). In the vertex ordering (+x,−x,+y,−y,+z,−z), the intra-cell tensions are:

| Edges | Tension |
|---|---|
| (+x,+y), (+x,+z), (−x,−y), (−x,−z) | a/4 + t/2 |
| (+x,−y), (+x,−z), (−x,+y), (−x,+z) | a/4 − t/2 |
| (+y,+z), (−y,−z) | −3a/4 − t/2 |
| (+y,−z), (−y,+z) | −3a/4 + t/2 |

Substitution at each vertex gives zero resultant force. The squared Euclidean norm of all fifteen tensions is N = (11a² + 12t² + 12)/4. This tension vector spans ker Rᵀ when t > 0.

**Projection onto the self-stress.**

For homogeneous symmetric strain E and internal displacement u, the linear extensions are Ru + BE. Minimising their squared norm projects BE onto ker Rᵀ. Consequently the relaxed energy per cell volume V is

```text
W(E) = (wᵀ BE)² / (2 N V).
```

Force balance cancels motif-position terms in wᵀBE. Only the three bridge translations remain. Their contribution is M:E, with

```text
T = diag(1,-1,-1)
M = Dᵀ T L / √2.
```

TC is symmetric, so M is symmetric. In the orthonormal strain basis (xx,yy,zz,√2 yz,√2 xz,√2 xy), this gives K = mmᵀ/(NV), with m = mandel(M). This is the formula independently checked against the full compatibility matrix in `probe.py`.

M is nonzero throughout the path. More strongly, its inertia is one positive and two negative eigenvalues. Its determinant cannot vanish: for x ≥ 0,

```text
det(xI + tC) = (x+t)(x² - xt + 2t²).
```

For D, x = a and (a,t) never equals (0,0). For L, x = a+2 > 0. Both determinants are positive. Since det T = 1, det M is positive. At s = 0, M = (2+√2)T. Continuity then preserves its inertia. This excludes interpreting the single supported stress as isotropic positive pressure.

**The two ideal limits.**

Let L₀ = 2+√2 and v = (1,−1,−1,0,0,0). Substituting a → √2 and t → 0 into the folded formula gives

```text
Kfold-limit = 2 vvᵀ / (17 L₀).
```

Evaluating the open geometry before discarding its other two self-stresses gives a different tensor: its 3-by-3 normal block is (3I+J)/(9L₀), where J has every entry equal to one, and its remaining entries vanish. This is the source project's open-state tensor in the rescaled coordinates used here.

**What the positive weak-spring control proves.**

The added twenty-one springs contribute η/2 times a nonnegative quadratic extension energy, with all rest lengths reset at the selected reference state. For fixed s, the minimum energy converges to the original minimum as η decreases to zero. The lower bound is the original minimum. Evaluating the completed energy on any original minimiser supplies an upper bound differing by a finite quantity times η.

At s = 0, three selected added edges constrain all three original rotations. Number the motif vertices 0 through 5 in the order above. The edges (0,1,[0,1,1]), (0,2,[1,0,0]) and (0,3,[0,1,1]) have rotation rows proportional to (0,2,−2), (0,0,−1) and (−1,1,−1). Their integer determinant is 2. Normalising the bond directions changes no rank.

Thus every η > 0 gives internal rank 15 at s = 0, leaving only translations. This rank and the relaxed tensor remain continuous in a neighbourhood of s = 0. Taking s to zero first, and then η, gives the open tensor. Reversing the limits gives the folded limiting tensor.

The distinct analytic limits, supported by the two numerical paths in `evidence.json`, establish noncommutation for this completion. The crossover values are model dependent. They are not a prediction for a particular hinge, bond-bending interaction or compound.
