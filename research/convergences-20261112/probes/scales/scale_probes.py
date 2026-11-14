#!/usr/bin/env python3
"""Small scale-selection probes. Existing research repositories remain read-only.

No observational fit. Rate and homogeneity examples are analytic toy calculations.
The gravity baseline reuses the repository's transfer-function approximation.
Run: python3 scale_probes.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
GRAVITY = HERE.parents[1] / "inputs"
sys.path.insert(0, str(GRAVITY))
spec = importlib.util.spec_from_file_location("scale_probe_wave10", GRAVITY / "wave10_covariant_jeans_unification.py")
wave10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wave10)


def collapse(sigma_r, growth, redshift=0.0, halo_delta=200.0, sigma8_factor=1.0):
    """Same PS threshold, variable halo definition or spectrum amplitude.

    Changing halo_delta at fixed mass compares conventions, not an NFW
    remeasurement of the same halo. sigma8 factors are stress tests, not posteriors.
    """
    target = wave10.DELTA_C_SPH / growth(redshift)
    lo, hi = 1.0e-4, 25.0
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if sigma_r(mid) * sigma8_factor > target:
            lo = mid
        else:
            hi = mid
    radius = (lo + hi) / 2
    mass = 4 * math.pi / 3 * (radius * wave10.MPC) ** 3 * wave10.OMEGA_M * wave10.RHO_CRIT0
    ez2 = wave10.OMEGA_M * (1 + redshift) ** 3 + wave10.OMEGA_L
    halo_radius = (3 * mass / (4 * math.pi * halo_delta * wave10.RHO_CRIT0 * ez2)) ** (1 / 3)
    circular = math.sqrt(wave10.G * mass / halo_radius) / 1000
    return {"z": redshift, "halo_Delta_relative_to_critical": halo_delta,
            "sigma8_factor": sigma8_factor, "Rstar_Mpc": radius,
            "Mstar_Msun": mass / wave10.M_SUN, "Vc_kms": circular,
            "sigma1D_isothermal_kms": circular / math.sqrt(2)}


def homogeneity_scale(gamma, tolerance_fraction, bias=1.0):
    """xi(r)=b^2 (r0/r)^gamma toy, D2=3 within fractional tolerance.

    N(<r) proportional to r^3[1+3 b^2/(3-gamma)(r0/r)^gamma].
    This is not a model fit to WiggleZ or a valid BAO-scale spectrum.
    """
    return ((3 * bias ** 2 / (3 - gamma)) * (gamma / (3 * tolerance_fraction) - 1)) ** (1 / gamma)


def main():
    sigma_r, growth = wave10.build_eh98_power_spectrum()
    base = collapse(sigma_r, growth)
    c27 = wave10.audit_c27_four_way_convergence_and_predictions({
        "sigma_star_z0_kms": base["sigma1D_isothermal_kms"],
        "press_schechter_redshift_trajectory": [
            {"z": z, "sigma_1D_star_kms": collapse(sigma_r, growth, z)["sigma1D_isothermal_kms"]}
            for z in [0.0, 0.5, 1.0]]})
    comparison = c27["four_converging_scales_kms"]
    cooling_base = comparison["bremsstrahlung_hubble_cooling_Delta1000"]
    vflat = comparison["milgrom_btfr_Lstar_vflat"]
    b = 0.6717 / (1 + 0.6717 * 1.5)
    results = {
        "status": "reproducible model calculations; no new observational evidence",
        "source_dependency": {
            "path": "inputs/wave10_covariant_jeans_unification.py",
            "sha256": hashlib.sha256((GRAVITY / "wave10_covariant_jeans_unification.py").read_bytes()).hexdigest(),
            "limitations": "Reuses wave10 approximate EH no-wiggle power spectrum and fixed cosmology. Not an independent Boltzmann-code verification."},
        "rate_responses": {
            "KZ_nu": 0.6717, "KZ_z_dynamic": 1.5, "KZ_length_exponent": b,
            "KZ_quench_100x_slower_length_factor": 100 ** b,
            "viscosity_100x_at_fixed_epsilon_eta_factor": 100 ** 0.75,
            "sonic_Mach_10x_at_fixed_L_cs_p_half_length_factor": 10 ** -2,
            "pressure_100x_W_equal_1_length_factor": 100 ** -0.25,
            "pressure_100x_fixed_time_visibility_length_factor": 100 ** -0.5,
            "assumptions": "KZ linear quench in scaling regime; Kolmogorov ordinary-fluid estimate; sonic p=1/2 illustrative; Gamma=Lambda*dx^2 with Lambda proportional to pressure and negligible other decoherence."},
        "homogeneity_toy": {
            "gamma": 1.8,
            "tolerance_scan": [{"fractional_tolerance": e, "rH_over_r0": homogeneity_scale(1.8, e)} for e in [0.1, 0.01, 0.001]],
            "bias_scan_at_1percent": [{"bias": b1, "rH_over_r0": homogeneity_scale(1.8, 0.01, b1)} for b1 in [1, 1.5, 2]],
            "interpretation": "Threshold and tracer change the reported scale in an unchanged smooth model. These are not revised WiggleZ measurements."},
        "galaxy_convergence": {
            "baseline_repository_four_scales": comparison,
            "baseline_recomputed": base,
            "vflat_converted_with_same_isothermal_rule_kms": vflat / math.sqrt(2),
            "conversion_note": "Conditional comparison only: galaxy Vflat, halo V200 and observed group line-of-sight dispersion do not have one universal conversion.",
            "cooling_density_scan": [{"Delta": d, "sigma_ff_kms": cooling_base * d / 1000} for d in [200, 500, 1000, 2500]],
            "cooling_time_scan_Delta1000": [{"t_available_in_Hubble_times": t, "sigma_ff_kms": cooling_base * t} for t in [0.1, 0.5, 1]],
            "cooling_note": "Same free-free-only local formula. Delta variation changes the gas environment; time variation changes the physical criterion. Neither is a statistical error bar or same-halo convention conversion. Low-T endpoints may invalidate free-free-only cooling.",
            "halo_convention_scan_fixed_Mstar": [collapse(sigma_r, growth, halo_delta=d) for d in [100, 200, 500, 2500]],
            "amplitude_stress_test": [collapse(sigma_r, growth, sigma8_factor=f) for f in [0.95, 1, 1.05]],
            "redshift_trajectory": [collapse(sigma_r, growth, redshift=z) for z in [0, 0.5, 1, 3]],
        },
    }
    assert abs(base["sigma1D_isothermal_kms"] - 185.59) < 0.02
    assert abs(comparison["bremsstrahlung_hubble_cooling_Delta1000"] - 178.42) < 0.01
    assert abs(results["rate_responses"]["pressure_100x_W_equal_1_length_factor"] ** 4 - 0.01) < 1e-12
    # Substitute toy homogeneity radius back into the defining D2 threshold.
    for row in results["homogeneity_toy"]["tolerance_scan"]:
        x = 3 / (3 - 1.8) * row["rH_over_r0"] ** -1.8
        d2 = 3 - 1.8 * x / (1 + x)
        assert abs((3 - d2) / 3 - row["fractional_tolerance"]) < 1e-12
    path = HERE / "results.json"
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"wrote": str(path), "baseline_sigma_kms": base["sigma1D_isothermal_kms"],
                      "matched_Lstar_sigma_kms": vflat / math.sqrt(2),
                      "cooling_density_scan": results["galaxy_convergence"]["cooling_density_scan"],
                      "KZ_100x": 100 ** b, "homogeneity": results["homogeneity_toy"]["tolerance_scan"]}, indent=2))


if __name__ == "__main__":
    main()
