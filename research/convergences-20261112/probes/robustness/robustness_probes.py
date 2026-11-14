#!/usr/bin/env python3
"""Independent robustness probes for the convergence expedition.

Requires NumPy. Runs only mathematical examples and reads one repository JSON.
No source module is imported, no observational dataset is fitted, and writes
are confined to this directory. Use --check to compare without writing.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def mechanics():
    """Fixed-cell, Bloch k=0, unstressed central springs, k=m=1.

    Geometry is transcribed from the source proof, rather than imported from
    the repetition probe. Bond directions, not just graph edges, enter C.
    A direct finite-displacement spring energy independently checks C^T C.
    """
    motif = np.vstack([sign * np.eye(3)[axis]
                      for axis in range(3) for sign in (1, -1)])
    shear = np.array([[0, -1, -1], [1, 0, -1], [1, -1, 0.]])
    interior = [(i, j, None) for i, j in itertools.combinations(range(6), 2)
                if i // 2 != j // 2]
    bonds = interior + [(2 * axis, 2 * axis + 1, axis) for axis in range(3)]
    rng = np.random.default_rng(7913)
    displacement = rng.normal(size=18)
    displacement /= np.linalg.norm(displacement)
    rows = []
    for s in (0., .25, .5, .75, 1.):
        t = 2 * s / (1 + s*s)
        a = math.sqrt(2) * (1 - s*s) / (1 + s*s)
        cell = (2 + a) * np.eye(3) + t * shear
        C, vectors = [], []
        for i, j, axis in bonds:
            vector = motif[j] - motif[i]
            if axis is not None:
                vector = vector + cell[axis]
            np.testing.assert_allclose(vector @ vector, 2, atol=1e-13)
            direction = vector / math.sqrt(2)
            row = np.zeros(18)
            row[3*i:3*i+3] = -direction
            row[3*j:3*j+3] = direction
            C.append(row)
            vectors.append(vector)
        C = np.array(C)
        D = C.T @ C
        eigenvalues = np.linalg.eigvalsh(D)
        singular = np.linalg.svd(C, compute_uv=False)
        rank = int(np.count_nonzero(singular > 1e-10))
        # Analytic trace identity from bond-direction dot products.
        np.testing.assert_allclose(np.trace(D), 30., atol=1e-12)
        np.testing.assert_allclose(np.trace(D @ D), 96 - 12*t*t, atol=1e-12)
        expected_nullity = 6 if s == 0 else 4
        assert 18 - rank == expected_nullity
        assert (18-rank) - (15-rank) == 3
        # Independent directional Hessian from actual stretched lengths.
        def energy(epsilon):
            u = epsilon * displacement.reshape(6, 3)
            return .5 * sum((np.linalg.norm(v + u[j] - u[i]) - math.sqrt(2))**2
                            for (i, j, _), v in zip(bonds, vectors))
        epsilon = 1e-4
        from_energy = (energy(epsilon) + energy(-epsilon)) / epsilon**2
        from_matrix = float(displacement @ D @ displacement)
        assert abs(from_energy-from_matrix) < 3e-8
        # Common rigid rotation about (-1,1,1) remains a null vector.
        rotation = np.cross(np.array([-1., 1., 1.]), motif).ravel()
        np.testing.assert_allclose(C @ rotation, 0, atol=1e-12)
        rows.append({"s": s, "t": t, "squared_frequencies": eigenvalues.tolist(),
                     "sum_omega_squared": float(np.trace(D)),
                     "sum_omega_fourth": float(np.trace(D@D)),
                     "zero_modes": 18-rank, "self_stress_states": 15-rank,
                     "energy_hessian_discrepancy": abs(from_energy-from_matrix)})
    return {"scope": "Fixed-cell Bloch k=0 central-force model, equal unit masses and spring constants, no prestress; only original bars, including at the fcc endpoint.",
            "bonds_per_cell": len(bonds), "physical_coordinates_per_cell": 18,
            "analytic_sum_omega_fourth": "96 - 12 t^2",
            "rows": rows,
            "limits": "Not a full Brillouin-zone stability study, material Hamiltonian, or proof of topological protection."}


def trace_out(rho, keep, n):
    tensor = rho.reshape([2] * (2*n))
    left = n
    for axis in reversed(range(n)):
        if axis not in keep:
            tensor = np.trace(tensor, axis1=axis, axis2=axis+left)
            left -= 1
    return tensor.reshape(2**len(keep), 2**len(keep))


def entropy(rho):
    eig = np.linalg.eigvalsh(rho)
    assert eig.min() > -1e-12
    return -sum(float(v)*math.log2(float(v)) for v in eig if v > 1e-12)


def records():
    """The same dephasing channel and mutual information, different Z records.

    Branches |00>,|11> versus Bell+ and Bell-. An environment-only unitary
    relates them, so the system's channel cannot distinguish their records.
    The entangling unitary is a physical operation at fixed local access.
    """
    env = np.eye(4, dtype=complex)
    hadamard = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    cnot = np.array([[1,0,0,0], [0,1,0,0], [0,0,0,1], [0,0,1,0]])
    unitary = cnot @ np.kron(hadamard, np.eye(2)) @ cnot
    np.testing.assert_allclose(unitary.conj().T @ unitary, np.eye(4), atol=1e-14)
    branch_pairs = {"repeated_Z_records": (env[:, 0], env[:, 3]),
                    "Bell_encoded_Z_records": (unitary @ env[:, 0], unitary @ env[:, 3])}
    outputs = {}
    max_channel_error = 0.
    for name, pair in branch_pairs.items():
        isometry = np.column_stack([np.kron(np.eye(2)[:, i], pair[i]) for i in (0,1)])
        # Check the whole channel on an operator basis, including off-diagonals.
        for i, j in itertools.product(range(2), repeat=2):
            operator = np.zeros((2, 2), complex)
            operator[i, j] = 1.
            result = trace_out(isometry @ operator @ isometry.conj().T, [0], 3)
            desired = operator if i == j else np.zeros((2, 2))
            max_channel_error = max(max_channel_error, float(np.max(abs(result-desired))))
        psi = isometry @ (np.ones(2)/math.sqrt(2))
        rho = np.outer(psi, psi.conj())
        rho_s = trace_out(rho, [0], 3)
        fragments = []
        for keep in ([0], [1], [0,1]):
            branch_rhos = [trace_out(np.outer(v, v.conj()), keep, 2) for v in pair]
            average = (branch_rhos[0] + branch_rhos[1]) / 2
            chi = entropy(average) - sum(entropy(r) for r in branch_rhos)/2
            distance = np.sum(abs(np.linalg.eigvalsh(branch_rhos[0]-branch_rhos[1])))/2
            # Conditional states commute: Holevo information here is accessible.
            np.testing.assert_allclose(branch_rhos[0]@branch_rhos[1], branch_rhos[1]@branch_rhos[0], atol=1e-14)
            rho_sf = trace_out(rho, [0]+[i+1 for i in keep], 3)
            mutual = entropy(rho_s) + entropy(average) - entropy(rho_sf)
            fragments.append({"environment_qubits": keep, "Z_pointer_information_bits": chi,
                              "Z_distinguishability": float(distance), "total_mutual_information_bits": mutual})
        outputs[name] = fragments
    assert max_channel_error < 1e-13
    for name, fragments in outputs.items():
        for row in fragments[:2]:
            np.testing.assert_allclose(row["total_mutual_information_bits"], 1, atol=1e-12)
            np.testing.assert_allclose(row["Z_pointer_information_bits"], 1 if name.startswith("repeated") else 0, atol=1e-12)
        np.testing.assert_allclose(fragments[2]["Z_pointer_information_bits"], 1, atol=1e-12)
    return {"channel_error_on_all_four_matrix_units": max_channel_error,
            "examples": outputs,
            "limits": "Engineered three-qubit example, not a natural environment. The Bell construction has local records about a different system basis for the equal-amplitude input; the claimed absence concerns Z information."}


def inference():
    """Known linear map: new views remove null directions, repeat views do not.

    This example has no priors and is not nonlinear ICA. Information metrics
    transform with parameter coordinates; raw eigenvalues do not stay fixed.
    """
    target = np.array([[1., 1.]])
    reference = np.array([[0., 1.]])
    sigma2 = .01
    joint = np.vstack([target, reference])
    F = joint.T @ joint / sigma2
    S = np.diag([100., .01])
    inv_S = np.linalg.inv(S)
    transformed_F = inv_S.T @ F @ inv_S
    delta = np.array([.01, -.02])
    transformed_delta = S @ delta
    ds2 = float(delta @ F @ delta)
    transformed_ds2 = float(transformed_delta @ transformed_F @ transformed_delta)
    np.testing.assert_allclose(ds2, transformed_ds2, atol=1e-14)
    q, b, gain = .8, .3, 1.7
    obs = np.array([gain*(q+b), gain*b])
    rescale = 2.3
    alternative = np.array([gain/rescale*(rescale*q+rescale*b), gain/rescale*(rescale*b)])
    np.testing.assert_allclose(obs, alternative, atol=1e-14)
    jac = np.array([[gain, gain, q+b], [0., gain, b]])
    anchored = np.vstack([jac, [0., 0., 1.]])
    assert np.linalg.matrix_rank(jac) == 2
    assert np.linalg.matrix_rank(anchored) == 3
    # Gaussian known-design Fisher information with a shared random offset
    # after marginalizing that offset has an exact saturation, independently
    # of the separate linear-parameter rank argument above.
    saturation = []
    for n in [1, 10, 100, 1000]:
        saturation.append({"readouts": n, "correct_information_about_q": n/(sigma2+n),
                           "information_if_offset_mistakenly_independent": n/(sigma2+1)})
    return {"known_design_noise_variance": sigma2,
            "one_view_rank": int(np.linalg.matrix_rank(target)),
            "one_hundred_repeated_view_rank": int(np.linalg.matrix_rank(np.repeat(target, 100, axis=0))),
            "target_plus_reference_rank": int(np.linalg.matrix_rank(joint)),
            "Fisher_eigenvalues_original_coordinates": np.linalg.eigvalsh(F).tolist(),
            "Fisher_eigenvalues_after_coordinate_rescaling": np.linalg.eigvalsh(transformed_F).tolist(),
            "distinguishability_quadratic_form_both_coordinates": [ds2, transformed_ds2],
            "unknown_gain": {"parameters_q_b_gain": [q,b,gain], "observations": obs.tolist(),
                             "equivalent_rescaled_parameters": [rescale*q,rescale*b,gain/rescale],
                             "unanchored_rank_out_of_three": 2, "anchored_rank_out_of_three": 3},
            "shared_offset_information": saturation,
            "limits": "Linear known observation functions and specified noise. Rank is local in the gain model. Nonlinear global identifiability and blind source recovery are separate problems."}


def gravity():
    """Jeans and cooling sensitivity, independent analytic derivations.

    The Press-Schechter numbers below are *read* from the repository artifact,
    not independently revalidated. No nonlinear stability result is inferred.
    """
    G = 6.67430e-11
    hbar, me, mp = 1.054571817e-34, 9.1093837015e-31, 1.67262192369e-27
    kB, c, alpha = 1.380649e-23, 299792458., 1/137.035999084
    H0 = 67.36e3 / 3.085677581491367e22
    omega_m = (.02237+.1200+.00064)/.6736**2
    baryon_fraction = .02237/(.02237+.1200+.00064)
    rho_critical = 3*H0**2/(8*math.pi*G)
    emissivity = (16/3)*math.sqrt(2*math.pi/3)*1.2*alpha**3*(hbar/(me*c))**2*c*math.sqrt(me*c*c)
    ne = baryon_fraction * 1000*rho_critical/(1.14*mp)
    velocity = 1.15*emissivity*ne/(3*H0*math.sqrt(.60*mp))/1000
    temperature = .60*mp*(velocity*1000)**2/kB
    path = PROJECT / "inputs/wave10_covariant_jeans_certificates.json"
    payload = json.loads(path.read_text())
    trajectory = payload["claim_c26_dark_whim_nonlinear_collapse_scale"]["press_schechter_redshift_trajectory"]
    redshifts = []
    for item in trajectory:
        if item["z"] not in [0., .5, 1.]:
            continue
        Ez = math.sqrt(omega_m*(1+item["z"])**3+1-omega_m)
        redshifts.append({"z": item["z"], "H_over_H0": Ez,
                          "cooling_sigma_fixed_Delta_Hubble_clock_kms": velocity*Ez,
                          "repository_sigma_star_kms_not_independently_recomputed": item["sigma_1D_star_kms"]})
    hydrostatic = []
    x = .05
    for ratio in [.99, 1., 1.01]:
        gamma = 2*ratio**2
        integral = x**(3-gamma)
        hydrostatic.append({"sigma_h_over_sigma_star": ratio, "density_slope": gamma,
                            "inner_mass_fraction_x_0_05": integral,
                            "separately_imposed_trapped_fraction": max(0., 1-1/ratio**2)})
    conversions = []
    for gamma, beta in [(2,0), (3,0), (3,.5)]:
        conversions.append({"tracer_density_slope": gamma, "anisotropy_beta": beta,
                            "Vc_over_sigma_r": math.sqrt(gamma-2*beta)})
    assert 178.41 < velocity < 178.44
    assert hydrostatic[0]["inner_mass_fraction_x_0_05"] > 0
    return {"Jeans_constant_sigma_spherical_relation": "Vc^2 = (gamma - 2 beta) sigma_r^2",
            "conversion_examples_not_LOS_aperture_models": conversions,
            "cooling": {"ne_cm_minus3": ne/1e6, "temperature_K": temperature,
                        "sigma_kms": velocity,
                        "coefficient_erg_cm3_s_minus1_K_minus_half": emissivity*math.sqrt(kB)*1e13,
                        "density_sensitivity_Hubble_clock": "sigma_ff proportional to Delta H",
                        "density_sensitivity_freefall_clock": "sigma_ff proportional to sqrt(Delta) H",
                        "freefall_over_Hubble_at_Delta_1000": math.pi/(2*math.sqrt(1000))},
            "redshift_sensitivity": redshifts,
            "hydrostatic_crossing": hydrostatic,
            "repository_trajectory_source": {"path": "inputs/wave10_covariant_jeans_certificates.json", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
            "limits": "Free-free ionized-gas approximation with fixed composition/Gaunt factor and specified density and clock. Redshift curves change physical environments, not errors on one object. The Jeans slope does not constitute a stability analysis."}


def aest_current():
    """Differentiate the scalar part of the published action independently.

    A generic polynomial F probes both Y and Q dependence, without claiming
    this polynomial is a viable AeST model. Metric and aether are held fixed.
    """
    rng = np.random.default_rng(1701)
    metric = np.diag([-1., 1., 1., 1.])
    errors = []
    for _ in range(16):
        velocity = rng.uniform(-.2, .2, 3)
        aether = np.r_[1., velocity] / math.sqrt(1-velocity@velocity)
        q = metric + np.outer(aether, aether)
        spatial_acceleration = rng.normal(size=3)
        acceleration = np.r_[velocity@spatial_acceleration, spatial_acceleration]
        np.testing.assert_allclose(aether@metric@aether, -1., atol=1e-13)
        np.testing.assert_allclose(aether@metric@acceleration, 0., atol=1e-13)
        gradient = rng.normal(size=4)
        KB = .8
        def lagrangian(k):
            Y, Q = k@q@k, aether@k
            F = .7*Y + .3*Q**2 + .2*Y*Q + .11*Y**2 + .05*Q**3
            return (2-KB)*(2*acceleration@k-Y)-F
        Y, Q = gradient@q@gradient, aether@gradient
        FY, FQ = .7+.2*Q+.22*Y, .6*Q+.2*Y+.15*Q**2
        analytic = 2*(2-KB)*acceleration - 2*(2-KB+FY)*(q@gradient) - FQ*aether
        h = 1e-5
        numerical = np.array([(lagrangian(gradient+h*e)-lagrangian(gradient-h*e))/(2*h) for e in np.eye(4)])
        errors.append(float(np.max(abs(analytic-numerical))))
    assert max(errors) < 1e-7
    return {"points_tested": len(errors), "maximum_absolute_component_error": max(errors),
            "current": "P^mu = 2(2-KB)J^mu - 2[(2-KB)+F_Y] q^(mu nu) d_nu(phi) - F_Q A^mu",
            "conservation": "nabla_mu P^mu = 0 follows from shift symmetry for this action",
            "limits": "Derivative check only. No entropy, heat trapping, energy flux, nonlinear fluid closure, or astrophysical parameter viability follows."}


def compare(a, b, path="result"):
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        for key in a:
            compare(a[key], b[key], path+"."+key)
    elif isinstance(a, list):
        assert len(a) == len(b), path
        for i, (x,y) in enumerate(zip(a,b)):
            compare(x,y,path+f"[{i}]")
    elif isinstance(a, float):
        assert abs(a-b) <= 1e-9*max(1.,abs(a),abs(b)), (path,a,b)
    else:
        assert a == b, (path,a,b)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = {"status": "Independent mathematical probes; no observational discovery or validated dark-field mechanism.",
              "mechanics": mechanics(), "records": records(), "inference": inference(), "gravity": gravity(),
              "aest_current": aest_current()}
    target = HERE / "results.json"
    if args.check:
        compare(result, json.loads(target.read_text()))
    else:
        target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"checks": "passed", "output": str(target), "read_only_check": args.check,
                      "spring_fourth_frequency_moments": [r["sum_omega_fourth"] for r in result["mechanics"]["rows"]],
                      "gravity_redshift_sensitivity": result["gravity"]["redshift_sensitivity"]}, indent=2))


if __name__ == "__main__":
    main()
