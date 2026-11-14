# Two probes of behavior stored in correlations

Run `python3 correlation_probe.py` from this directory, or use its absolute path. Python 3 and NumPy are required. The verified run used Python 3.14.6 and NumPy 2.5.4. It writes `results.json` beside the script and records interpreter and NumPy versions.

Run `python3 correlation_probe.py --check` to recalculate and compare with the saved result without writing files. The comparison permits numerical differences below 1e-12 and ignores interpreter/version metadata so that other machines can reproduce it.

The first probe compares a system qubit entangled with five repeated environment records to the same system qubit entangled with the two logical states of the standard [[5,1,3]] quantum code. Both reduced system states are I/2. More strongly, controlled preparation of either orthogonal branch pair gives the same complete dephasing channel for arbitrary input amplitudes. All individual environmental qubits also have state I/2 in both constructions.

For each of the 32 environment fragments in each construction, the script calculates total mutual information with the system, the Holevo information for the system's Z label, and the trace distance of the two conditional fragment states. The conditional states commute in this example, so the Holevo quantity is achievable classical information here. In general it is only an upper bound. The code state hides all information from every fragment of size one or two. Its information is accessible in joint correlations of three or more environment qubits. Repeated records reveal the classical label in every individual environment qubit.

The code is constructed with stabilizers XZZXI, IXZZX, XIXZZ and ZXIXZ. An independent Pauli-operator check verifies that all nontrivial operators of weight one or two have zero matrix elements within the code space. The script verifies all fragment results against the analytic expectations, checks code normalization and stabilizers, and checks the system's dephasing for additional unequal input amplitudes and phases.

The second probe compares symmetric, antisymmetric and incoherent one-excitation states of two atoms. Their individual atom states are identical. For a two-emitter decay matrix with diagonal Γ and off-diagonal ηΓ, the initial photon emission rates are Γ(1+η), Γ(1−η) and Γ. Values 0 ≤ η ≤ 1 interpolate from independent channels to ideal collective coupling. Every numerical rate is checked against the analytic value.

These are finite-dimensional illustrations of known quantum mechanics. No natural environment is simulated, no new code is claimed, and no physical observation is reported. Exact darkness requires ideal shared coupling and no additional loss channels.

Identical reduced system states do not mean identical joint states. Global phase information remains in system-environment correlations in both constructions. Neither calculation establishes a unique measurement outcome.

Primary sources and their claim limits are recorded in the route's source ledger. The five-qubit code is due to Laflamme, Miquel, Paz and Zurek (1996), with related foundational error-correction work by Knill and Laflamme. Collective emission follows Dicke (1954). The present juxtaposition is an explanatory probe for Foundation0's exploration.
