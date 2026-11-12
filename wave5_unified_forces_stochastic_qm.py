"""
Foundation-0 / gravity -- Wave-5 Force-Scale Comparisons & Stochastic QM Checks (C-12..C-17)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
"""

from __future__ import annotations
import hashlib
import json
import math
import random
import sys
from pathlib import Path

G = 6.67430e-11
HBAR = 1.054571817e-34
C = 299792458.0
EV_J = 1.602176634e-19
GEV_J = 1.0e9 * EV_J
HBAR_C_GEV_FM = 0.1973269804
FM_M = 1.0e-15
M_E = 9.1093837015e-31
M_P = 1.67262192369e-27
M_N = 1.67492749804e-27
DALTON_KG = 1.66053906660e-27
M_SUN = 1.98847e30
PC = 3.085677581491367e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
A0 = 1.20e-10
H0_SI = 67.4e3 / MPC
M_PLANCK_GEV = math.sqrt(HBAR * C / G) * (C ** 2) / GEV_J


def check_c12_c13_force_scales() -> dict:
    sigma_qcd_gev2 = 0.180
    sigma_qcd_gev_fm = sigma_qcd_gev2 / HBAR_C_GEV_FM
    sigma_qcd_newton = (sigma_qcd_gev_fm * GEV_J) / FM_M

    def cornell_slope(r_fm: float, alpha_s: float) -> float:
        f1 = (4.0 / 3.0) * alpha_s * HBAR_C_GEV_FM / (r_fm ** 2) + sigma_qcd_gev_fm
        f2 = (4.0 / 3.0) * alpha_s * HBAR_C_GEV_FM / ((r_fm * 1.05) ** 2) + sigma_qcd_gev_fm
        return math.log(f2 / f1) / math.log(1.05)

    l_ew_m = (HBAR_C_GEV_FM / 80.377) * FM_M
    a_ew_si = (C ** 2) / l_ew_m
    sqrt_sigma_gev = math.sqrt(sigma_qcd_gev2)
    l_qcd_m = (HBAR_C_GEV_FM / sqrt_sigma_gev) * FM_M
    a_qcd_si = (C ** 2) / l_qcd_m
    l_ds_m = (2.0 * math.pi * C) / H0_SI
    a_ds_si = (C ** 2) / l_ds_m
    lambda_ds_ev = (HBAR * H0_SI / (2.0 * math.pi)) / EV_J

    alpha_uv_qcd = round((2.0 * math.pi) / (7.0 * math.log(M_PLANCK_GEV / sqrt_sigma_gev)), 5)
    alpha_uv_dark = round((2.0 * math.pi) / ((22.0 / 3.0) * math.log((M_PLANCK_GEV * 1.0e9) / lambda_ds_ev)), 5)

    return {
        "epistemic_status": "COMPUTED (KNOWN-TEXTBOOK-RELATIONS) & CONJECTURE",
        "qcd_cornell_string_tension_N": round(sigma_qcd_newton, 1),
        "qcd_force_log_slope_at_0_05fm": round(cornell_slope(0.05, 0.20), 4),
        "qcd_force_log_slope_at_2_0fm": round(cornell_slope(2.00, 0.35), 4),
        "proton_alpha_EM_over_alpha_grav": float(f"{(1.0 / 137.035999084) / (G * M_P * M_P / (HBAR * C)):.4e}"),
        "compton_and_horizon_accelerations": {
            "electroweak_mW_a_m_s2": float(f"{a_ew_si:.4e}"),
            "qcd_sqrt_sigma_a_m_s2": float(f"{a_qcd_si:.4e}"),
            "desitter_cH0_over_2pi_m_s2": float(f"{a_ds_si:.4e}"),
            "empirical_MOND_a0_m_s2": A0,
            "desitter_to_empirical_a0_ratio": round(a_ds_si / A0, 4),
            "qcd_to_desitter_ratio": float(f"{a_qcd_si / a_ds_si:.4e}"),
        },
        "one_loop_algebraic_inversion_conjecture": {
            "note": "Algebraic inversion of Lambda = M_Pl * exp(-2*pi/(beta0 * alpha_UV)); no dark beta-function is integrated.",
            "alpha_UV_QCD_beta0_7": alpha_uv_qcd,
            "alpha_UV_hypothetical_SU2_beta0_22_3": alpha_uv_dark,
            "rounded_coupling_ratio": round(alpha_uv_qcd / alpha_uv_dark, 3),
        },
    }


def check_c14_diffusivity_mass_ratio_and_wep_context() -> dict:
    species = [
        ("electron", M_E),
        ("neutron", M_N),
        ("C60_fullerene_720Da", 720.64 * DALTON_KG),
        ("oligoporphyrin_25kDa_Fein2019", 25000.0 * DALTON_KG),
    ]
    rows = [
        {
            "species": name,
            "mass_kg": float(f"{m_kg:.4e}"),
            "nelson_diffusivity_hbar_over_2m_m2_s": float(f"{HBAR / (2.0 * m_kg):.4e}"),
            "mass_ratio_m_over_me": float(f"{m_kg / M_E:.4e}"),
            "calogero1997_m_over_mn_pow_1_5": float(f"{(m_kg / M_N) ** 1.5:.4e}"),
        }
        for name, m_kg in species
    ]
    return {
        "epistemic_status": "COMPUTED (MASS-RATIO ARITHMETIC, NOT A GRAVITATIONAL WEP MEASUREMENT)",
        "clarification": (
            "4.5572e7 is the particle mass ratio m(25 kDa)/m_e. Fein et al. (2019, Nature Physics 15, 1242) "
            "measured macromolecule interference fringes, not gravitational WEP violation."
        ),
        "published_gravitational_WEP_bounds_eta": {
            "EotWash_Wagner2012_Be_Ti": "eta = (0.3 +/- 1.8)e-13 (CQG 29, 184002)",
            "MICROSCOPE_Touboul2022_Ti_Pt": "eta = [-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15 (PRL 129, 121102)",
        },
        "de_broglie_diffusivity_mass_ratio_25kDa_over_me": rows[-1]["mass_ratio_m_over_me"],
        "calogero1997_scaling_ratio_25kDa_vs_nucleon": rows[-1]["calogero1997_m_over_mn_pow_1_5"],
        "species_table": rows,
    }


def check_c15_nelson_sde_simulation() -> dict:
    rng = random.Random(20261111)
    n_p, dt, n_steps, d_coeff = 4000, 0.002, 2500, 0.5
    sqrt_dt = math.sqrt(dt)
    sqrt_2d_dt = math.sqrt(2.0 * d_coeff * dt)

    x_l = [rng.gauss(0.0, math.sqrt(0.5)) for _ in range(n_p)]
    v_l = [rng.gauss(0.0, math.sqrt(0.5)) for _ in range(n_p)]
    e0 = sum(0.5 * (v * v + x * x) for x, v in zip(x_l, v_l)) / n_p
    for _ in range(n_steps):
        for i in range(n_p):
            xi = rng.gauss(0.0, 1.0)
            vn = v_l[i] - x_l[i] * dt + sqrt_dt * xi
            x_l[i] += vn * dt
            v_l[i] = vn
    ef = sum(0.5 * (v * v + x * x) for x, v in zip(x_l, v_l)) / n_p

    x_n = [rng.gauss(0.0, math.sqrt(0.5)) for _ in range(n_p)]
    dx2_acc = 0.0
    for step in range(n_steps):
        for i in range(n_p):
            dx = -x_n[i] * dt + sqrt_2d_dt * rng.gauss(0.0, 1.0)
            if step == n_steps - 1:
                dx2_acc += dx * dx
            x_n[i] += dx
    var_x = sum(x * x for x in x_n) / n_p

    return {
        "epistemic_status": "COMPUTED (SIMULATION OF KNOWN NELSON 1966 / WALLSTROM 1994 MECHANICS)",
        "seed": 20261111,
        "undamped_white_noise_E_initial": round(e0, 4),
        "undamped_white_noise_E_final_T5": round(ef, 4),
        "undamped_heating_ratio_T5": round(ef / e0, 3),
        "nelson_ground_state_var_x_sim": round(var_x, 4),
        "nelson_ground_state_var_x_exact": 0.5,
        "short_time_dx2_over_dt_sim": round((dx2_acc / n_p) / dt, 4),
        "wallstrom_1994_note": "Single-valued wavefunctions require imposing quantized circulation int grad(theta).dl = 2*pi*k by hand.",
    }


def check_c16_c17_bell_and_disk_quadrupole() -> dict:
    omega_0 = 233.0e3 / (8.1 * KPC)
    kappa = math.sqrt(2.0) * omega_0
    lambda_epi_kpc = (35.0e3 / kappa) / KPC
    r_b = 2.97
    return {
        "c16_bell_chsh_reference": {
            "epistemic_status": "KNOWN-LITERATURE-VALUE",
            "note": "Applies to entangled quantum spin correlations (Hensen et al. 2015), not classical galactic N-body perturbations.",
            "local_hidden_variable_bound_S": 2.0,
            "quantum_tsirelson_bound_S": round(2.0 * math.sqrt(2.0), 6),
            "hensen2015_central_value_S": 2.42,
        },
        "c17_baryonic_disk_quadrupole_check": {
            "epistemic_status": "COMPUTED (CLASSICAL MULTIPOLE FALLOFF)",
            "note": "Batygin (2018, MNRAS 475, 5070) applies to quasi-Keplerian disks, not outer galactic halo rotation curves.",
            "solar_circle_epicyclic_scale_kpc": round(lambda_epi_kpc, 4),
            "disk_quadrupole_over_gN_at_100kpc": float(f"{1.5 * ((r_b / 100.0) ** 2):.4e}"),
            "disk_quadrupole_over_gN_at_1Mpc": float(f"{1.5 * ((r_b / 1000.0) ** 2):.4e}"),
            "rar_gobs_over_gN_at_1Mpc": round(math.sqrt(A0 / (G * 6.0e10 * M_SUN / ((1000.0 * KPC) ** 2))), 2),
        },
    }


def emit_or_verify(cert: dict, out_path: Path) -> None:
    canonical = json.dumps(cert, sort_keys=True, separators=(",", ":")).encode("utf-8")
    cert["sha256_canonical"] = hashlib.sha256(canonical).hexdigest()
    rendered = json.dumps(cert, indent=2) + "\n"
    if "--check" in sys.argv:
        assert out_path.is_file(), f"Missing certificate file: {out_path}"
        on_disk_text = out_path.read_text(encoding="utf-8")
        on_disk_obj = json.loads(on_disk_text)
        stored_sha = on_disk_obj.pop("sha256_canonical", None)
        disk_canonical = json.dumps(on_disk_obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
        assert stored_sha == hashlib.sha256(disk_canonical).hexdigest(), "Canonical SHA-256 mismatch on disk"
        assert stored_sha == cert["sha256_canonical"], "Recomputed canonical SHA-256 mismatch"
        assert on_disk_text == rendered, "Certificate file is not byte-identical to generator output"
        print(f"CHECK OK (byte-identical): {out_path.name} sha256_canonical={stored_sha}")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"WROTE {out_path.name} sha256_canonical={cert['sha256_canonical']}")


def main() -> int:
    c12_c13 = check_c12_c13_force_scales()
    c14 = check_c14_diffusivity_mass_ratio_and_wep_context()
    c15 = check_c15_nelson_sde_simulation()
    c16_c17 = check_c16_c17_bell_and_disk_quadrupole()

    assert 0.85 < c12_c13["compton_and_horizon_accelerations"]["desitter_to_empirical_a0_ratio"] < 0.88
    assert c14["de_broglie_diffusivity_mass_ratio_25kDa_over_me"] > 4.5e7
    assert c15["undamped_heating_ratio_T5"] > 5.0
    assert abs(c15["nelson_ground_state_var_x_sim"] - 0.5) < 0.03
    assert c16_c17["c17_baryonic_disk_quadrupole_check"]["disk_quadrupole_over_gN_at_1Mpc"] < 2.0e-5

    cert5 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE5-FORCES-STOCHASTIC-QM/1.1",
        "claims_c12_c13_force_scales": c12_c13,
        "claim_c14_diffusivity_mass_ratio": c14,
        "claim_c15_nelson_sde_simulation": c15,
        "claims_c16_c17_bell_and_disk_quadrupole": c16_c17,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave5_forces_stochastic_certificates.json"
    emit_or_verify(cert5, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
