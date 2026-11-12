"""
Foundation-0 / gravity -- Wave-10 Linear Sound-Speed No-Go, Dark-WHIM Nonlinear Collapse Scale & 4-Way Convergence (C-25..C-27; M-08)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
"""

from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path

import wave7_group_cluster_threshold_audit as w7

C_KMS = 299792.458
C_SI = 299792458.0
G = 6.67430e-11
HBAR = 1.054571817e-34
K_B = 1.380649e-23
M_P = 1.67262192369e-27
M_E = 9.1093837015e-31
ALPHA_EM = 1.0 / 137.035999084
M_SUN = 1.98847e30
MPC = 3.085677581491367e22
KPC = 3.085677581491367e19
A0 = 1.20e-10

# Planck 2018 TT,TE,EE+lowE+lensing (arXiv:1807.06209)
H_LITTLE = 0.6736
H0_SI = (100.0 * H_LITTLE * 1000.0) / MPC
OMEGA_B_H2 = 0.02237
OMEGA_C_H2 = 0.1200
OMEGA_M_H2 = OMEGA_B_H2 + OMEGA_C_H2 + 0.00064
OMEGA_B = OMEGA_B_H2 / (H_LITTLE ** 2)
OMEGA_C = OMEGA_C_H2 / (H_LITTLE ** 2)
OMEGA_M = OMEGA_M_H2 / (H_LITTLE ** 2)
OMEGA_L = 1.0 - OMEGA_M
T_CMB = 2.7255
N_S = 0.9649
SIGMA8_PLANCK = 0.8111
DELTA_C_SPH = 1.686
RHO_CRIT0 = 3.0 * (H0_SI ** 2) / (8.0 * math.pi * G)
F_BAR_R2500 = 0.105
DUST_TO_B_R2500 = (1.0 - F_BAR_R2500) / F_BAR_R2500


def nu_rar(y: float) -> float:
    sy = math.sqrt(max(0.0, y))
    if sy == 0.0:
        return 1.0
    return 1.0 if sy > 40.0 else 1.0 / (1.0 - math.exp(-sy))


def audit_c25_linear_sound_speed_nogo() -> dict:
    """Evaluates why a homogeneous FLRW adiabatic sound speed c_s(z=0)=185 km/s fails linear cosmology."""
    cs_target_kms = 185.0
    cs0_sq_over_c2 = (cs_target_kms / C_KMS) ** 2

    # 1. Polytrope P propto rho^gamma (gamma=2 BEC self-interaction) calibrated to 185 km/s in a Delta=200 halo:
    rho_m_z1100_over_crit0 = OMEGA_M * (1101.0 ** 3)
    halo_200_over_crit0 = 200.0
    density_inversion_ratio = rho_m_z1100_over_crit0 / halo_200_over_crit0
    naive_gamma2_cs_z1100_over_c = (cs_target_kms / C_KMS) * math.sqrt(density_inversion_ratio)

    # 2. Constant-M k^4 scordatura / quantum-pressure Jeans wavenumber scaling: k_J,com(z) / k_J,com(0) = (1+z)^(-1/4)
    scordatura_kJ_ratio_z1100_to_z0 = 1101.0 ** (-0.25)

    # 3. Shift-symmetric K(Q) = Lambda^4 * eps^p around Q_0 across p = 2, 4, 8, 16, 32:
    k_power_scan = []
    kJ_com_z0_Mpc_inv = math.sqrt(1.5 * OMEGA_M) * (100.0 * H_LITTLE / cs_target_kms)
    lambda_J_com_z0_Mpc = (2.0 * math.pi) / kJ_com_z0_Mpc_inv

    for p in [2.0, 4.0, 8.0, 16.0, 32.0]:
        eps0 = (p - 1.0) * cs0_sq_over_c2 / (1.0 - (p - 1.0) * cs0_sq_over_c2)
        target = (p * (eps0 ** (p - 1.0)) + (p - 1.0) * (eps0 ** p)) * (1101.0 ** 3)
        lo_l, hi_l = math.log(eps0), 40.0
        for _ in range(90):
            mid_l = 0.5 * (lo_l + hi_l)
            m = math.exp(mid_l)
            val = p * (m ** (p - 1.0)) + (p - 1.0) * (m ** p)
            if val < target:
                lo_l = mid_l
            else:
                hi_l = mid_l
        ez = math.exp(0.5 * (lo_l + hi_l))
        w_1100 = ez / (p + (p - 1.0) * ez)
        cs_1100 = C_KMS * math.sqrt(ez / ((p - 1.0) * (1.0 + ez)))
        kJ_1100 = math.sqrt(1.5 * OMEGA_M) * (100.0 * H_LITTLE / cs_1100) * math.sqrt(1101.0)
        k_power_scan.append({
            "power_p": p,
            "eps_z0": float(f"{eps0:.4e}"),
            "w_z1100": float(f"{w_1100:.4e}"),
            "cs_z1100_kms": round(cs_1100, 2),
            "k_J_com_z1100_Mpc_inv": round(kJ_1100, 4),
        })

    return {
        "epistemic_status": "COMPUTED (LINEAR PERTURBATION & JEANS SCALING NO-GO BOUND)",
        "target_halo_dispersion_kms": cs_target_kms,
        "homogeneous_z0_comoving_kJ_Mpc_inv": round(kJ_com_z0_Mpc_inv, 4),
        "homogeneous_z0_comoving_lambdaJ_Mpc": round(lambda_J_com_z0_Mpc, 2),
        "recombination_matter_density_over_crit0": round(rho_m_z1100_over_crit0, 1),
        "recombination_to_virial200_density_ratio": round(density_inversion_ratio, 1),
        "polytrope_gamma2_naive_cs_z1100_over_c": round(naive_gamma2_cs_z1100_over_c, 4),
        "scordatura_k4_comoving_kJ_ratio_z1100_over_z0": round(scordatura_kJ_ratio_z1100_to_z0, 4),
        "shift_symmetric_K_power_scan": k_power_scan,
    }


def build_eh98_power_spectrum():
    """Constructs Planck-2018 normalized Eisenstein & Hu (1998, ApJ 496, 605) linear sigma(R) and D(z)."""
    theta_27 = T_CMB / 2.7

    def eh98_T(k_Mpc: float) -> float:
        q_k = k_Mpc / H_LITTLE
        alpha_g = (
            1.0
            - 0.328 * math.log(431.0 * OMEGA_M_H2) * (OMEGA_B / OMEGA_M)
            + 0.38 * math.log(22.3 * OMEGA_M_H2) * ((OMEGA_B / OMEGA_M) ** 2)
        )
        s_sound = 44.5 * math.log(9.83 / OMEGA_M_H2) / math.sqrt(1.0 + 10.0 * (OMEGA_B_H2 ** 0.75))
        gamma_eff = OMEGA_M * H_LITTLE * (alpha_g + (1.0 - alpha_g) / (1.0 + (0.43 * k_Mpc * s_sound) ** 4))
        q = q_k * (theta_27 ** 2) / gamma_eff
        l0 = math.log(2.0 * math.e + 1.8 * q)
        c0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
        return l0 / (l0 + c0 * q * q)

    def top_hat_W(x: float) -> float:
        if x < 1.0e-4:
            return 1.0 - (x * x) / 10.0
        return 3.0 * (math.sin(x) - x * math.cos(x)) / (x ** 3)

    nk = 1600
    lk_min, lk_max = math.log(1.0e-5), math.log(300.0)
    dlk = (lk_max - lk_min) / nk
    ks = [math.exp(lk_min + (i + 0.5) * dlk) for i in range(nk)]
    dks = [k * dlk for k in ks]
    unnorm = [(k ** N_S) * (eh98_T(k) ** 2) for k in ks]
    r8 = 8.0 / H_LITTLE
    sig8_raw = math.sqrt(
        sum((ks[i] ** 2 * dks[i] / (2.0 * math.pi ** 2)) * unnorm[i] * (top_hat_W(ks[i] * r8) ** 2) for i in range(nk))
    )
    pk0 = [unnorm[i] * ((SIGMA8_PLANCK / sig8_raw) ** 2) for i in range(nk)]

    def sigma_R0(r_Mpc: float) -> float:
        s2 = sum((ks[i] ** 2 * dks[i] / (2.0 * math.pi ** 2)) * pk0[i] * (top_hat_W(ks[i] * r_Mpc) ** 2) for i in range(nk))
        return math.sqrt(s2)

    def E_z(z: float) -> float:
        return math.sqrt(OMEGA_M * ((1.0 + z) ** 3) + OMEGA_L)

    def D_raw(z: float) -> float:
        nz = 1600
        u0, u1 = math.log(1.0 + z), math.log(max(5000.0, 50.0 * (1.0 + z)))
        du = (u1 - u0) / nz
        acc = 0.0
        for i in range(nz):
            zp1 = math.exp(u0 + (i + 0.5) * du)
            ez = math.sqrt(OMEGA_M * (zp1 ** 3) + OMEGA_L)
            acc += (zp1 ** 2) * du / (ez ** 3)
        return 2.5 * OMEGA_M * E_z(z) * acc

    d0 = D_raw(0.0)
    return sigma_R0, (lambda z: D_raw(z) / d0)


def audit_c26_nonlinear_collapse_and_k0_test(sigma_R0, D_norm) -> dict:
    """Computes Planck-2018 Press-Schechter sigma_*(z), Jeans core-collapse slope, and k=0 126-system test."""
    trajectory = []
    sigma_star_z0 = 0.0

    for z in [0.0, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0]:
        dz = D_norm(z)
        target = DELTA_C_SPH / dz
        lo, hi = 1.0e-4, 25.0
        for _ in range(55):
            mid = math.sqrt(lo * hi)
            if sigma_R0(mid) > target:
                lo = mid
            else:
                hi = mid
        rs = 0.5 * (lo + hi)
        ms = (4.0 / 3.0) * math.pi * ((rs * MPC) ** 3) * (OMEGA_M * RHO_CRIT0)
        ez2 = OMEGA_M * ((1.0 + z) ** 3) + OMEGA_L
        r200_z = ((3.0 * ms) / (4.0 * math.pi * 200.0 * RHO_CRIT0 * ez2)) ** (1.0 / 3.0)
        v200_kms = math.sqrt(G * ms / r200_z) / 1000.0
        sig1d_kms = v200_kms / math.sqrt(2.0)
        if z == 0.0:
            sigma_star_z0 = sig1d_kms
        trajectory.append({
            "z": z,
            "D_z": round(dz, 4),
            "R_star_comoving_Mpc": round(rs, 4),
            "M_star_Msun": float(f"{ms / M_SUN:.3e}"),
            "V_200_kms": round(v200_kms, 2),
            "sigma_1D_star_kms": round(sig1d_kms, 2),
        })

    # Hydrostatic Jeans log-slope gamma_d = 2*(sigma_halo/sigma_*)^2 and enclosed core dust fraction (r/R_vir)^(3-gamma_d)
    core_suppression_examples = []
    for name, sig_h, r_in_kpc, r_vir_kpc in [
        ("Dwarf_50kms", 35.0, 5.0, 75.0),
        ("Lstar_spiral_176kms", 125.0, 10.0, 220.0),
        ("Threshold_halo_185_6kms", sigma_star_z0, 15.0, 300.0),
    ]:
        gamma_d = 2.0 * ((sig_h / sigma_star_z0) ** 2)
        f_inner = (r_in_kpc / r_vir_kpc) ** max(0.0, 3.0 - gamma_d)
        core_suppression_examples.append({
            "system": name,
            "sigma_halo_kms": round(sig_h, 2),
            "hydrostatic_density_slope_gamma_d": round(gamma_d, 4),
            "r_probe_kpc": r_in_kpc,
            "R_vir_kpc": r_vir_kpc,
            "enclosed_dust_fraction_inside_r_probe": round(f_inner, 6),
            "enclosed_dust_over_Mb_cosmic_cap": round((OMEGA_C / OMEGA_B) * f_inner, 5),
        })

    # Zero-fitted-parameter (k = 0) evaluation on Wave-7 126-system benchmark using sigma_J = sigma_*(z=0)
    def pred_k0(sigma_kms: float) -> float:
        if sigma_kms <= sigma_star_z0:
            return 0.0
        f_trap = 1.0 - ((sigma_star_z0 / sigma_kms) ** 2)
        g_tot = 2.0 * ((sigma_kms * 1.0e3) ** 2) / (250.0 * KPC)
        lo_g, hi_g = 1.0e-15, g_tot
        for _ in range(55):
            mid_g = 0.5 * (lo_g + hi_g)
            if mid_g * (nu_rar(mid_g / A0) + f_trap * DUST_TO_B_R2500) < g_tot:
                lo_g = mid_g
            else:
                hi_g = mid_g
        gb_sol = 0.5 * (lo_g + hi_g)
        return math.log10(g_tot / (gb_sol * nu_rar(gb_sol / A0)))

    all_rows = w7.build_catalog()
    w_77 = [r for r in all_rows if 150.0 <= r["sig"] <= 1200.0]
    clean_60 = [r for r in all_rows if r["cat"] not in ("Milgrom2019_opt", "Milgrom2019_rich")]

    k0_fits = {}
    for key, ds, w7_bic, w9_k1_bic in [
        ("clean_60", clean_60, 70.27, 64.167),
        ("primary_77", w_77, 113.11, 110.7794),
        ("full_126", all_rows, 156.83, 152.9667),
    ]:
        res = w7.odr_chi2(ds, pred_k0)
        res["k_fitted_params"] = 0
        res["bic_k0"] = res["chi2"]
        res["delta_bic_vs_wave7_3param"] = round(res["chi2"] - w7_bic, 2)
        res["delta_bic_vs_wave9_1param"] = round(res["chi2"] - w9_k1_bic, 2)
        k0_fits[key] = res

    return {
        "epistemic_status": (
            "COMPUTED (ZERO-FREE-PARAMETER PRESS-SCHECHTER SCALE & JEANS SLOPE) & "
            "CONJECTURE (NONLINEAR AEST FLUID-SHOCK CLOSURE WITHOUT DARK COOLING)"
        ),
        "sigma_star_z0_kms": round(sigma_star_z0, 2),
        "press_schechter_redshift_trajectory": trajectory,
        "hydrostatic_jeans_slope_suppression": core_suppression_examples,
        "zero_fitted_parameter_catalog_benchmarks": k0_fits,
    }


def audit_c27_four_way_convergence_and_predictions(c26: dict) -> dict:
    """Compares the 4 converging ~185 km/s velocity scales and generates high-z Euclid group predictions."""
    sigma_star_z0 = c26["sigma_star_z0_kms"]
    v_lstar_kms = ((G * 6.0e10 * M_SUN * A0) ** 0.25) / 1000.0

    # Rees-Ostriker free-free Hubble-cooling transition at inner halo / group core overdensity Delta = 1000:
    g_ff = 1.2
    c_ff = (
        (16.0 / 3.0)
        * math.sqrt(2.0 * math.pi / 3.0)
        * g_ff
        * (ALPHA_EM ** 3)
        * ((HBAR / (M_E * C_SI)) ** 2)
        * C_SI
        * math.sqrt(M_E * (C_SI ** 2))
    )
    f_b_cosmic = OMEGA_B / OMEGA_M
    n_e_1000 = (f_b_cosmic * 1000.0 * RHO_CRIT0) / (1.14 * M_P)
    sqrt_kbt_1000 = (1.15 * c_ff * n_e_1000 * (1.0 / H0_SI)) / 3.0
    sigma_ff_delta1000_kms = math.sqrt((sqrt_kbt_1000 ** 2) / (0.60 * M_P)) / 1000.0

    # Equivalent AeST Lorentz-norm parameter Q_0 if X = Q^2 - Y instead produced constant sigma_J = a0 / (2 c Q_0):
    q0_inv_Mpc = ((2.0 * C_SI * (sigma_star_z0 * 1000.0)) / A0) / MPC

    # Discriminating high-z prediction for a sigma = 200 km/s group across z = 0, 0.5, 1.0:
    z_map = {row["z"]: row["sigma_1D_star_kms"] for row in c26["press_schechter_redshift_trajectory"]}
    euclid_group_200kms_forecast = []
    for z in [0.0, 0.5, 1.0]:
        sj_dyn = z_map[z]
        f_trap_dyn = max(0.0, 1.0 - (sj_dyn / 200.0) ** 2)
        f_trap_const = max(0.0, 1.0 - (sigma_star_z0 / 200.0) ** 2)
        euclid_group_200kms_forecast.append({
            "redshift_z": z,
            "dynamic_dark_whim_sigma_J_kms": sj_dyn,
            "dynamic_f_trap_at_200kms": round(f_trap_dyn, 4),
            "constant_lagrangian_f_trap_at_200kms": round(f_trap_const, 4),
        })

    return {
        "epistemic_status": "COMPUTED (SCALE COMPARISON & FALSIFIABLE REDSHIFT FORECAST) / CONJECTURE (SINGULAR-ORIGIN COINCIDENCE)",
        "four_converging_scales_kms": {
            "empirical_wave9_group_onset_clean60_full126": [180.0, 190.0],
            "planck2018_press_schechter_Mstar_z0": sigma_star_z0,
            "milgrom_btfr_Lstar_vflat": round(v_lstar_kms, 2),
            "bremsstrahlung_hubble_cooling_Delta1000": round(sigma_ff_delta1000_kms, 2),
        },
        "lorentz_norm_equivalent_Q0_inv_Mpc": round(q0_inv_Mpc, 3),
        "euclid_lsst_200kms_group_redshift_test": euclid_group_200kms_forecast,
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
    c25 = audit_c25_linear_sound_speed_nogo()
    sigma_R0, D_norm = build_eh98_power_spectrum()
    c26 = audit_c26_nonlinear_collapse_and_k0_test(sigma_R0, D_norm)
    c27 = audit_c27_four_way_convergence_and_predictions(c26)

    assert c25["homogeneous_z0_comoving_lambdaJ_Mpc"] > 20.0
    assert c25["recombination_to_virial200_density_ratio"] > 2.0e6
    assert 183.0 <= c26["sigma_star_z0_kms"] <= 188.0
    assert c26["press_schechter_redshift_trajectory"][5]["sigma_1D_star_kms"] < 15.0
    assert c26["zero_fitted_parameter_catalog_benchmarks"]["clean_60"]["bic_k0"] < 61.0
    assert c26["zero_fitted_parameter_catalog_benchmarks"]["clean_60"]["delta_bic_vs_wave7_3param"] < -9.5

    cert10 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE10-JEANS-UNIFICATION/1.0",
        "claim_c25_linear_sound_speed_nogo": c25,
        "claim_c26_dark_whim_nonlinear_collapse_scale": c26,
        "claim_c27_four_way_scale_convergence_and_forecasts": c27,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave10_covariant_jeans_certificates.json"
    emit_or_verify(cert10, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
