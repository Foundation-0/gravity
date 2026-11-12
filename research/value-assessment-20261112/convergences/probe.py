#!/usr/bin/env python3
"""Convergence follow-up: fold elasticity and physical photon receptivity.

Independent NumPy implementation. No repository modules are imported and no
source snapshot is modified. All lengths and spring constants are dimensionless.
Run `python3 probe.py` to write evidence.json or `python3 probe.py --check` to
compare the numerical content with that stored output.
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
MOTIF = np.array([sign * np.eye(3)[axis]
                  for axis in range(3) for sign in (1, -1)])
SHEAR = np.array([[0., -1., -1.], [1., 0., -1.], [1., -1., 0.]])
BONDS = [(i, j, np.zeros(3)) for i, j in itertools.combinations(range(6), 2)
         if i // 2 != j // 2]
BONDS += [(2 * axis, 2 * axis + 1, np.eye(3)[axis]) for axis in range(3)]
MANDEL = [np.diag(np.eye(3)[axis]) for axis in range(3)]
for i, j in ((1, 2), (0, 2), (0, 1)):
    e = np.zeros((3, 3))
    e[i, j] = e[j, i] = 1 / math.sqrt(2)
    MANDEL.append(e)


def geometry(s):
    t = 2 * s / (1 + s*s)
    a = math.sqrt(2) * (1 - s*s) / (1 + s*s)
    cell = (2 + a) * np.eye(3) + t * SHEAR
    return a, t, cell


def compatibility(s, q=(0., 0., 0.), bonds=BONDS):
    """q are phases per lattice step, not fixed laboratory wavevectors."""
    _, _, cell = geometry(s)
    rows, affine, vectors = [], [], []
    for i, j, shift in bonds:
        vector = MOTIF[j] - MOTIF[i] + shift @ cell
        direction = vector / np.linalg.norm(vector)
        row = np.zeros(18, dtype=complex)
        row[3*i:3*i+3] = -direction
        row[3*j:3*j+3] += np.exp(1j * (np.array(q) @ shift)) * direction
        rows.append(row)
        affine.append([direction @ strain @ vector for strain in MANDEL])
        vectors.append(vector)
    return np.array(rows), np.array(affine), np.array(vectors)


def static_elasticity(s, eta=0., extra=()):
    """Relax linear internal displacements within the one-cell period.

    Optional extra bonds have rest lengths reset to the chosen reference state.
    They are a sensitivity control, not one fixed material along the fold.
    """
    C, B, _ = compatibility(s, bonds=BONDS + list(extra))
    scale = np.r_[np.ones(15), np.full(len(extra), math.sqrt(eta))]
    C, B = C.real * scale[:, None], B * scale[:, None]
    left, singular, _ = np.linalg.svd(C, full_matrices=True)
    rank = int(np.sum(singular > 1e-10))
    selfstress = left[:, rank:]
    _, _, cell = geometry(s)
    K = B.T @ selfstress @ selfstress.T @ B / np.linalg.det(cell)
    response = -np.linalg.pinv(C, rcond=1e-12) @ B
    return K, response, rank, singular


def exact_selfstress(a, t):
    """Closed form, bridge tensions (1,-1,-1), intra-bond order BONDS[:12]."""
    return np.array([a/4+t/2, a/4-t/2, a/4+t/2, a/4-t/2,
                     a/4-t/2, a/4+t/2, a/4-t/2, a/4+t/2,
                     -3*a/4-t/2, -3*a/4+t/2,
                     -3*a/4+t/2, -3*a/4-t/2, 1., -1., -1.])


def fcc_extra_bonds():
    """Integer endpoint enumeration; exactly 21 unoriented nonbar contacts."""
    _, _, cell = geometry(1.)
    candidates = set()
    for i, j, shift in itertools.product(range(6), range(6),
                                         itertools.product(range(-2, 3), repeat=3)):
        if i == j and shift == (0, 0, 0):
            continue
        v = MOTIF[j] - MOTIF[i] + np.array(shift) @ cell
        if v @ v != 2:
            continue
        edge = (i, j, shift)
        reverse = (j, i, tuple(-n for n in shift))
        candidates.add(min(edge, reverse))
    original = {min((i, j, tuple(n)), (j, i, tuple(-n))) for i, j, n in BONDS}
    extra = sorted(candidates - original)
    assert len(candidates) == 36 and len(extra) == 21
    return [(i, j, np.array(shift)) for i, j, shift in extra]


def mechanics():
    rows, max_formula_error, max_force_error = [], 0., 0.
    for s in (0., 1e-5, .001, .01, .1, .25, .5, .75, 1.):
        a, t, cell = geometry(s)
        C, B, vectors = compatibility(s)
        np.testing.assert_allclose(np.sum(vectors*vectors, axis=1), 2, atol=1e-13)
        K, response, rank, singular = static_elasticity(s)
        lambdas = np.linalg.eigvalsh(K)
        assert rank == (12 if s == 0 else 14)
        assert np.sum(lambdas > 1e-10) == (3 if s == 0 else 1)
        stress = exact_selfstress(a, t)
        force_error = float(np.max(np.abs(C.T @ stress)))
        max_force_error = max(max_force_error, force_error)
        np.testing.assert_allclose(stress @ stress, (11*a*a+12*t*t+12)/4, atol=1e-12)
        # Macroscopic stress follows from equilibrium: motif coordinates cancel.
        D = a * np.eye(3) + t * SHEAR
        M = D.T @ np.diag([1., -1., -1.]) @ cell / math.sqrt(2)
        np.testing.assert_allclose(M, M.T, atol=1e-12)
        m = np.array([np.sum(M * strain) for strain in MANDEL])
        np.testing.assert_allclose(B.T @ stress, m, atol=2e-12)
        if s > 0:
            formula = np.outer(m, m) / ((stress @ stress) * np.linalg.det(cell))
            error = float(np.max(np.abs(K-formula)))
            max_formula_error = max(max_formula_error, error)
            np.testing.assert_allclose(K, formula, atol=2e-11)
        # This stress has two negative and one positive principal value.
        principal = np.linalg.eigvalsh(M)
        assert principal[1] < 0 < principal[2]
        rows.append({"s": s, "zero_modes_at_q0": 18-rank,
                     "self_stresses_at_q0": 15-rank,
                     "mandel_elastic_eigenvalues": lambdas.tolist(),
                     "exx_internal_displacement_norm_per_unit_strain":
                         float(np.linalg.norm(response[:, 0])),
                     "unnormalized_supported_stress_principal_values": principal.tolist(),
                     "compatibility_smallest_three_singular_values": singular[-3:].tolist()})
    # Analytic s->0+ modulus, distinct from evaluating exactly at s=0.
    limit = 6 / (17 * (2 + math.sqrt(2)))
    assert abs(rows[1]["mandel_elastic_eigenvalues"][-1]-limit) < 1e-9
    # Generic q is an extra check on extensive mechanisms, already known at s=0.
    bloch = []
    phases = [np.array(q)*2*math.pi/6 for q in itertools.product(range(6), repeat=3)]
    for s in (0., .1, .5, 1.):
        histogram = {}
        for q in phases:
            C, _, _ = compatibility(s, q)
            rank = int(np.sum(np.linalg.svd(C, compute_uv=False) > 1e-10))
            nullity = 18-rank
            assert nullity >= 3
            histogram[str(nullity)] = histogram.get(str(nullity), 0) + 1
        bloch.append({"s": s, "sampled_wavevectors": len(phases),
                      "zero_mode_count_histogram": histogram})
    # Direct finite-length energy tests the Hessian along its linear minimizer.
    finite = []
    for s, strain_size in ((.1, 1e-5), (.01, 1e-7), (.001, 1e-9)):
        K, response, _, _ = static_elasticity(s)
        _, _, vectors = compatibility(s)
        _, _, cell = geometry(s)
        direction = response[:, 0].reshape(6, 3)
        def energy(h):
            return .5 * sum((np.linalg.norm(v + h*(MANDEL[0] @ v + direction[j]-direction[i]))
                             - math.sqrt(2))**2 for (i, j, _), v in zip(BONDS, vectors))
        measured = (energy(strain_size)+energy(-strain_size)) / strain_size**2
        predicted = float(np.linalg.det(cell) * K[0, 0])
        relative_error = abs(measured-predicted)/predicted
        assert relative_error < 1e-4
        finite.append({"s": s, "strain_size": strain_size,
                       "relative_energy_hessian_error": relative_error})
    extra = fcc_extra_bonds()
    # Exact integer torque minor on the original open-state rotation kernel.
    # Actual unnormalised extensions have a common factor L0=2+sqrt(2).
    selected = [(0, 1, (0, 1, 1)), (0, 2, (1, 0, 0)), (0, 3, (0, 1, 1))]
    assert all(any(i == p and j == q and tuple(n) == shift for p, q, n in extra)
               for i, j, shift in selected)
    rotation_rows = [np.cross((MOTIF[j]-MOTIF[i]).astype(int), shift).tolist()
                     for i, j, shift in selected]
    u, v, w = rotation_rows
    exact_det = (u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0])
                 + u[2]*(v[0]*w[1]-v[1]*w[0]))
    assert exact_det == 2
    completion = []
    for s in (0., .001, .01, .1, .5, 1.):
        for eta in (1e-8, 1e-6, 1e-4):
            K, _, rank, _ = static_elasticity(s, eta, extra)
            eigen = np.linalg.eigvalsh(K)
            assert rank == 15 and eigen[0] > 0
            completion.append({"s": s, "extra_spring_stiffness": eta,
                               "mandel_elastic_eigenvalues": eigen.tolist()})
    # Two simultaneous limit paths distinguish the two iterated limits.
    # eta=s is large relative to s^2; eta=s^4 is small relative to s^2.
    K_cubic = np.zeros((6, 6))
    L0 = 2 + math.sqrt(2)
    K_cubic[:3, :3] = (3*np.eye(3)+np.ones((3, 3))) / (9*L0)
    v_limit = np.array([1., -1., -1., 0., 0., 0.])
    K_fold_limit = 2*np.outer(v_limit, v_limit)/(17*L0)
    np.testing.assert_allclose(static_elasticity(0.)[0], K_cubic, atol=1e-13)
    limit_paths = []
    for s in (.01, .001, .0001):
        for path_name, eta in (("eta=s", s), ("eta=s^4", s**4)):
            K, response, _, _ = static_elasticity(s, eta, extra)
            limit_paths.append({"path": path_name, "s": s, "eta": eta,
                "distance_to_cubic_tensor": float(np.linalg.norm(K-K_cubic)),
                "distance_to_fold_limit_tensor": float(np.linalg.norm(K-K_fold_limit)),
                "exx_internal_displacement_norm_per_unit_strain": float(np.linalg.norm(response[:, 0]))})
    assert limit_paths[-2]["distance_to_cubic_tensor"] < 3e-4
    assert limit_paths[-1]["distance_to_fold_limit_tensor"] < 5e-5
    assert limit_paths[-2]["distance_to_fold_limit_tensor"] > .21
    assert limit_paths[-1]["distance_to_cubic_tensor"] > .21
    fixed_regularization_response = []
    for s in (0., 1e-6, 1e-5, 1e-4, .001, .01, .1):
        _, response, _, _ = static_elasticity(s, 1e-6, extra)
        fixed_regularization_response.append({"s": s, "eta": 1e-6,
            "exx_internal_displacement_norm_per_unit_strain": float(np.linalg.norm(response[:, 0]))})
    # Null controls: treating vector springs as scalar graph edges is rejected.
    K0 = static_elasticity(0.)[0]
    Khalf = static_elasticity(.5)[0]
    assert np.linalg.norm(K0-Khalf) > .1
    return {"model": "Unit masses and unstressed unit central springs on original 15 bars. Fixed reference fold; linear periodic internal relaxation; energy per current cell volume.",
            "claim_scope": "Mathematical extension of a specified framework. No real-material constants, nonlinear stability, or novelty priority.",
            "mandel_order": ["xx", "yy", "zz", "sqrt(2)yz", "sqrt(2)xz", "sqrt(2)xy"],
            "closed_form": {"a": "sqrt(2)*(1-s^2)/(1+s^2)", "t": "2*s/(1+s^2)",
                            "L": "(2+a)I+t*C", "D": "a*I+t*C", "C": SHEAR.tolist(),
                            "T": [1, -1, -1], "M": "D.T*T*L/sqrt(2)",
                            "stress_norm_squared": "(11*a^2+12*t^2+12)/4",
                            "elastic_tensor": "K=mandel(M)*mandel(M).T/(stress_norm_squared*det(L)), 0<s<=1",
                            "sole_modulus_s_to_zero_positive": limit},
            "fold_rows": rows, "max_formula_matrix_error": max_formula_error,
            "max_self_stress_force_error": max_force_error,
            "bloch_grid": bloch, "finite_length_checks": finite,
            "weak_spring_control": {"extra_bonds": 21,
                "scope": "FCC endpoint nonbar contacts continued to each reference geometry, positive eta, rest lengths reset at each s. Sensitivity control only; not a material model or bend-energy law.",
                "rows": completion,
                "open_state_rotation_rank_certificate": {"selected_extra_bonds": [[i, j, list(n)] for i, j, n in selected],
                    "integer_torque_rows": rotation_rows, "exact_integer_determinant": exact_det},
                "limit_tensor_distance_frobenius": float(np.linalg.norm(K_cubic-K_fold_limit)),
                "cubic_limit_tensor": K_cubic.tolist(),
                "fold_limit_tensor": K_fold_limit.tolist(),
                "simultaneous_limit_paths": limit_paths,
                "fixed_eta_response": fixed_regularization_response}}


def cap_quadrature(mu_low, mu_high, nmu=8, nphi=24):
    """Uniform solid-angle measure for a latitude band about the z axis."""
    x, w = np.polynomial.legendre.leggauss(nmu)
    mu = (mu_low+mu_high)/2 + x*(mu_high-mu_low)/2
    w = w*(mu_high-mu_low)/2
    phi = np.arange(nphi)*2*math.pi/nphi
    points = np.array([[math.sqrt(max(0, 1-z*z))*math.cos(p),
                        math.sqrt(max(0, 1-z*z))*math.sin(p), z] for z in mu for p in phi])
    weights = np.repeat(w, nphi)*2*math.pi/nphi
    return points, weights


def receptivity(sky_fraction, chi, nmu=8, nphi=24):
    mu0 = 1 - 2*sky_fraction
    incident, wi = cap_quadrature(mu0, 1., nmu, nphi)
    complement, wc = cap_quadrature(-1., mu0, nmu, nphi)
    sky, ws = cap_quadrature(-1., 1., nmu, nphi)
    dx = np.array([math.sin(chi), 0., math.cos(chi)])
    def integral(points, weights):
        kernel = (1+(incident @ points.T)**2) * (
            (incident @ dx)[:, None] - (points @ dx)[None, :])**2
        return float(wi @ kernel @ weights)
    total, available = integral(sky, ws), integral(complement, wc)
    denominator_exact = float(wi @ ((8*math.pi/15)*(3+11*(incident@dx)**2)))
    np.testing.assert_allclose(total, denominator_exact, rtol=2e-14, atol=1e-12)
    normalization = 128*math.pi*math.pi/9
    return {"sky_fraction": sky_fraction, "separation_angle_degrees": math.degrees(chi),
            "decoherence_rate_over_isotropic": total/normalization,
            "receptivity_alpha": available/total,
            "redundancy_rate_over_isotropic_decoherence": available/normalization}


def photons():
    rows = [receptivity(f, chi) for f in (.01, .25, .5, .75, .99, 1.)
            for chi in (0., math.pi/4, math.pi/2)]
    convergence_error = 0.
    for r in rows:
        independent = receptivity(r["sky_fraction"], math.radians(r["separation_angle_degrees"]), 12, 32)
        for key in ("decoherence_rate_over_isotropic", "receptivity_alpha",
                    "redundancy_rate_over_isotropic_decoherence"):
            convergence_error = max(convergence_error, abs(r[key]-independent[key]))
        assert 0 <= r["receptivity_alpha"] <= 1
        if r["sky_fraction"] == 1:
            assert r["receptivity_alpha"] == 0
            np.testing.assert_allclose(r["decoherence_rate_over_isotropic"], 1.)
    assert convergence_error < 1e-12
    # Complementary caps have the same redundancy rate by kernel symmetry.
    for f in (.01, .25, .5):
        a = receptivity(f, 0.)
        b = receptivity(1-f, 0.)
        np.testing.assert_allclose(a["redundancy_rate_over_isotropic_decoherence"],
                                   b["redundancy_rate_over_isotropic_decoherence"], atol=1e-14)
    return {"claim_class": "Reimplementation of Riedel and Zurek 2011 Eqs. 18, 21, 25, 27; not a new physics result.",
            "assumptions": "Dipole scattering, wavelength much larger than sphere and separation, elastic scattering, negligible recoil, initially independent photons, uniform blackbody cap, arbitrary photon-subset access. No measured illumination map.",
            "rate_convention": "tau_D inverse governs squared coherence; visibility amplitude decays at half this rate. Redundancy rate alpha/tau_D is an asymptotic information-rate parameter, not a count of detected bits per second.",
            "rows": rows, "quadrature_refinement_max_error": convergence_error}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    results = {"date": "2026-11-12", "mechanics": mechanics(), "photons": photons()}
    path = HERE / 'evidence.json'
    if args.check:
        prior = json.loads(path.read_text())
        assert prior == results, 'Numerical output differs from evidence.json'
        print('PASS: saved numerical evidence reproduced exactly in this environment')
    else:
        path.write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps({"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "formula_error": results['mechanics']['max_formula_matrix_error'],
                          "quadrature_error": results['photons']['quadrature_refinement_max_error']}))


if __name__ == '__main__':
    main()
