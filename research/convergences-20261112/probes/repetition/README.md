This probe separates a geometric fold from the choice of interactions on it. It reads no source repository and uses the Python standard library.

Run from the repository root:

```sh
python3 research/convergences-20261112/probes/repetition/graph_vs_geometry.py
```

The script writes `graph-results.json` beside itself. It checks the six-point cab-to-fcc curve supplied by `aska-digital/incentre-lattice`, commit `db3b51d0f31e04ea3c0ffafb553f70fcdfc617ec`, in `results/fold-continuous-fcc/PROOF.md`.

The contact graph has degree five throughout 0 < s < 1. At s = 1 it gains contacts and becomes degree twelve. Exact integer-pair arithmetic checks every nearby distance polynomial. The source's analytic singular-value bound excludes all more distant periodic images. A curve with a changed bridge is rejected, and near-cancelling exact signs are checked.

The original degree-five interaction graph is unchanged at the endpoint. Fixed scalar Ising couplings on those bars therefore give the same partition function throughout the fold. Coupling every fcc contact gives a different model, already visible in high-temperature coefficients.

This conditional identity does not describe physical CaB6 without a microscopic interaction law. Distance-dependent couplings, angular interactions, vector elasticity and geometrically defined measurements can change along the fold. No critical temperature or percolation threshold was estimated.

The source manuscript used for the literature check is available from the public NSF repository:

https://par.nsf.gov/servlets/purl/10230398

Section 7 documents prior bridged cross-polytope frameworks with a different bar-to-edge ratio. It is not the source of the particular equal-bar fcc curve used in this probe.
