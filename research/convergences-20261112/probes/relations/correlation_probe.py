#!/usr/bin/env python3
"""Two finite-dimensional illustrations of behavior stored in correlations.

Run: python3 correlation_probe.py
Requires numpy. Writes only beside this script. This is a mathematical probe,
not experimental data or a fit to the Foundation-0 witness map.
"""

import argparse
import itertools
import json
import platform
import sys
from pathlib import Path

import numpy as np


def ket(index, n):
    result = np.zeros(2**n, dtype=complex)
    result[index] = 1
    return result


def reduced(psi, keep, n):
    """Partial trace for a pure state, with qubit 0 the most significant bit."""
    keep = tuple(keep)
    rest = tuple(i for i in range(n) if i not in keep)
    a = psi.reshape((2,) * n).transpose(keep + rest)
    a = a.reshape(2 ** len(keep), -1)
    return a @ a.conj().T


def entropy(rho):
    eig = np.linalg.eigvalsh(rho)
    assert eig.min() > -1e-12
    eig = eig[eig > 1e-13]
    return float(-np.sum(eig * np.log2(eig)))


def pauli(word):
    matrices = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.diag([1, -1]).astype(complex),
    }
    result = np.ones((1, 1), dtype=complex)
    for char in word:
        result = np.kron(result, matrices[char])
    return result


def five_qubit_code():
    # Standard cyclic stabilizer form of the [[5,1,3]] perfect code.
    # Build |0_L> as the +1 state of all four generators and logical Z.
    words = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    gs = [pauli(w) for w in words]
    for g, h in itertools.combinations(gs, 2):
        np.testing.assert_allclose(g @ h, h @ g, atol=1e-13)
    zero = ket(0, 5)
    for g in gs:
        zero = (zero + g @ zero) / 2
    zero /= np.linalg.norm(zero)
    one = pauli("XXXXX") @ zero
    for state in (zero, one):
        for g in gs:
            np.testing.assert_allclose(g @ state, state, atol=1e-13)
    np.testing.assert_allclose(pauli("ZZZZZ") @ zero, zero, atol=1e-13)
    np.testing.assert_allclose(pauli("ZZZZZ") @ one, -one, atol=1e-13)
    np.testing.assert_allclose(np.vdot(zero, one), 0, atol=1e-13)
    # A separate check of local indistinguishability, using every nonidentity
    # Pauli on one or two positions instead of the partial-trace calculation.
    code = np.column_stack([zero, one])
    max_local_pauli = 0.0
    for word in itertools.product("IXYZ", repeat=5):
        if 1 <= sum(c != "I" for c in word) <= 2:
            matrix = code.conj().T @ pauli(word) @ code
            max_local_pauli = max(max_local_pauli, float(np.max(abs(matrix))))
    assert max_local_pauli < 1e-12
    return zero, one, words, max_local_pauli


def record_probe():
    code0, code1, stabilizers, max_local_pauli = five_qubit_code()
    branches = {
        "redundant_records": (ket(0, 5), ket(31, 5)),
        "encoded_correlations": (code0, code1),
    }
    output = {"environment_qubits": 5, "system_qubits": 1,
              "code_stabilizers": stabilizers,
              "max_code_matrix_element_of_weight_1_or_2_pauli": max_local_pauli,
              "states": {}}
    for name, (env0, env1) in branches.items():
        psi = (np.kron(ket(0, 1), env0) + np.kron(ket(1, 1), env1)) / np.sqrt(2)
        rho_s = reduced(psi, [0], 6)
        np.testing.assert_allclose(rho_s, np.eye(2) / 2, atol=1e-13)
        rows = []
        for size in range(6):
            mutual, holevo, distance = [], [], []
            for fragment in itertools.combinations(range(5), size):
                rho0 = reduced(env0, fragment, 5)
                rho1 = reduced(env1, fragment, 5)
                rho_f = (rho0 + rho1) / 2
                rho_sf = reduced(psi, [0] + [i + 1 for i in fragment], 6)
                mutual.append(entropy(rho_s) + entropy(rho_f) - entropy(rho_sf))
                holevo.append(entropy(rho_f) - (entropy(rho0) + entropy(rho1)) / 2)
                distance.append(float(np.sum(abs(np.linalg.eigvalsh(rho0 - rho1))) / 2))
                # Here the conditional states commute, so Holevo information is
                # achievable. This is not true for general quantum ensembles.
                np.testing.assert_allclose(rho0 @ rho1, rho1 @ rho0, atol=1e-13)
            expected_i = (0 if size == 0 else 2 if size == 5 else 1) if name == "redundant_records" else (0 if size <= 2 else 2)
            expected_chi = (0 if size == 0 else 1) if name == "redundant_records" else (0 if size <= 2 else 1)
            np.testing.assert_allclose(mutual, expected_i, atol=1e-12)
            np.testing.assert_allclose(holevo, expected_chi, atol=1e-12)
            np.testing.assert_allclose(distance, expected_chi, atol=1e-12)
            rows.append({"fragment_qubits": size, "fragments_checked": len(mutual),
                         "mutual_information_bits_min": round(min(mutual), 12),
                         "mutual_information_bits_max": round(max(mutual), 12),
                         "pointer_holevo_bits": round(float(np.mean(holevo)), 12),
                         "pointer_trace_distance": round(float(np.mean(distance)), 12)})
        # Both branch pairs implement the SAME full dephasing channel on S,
        # for arbitrary input alpha|0>+beta|1>, not merely for equal amplitudes.
        for p, phase in [(0.07, 0.0), (0.3, 0.8), (0.5, 2.1), (0.91, -0.4)]:
            arbitrary = np.sqrt(p) * np.kron(ket(0, 1), env0) + np.sqrt(1-p) * np.exp(1j*phase) * np.kron(ket(1, 1), env1)
            np.testing.assert_allclose(reduced(arbitrary, [0], 6), np.diag([p, 1-p]), atol=1e-13)
        output["states"][name] = {"system_density_matrix": rho_s.real.tolist(), "fragments": rows}
    return output


def emission_probe():
    # Basis |g>=|0>, |e>=|1>. Equal one-body marginals do not fix emission
    # through a shared field. gamma_12 = eta * gamma; |eta| <= 1 keeps the
    # two-emitter decay matrix positive. Units set single-emitter gamma=1.
    lower = np.array([[0, 1], [0, 0]], dtype=complex)
    lowering = [np.kron(lower, np.eye(2)), np.kron(np.eye(2), lower)]
    bright = (ket(1, 2) + ket(2, 2)) / np.sqrt(2)
    dark = (ket(1, 2) - ket(2, 2)) / np.sqrt(2)
    mixed = (np.outer(ket(1, 2), ket(1, 2)) + np.outer(ket(2, 2), ket(2, 2))) / 2
    states = {"symmetric": np.outer(bright, bright.conj()),
              "antisymmetric": np.outer(dark, dark.conj()), "incoherent_mixture": mixed}
    for state in (bright, dark):
        for particle in range(2):
            np.testing.assert_allclose(reduced(state, [particle], 2), np.eye(2)/2, atol=1e-13)
    rows = []
    for eta in [0.0, 0.25, 0.5, 0.9, 1.0]:
        rates = {}
        for name, rho in states.items():
            rate = sum((1 if i == j else eta) * np.trace(lowering[i].conj().T @ lowering[j] @ rho)
                       for i in range(2) for j in range(2))
            assert abs(rate.imag) < 1e-13
            rates[name] = float(rate.real)
        np.testing.assert_allclose([rates["symmetric"], rates["antisymmetric"], rates["incoherent_mixture"]], [1+eta, 1-eta, 1], atol=1e-13)
        rows.append({"bath_cross_correlation_eta": eta, "photon_emission_rate_over_single_atom_gamma": rates})
    return {"description": "Initial photon emission rates in the two-emitter Markov model; not measured rates.",
            "one_atom_density_matrix_for_each_pure_state": [[0.5, 0], [0, 0.5]], "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the checked-in result without writing files.")
    args = parser.parse_args()
    result = {"status": "COMPUTED_ILLUSTRATION_OF_KNOWN_QUANTUM_MECHANICS", "numpy_version": np.__version__,
              "python_version": platform.python_version(), "python_executable": "python3",
              "records": record_probe(), "emission": emission_probe(),
              "limitations": ["Endpoint states and ideal channels, not a natural-environment simulation.",
                              "All original system phase information remains in global correlations in both record examples.",
                              "Exact dark emission requires ideal collective coupling and no extra loss channels."]}
    destination = Path(__file__).with_name("results.json")
    if args.check:
        stored = json.loads(destination.read_text())
        # Interpreter metadata may differ across machines. Numerical and
        # scientific outputs must agree within the explicit tolerance below.
        def compare(actual, expected, path="result"):
            if isinstance(actual, dict):
                assert actual.keys() == expected.keys(), path
                for key in actual:
                    if key not in {"python_executable", "python_version", "numpy_version"}:
                        compare(actual[key], expected[key], path + "." + key)
            elif isinstance(actual, list):
                assert len(actual) == len(expected), path
                for index, (a, b) in enumerate(zip(actual, expected)):
                    compare(a, b, path + f"[{index}]")
            elif isinstance(actual, float):
                assert abs(actual - expected) < 1e-12, path
            else:
                assert actual == expected, path
        compare(result, stored)
    else:
        destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": "passed", "mode": "read_only_check" if args.check else "regenerate", "output": str(destination),
                      "record_fragments_per_state": 32,
                      "emission_limits": result["emission"]["rows"][-1]}, indent=2))


if __name__ == "__main__":
    main()
