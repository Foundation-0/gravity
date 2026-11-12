# Hidden dynamics probes

Run `python3 hidden_dynamics.py` from this directory, or run the script by its absolute path. It uses only the Python standard library and rewrites `results.json` and `trajectories.csv` beside the script.

The examples cover exact linear elimination, deterministic state insufficiency, a controlled instantaneous approximation, a stationary Gaussian memory witness, frequency-dependent response and the two-swap quantum example from Pollock et al., arXiv:1801.09811, Appendix B.3.

The deterministic equations are `x'=-x+y`, `y'=-gamma*(x+y)`. The exact scalar memory equation is integrated independently using trapezoidal convolution and compared with the analytic solution and a Runge-Kutta integration of the full equations. Step-halving checks verify the numerical order.

The stochastic example adds independent Wiener driving with amplitude `sqrt(2)` to the two equations at `gamma=1`. It starts in the stationary Gaussian state with covariance equal to the identity. The script computes its exact covariance and conditional covariance analytically. It does not simulate sample paths or infer a process from finite data. Sampling and measurement noise are absent.

The quantum example uses ideal two-qubit swap matrices, a pure environment initially independent of the system, and a system-only reset between swaps. Initial system states are zero, one and plus. The joint state is a product at the sampled steps. The example makes no claim about correlations during a continuous physical gate implementation.

All examples are synthetic. They contain no astronomical observations, no MOND law and no AeST evolution. The coupled-spring derivation in the report is elementary analytic work and is not separately simulated by this script.
