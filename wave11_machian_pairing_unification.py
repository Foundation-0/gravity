"""
Foundation-0 / gravity -- Wave-11 Machian Horizon Inertia, Zero-Energy Creation, DESI Turnaround & CPT Pair-Condensate Audit (C-28..C-30; M-09)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
"""

from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path

C_SI = 299792458.0
C_KMS = 299792.458
G = 6.67430e-11
HBAR = 1.054571817e-34
K_B = 1.380649e-23
M_P = 1.67262192369e-27
M_SUN = 1.98847e30
MPC = 3.085677581491367e22
AU = 1.495978707e11
A0_EMP = 1.20e-10

H_LITTLE = 0.6736
H0_SI = (100.0 * H_LITTLE * 1000.0) / MPC
R_H = C_SI / H0_SI
RHO_CRIT0 = 3.0 * (H0_SI ** 2) / (8.0 * math.pi * G)
OMEGA_B = 0.02237 / (H_LITTLE ** 2)
OMEGA_C = 0.1200 / (H_LITTLE ** 2)
OMEGA_M = (0.02237 + 0.1200 + 0.00064) / (H_LITTLE ** 2)
OMEGA_L = 1.0 - OMEGA_M


def audit_c28_machian_inertia_and_horizon_scales() -> dict:
    """Evaluates Sciama (1953) / Braun (2026) Machian induction identities, Milgrom (1999) Unruh-de Sitter scales, and PPN/locality caveats."""
    m_hubble = (4.0 / 3.0) * math.pi * (R_H ** 3) * RHO_CRIT0
    sciama_compactness = (G * m_hubble) / (R_H * (C_SI ** 2))
    sciama_potential_integral = (2.0 * math.pi * G * RHO_CRIT0 * (R_H ** 2)) / (C_SI ** 2)
    # Braun (2026, EPJC 86, 1215): gravitomagnetic induction K_gm = (2 H0^2 R_H^2)/(3 c^2) = 2/3 + gravitoelectric K_ge = 1/3 = 1
    k_gm = (2.0 * (H0_SI ** 2) * (R_H ** 2)) / (3.0 * (C_SI ** 2))
    k_ge = 1.0 / 3.0

    a_h0 = C_SI * H0_SI
    a_ds_2pi = a_h0 / (2.0 * math.pi)
    a_lambda = a_h0 * math.sqrt(OMEGA_L)
    a_uds_2pi = a_lambda / (2.0 * math.pi)
    a_verlinde = a_h0 / 6.0

    # Unruh-de Sitter excess thermal acceleration Delta_a(a) = sqrt(a^2 + a_0_eff^2) - a_0_eff
    # Compare circular-orbit equivalence vs eccentric/solar-system non-locality requirement (Milgrom 1994, Ann. Phys. 229, 384)
    a_earth = (G * M_SUN) / (AU ** 2)
    uds_earth_fractional_shift = math.sqrt(1.0 + ((2.0 * A0_EMP) / a_earth) ** 2) - 1.0 - ((2.0 * A0_EMP) / a_earth)

    return {
        "epistemic_status": "COMPUTED (KNOWN MACHIAN & UNRUH-DE SITTER IDENTITIES; MODIFIED INERTIA VS GRAVITY OPEN)",
        "hubble_radius_Mpc": round(R_H / MPC, 2),
        "hubble_critical_mass_Msun": float(f"{m_hubble / M_SUN:.4e}"),
        "sciama_compactness_GMH_over_RH_c2": round(sciama_compactness, 6),
        "sciama_potential_integral_over_c2": round(sciama_potential_integral, 6),
        "frame_dragging_induction_partition": {
            "gravitomagnetic_K_gm": round(k_gm, 6),
            "gravitoelectric_K_ge": round(k_ge, 6),
            "total_inertial_coefficient_K_tot": round(k_gm + k_ge, 6),
        },
        "horizon_acceleration_benchmarks_m_s2": {
            "empirical_sparc_a0": A0_EMP,
            "milgrom_cH0_over_2pi": float(f"{a_ds_2pi:.4e}"),
            "unruh_desitter_cH_Lambda_over_2pi": float(f"{a_uds_2pi:.4e}"),
            "verlinde_cH0_over_6": float(f"{a_verlinde:.4e}"),
        },
        "audit_caveats": {
            "linear_sciama_ppn_gamma": 0,
            "gr_and_aest_ppn_gamma": 1,
            "earth_1AU_acceleration_over_a0": float(f"{a_earth / A0_EMP:.3e}"),
            "uds_1AU_naive_relative_offset": float(f"{uds_earth_fractional_shift:.3e}"),
            "note": "Linearized vector Sciama/Treder models give PPN gamma=0 (half GR light bending); AeST restores Phi=Psi (gamma=1). Time-local F=m*mu(a/a0)*a violates momentum conservation on multi-body orbits unless formulated non-locally (Milgrom 1994).",
        },
    }


def audit_c29_zero_energy_and_desi_turnaround() -> dict:
    """Evaluates closed-FLRW / ADM zero-energy cancellation and DESI-motivated thawing dark-energy deceleration & turnaround."""
    w0_desi = -0.75
    wa_desi = -0.85

    def rho_de_rel(a: float) -> float:
        return (a ** (-3.0 * (1.0 + w0_desi + wa_desi))) * math.exp(3.0 * wa_desi * (a - 1.0))

    def accel_sign_term(a: float) -> float:
        # proportional to -ddot(a)/a: negative means accelerating, positive means decelerating (slowing down)
        w_a = w0_desi + wa_desi * (1.0 - a)
        return OMEGA_M * (a ** -3.0) + OMEGA_L * rho_de_rel(a) * (1.0 + 3.0 * w_a)

    # Bisection for future scale factor a_slow > 1 where cosmic expansion stops accelerating and begins slowing down:
    lo_s, hi_s = 1.0, 2.5
    for _ in range(70):
        mid_s = 0.5 * (lo_s + hi_s)
        if accel_sign_term(mid_s) < 0.0:
            lo_s = mid_s
        else:
            hi_s = mid_s
    a_slow = 0.5 * (lo_s + hi_s)

    # Turnaround scale factor a_turn where H(a_turn)^2 = 0 in a spatially closed S^3 universe (Omega_k < 0) with decaying DE:
    closed_turnarounds = []
    for ok_abs in [0.001, 0.004, 0.010]:
        lo_t, hi_t = 2.0, 2000.0
        for _ in range(80):
            mt = 0.5 * (lo_t + hi_t)
            h2 = OMEGA_M * (mt ** -3.0) + OMEGA_L * rho_de_rel(mt) - ok_abs * (mt ** -2.0)
            if h2 > 0.0:
                lo_t = mt
            else:
                hi_t = mt
        closed_turnarounds.append({
            "Omega_k": -ok_abs,
            "turnaround_scale_factor_a_max": round(0.5 * (lo_t + hi_t), 2),
            "asymptotic_matter_curvature_ratio_Omega_m_over_abs_Omega_k": round(OMEGA_M / ok_abs, 2),
        })

    # Evolving horizon acceleration a_0(z) = c H(z) / (2*pi) vs c H_Lambda(z) / (2*pi) at z = 0, 1, 2 (connecting to PR #4):
    a0_evolution_comparison = []
    for z in [0.0, 0.5, 1.0, 2.0]:
        a = 1.0 / (1.0 + z)
        ez_lcdm = math.sqrt(OMEGA_M * ((1.0 + z) ** 3) + OMEGA_L)
        ez_desi = math.sqrt(OMEGA_M * ((1.0 + z) ** 3) + OMEGA_L * rho_de_rel(a))
        a0_evolution_comparison.append({
            "z": z,
            "a0_H_z_over_a0_z0_LCDM": round(ez_lcdm, 4),
            "a0_H_z_over_a0_z0_DESI": round(ez_desi, 4),
            "a0_sqrt_rhoDE_over_a0_z0_DESI": round(math.sqrt(rho_de_rel(a)), 4),
        })

    return {
        "epistemic_status": "COMPUTED (FRIEDMANN & ADM HAMILTONIAN IDENTITIES UNDER STATED EOS INPUTS)",
        "adm_hamiltonian_constraint": "H_grav + H_matter = 0 identically in GR and 3+1D AeST (Bataki et al. 2024 Eq. 43a)",
        "desi_thawing_eos_inputs": {"w0": w0_desi, "wa": wa_desi},
        "future_deceleration_onset_scale_factor_a_slow": round(a_slow, 4),
        "closed_universe_recollapse_turnarounds": closed_turnarounds,
        "machian_a0_redshift_evolution_tracks": a0_evolution_comparison,
    }


def audit_c30_cpt_pair_bifurcation_and_cogenesis() -> dict:
    """Evaluates CPT-even Mexican-hat kinetic condensate P(Q) = K_2 (Q^2/Q_0^2 - 1)^2 - Lambda_DE and cogenesis scales."""
    # Dimensionless u = Q / Q_0 around u = 0 (unbroken creation maximum) and u = +/- (1 + eps) (CPT-conjugate branches)
    # P(u) / K_2 = (u^2 - 1)^2 - lam, rho(u) / K_2 = u * 4*u*(u^2 - 1) - (u^2 - 1)^2 + lam = (u^2 - 1)*(3*u^2 + 1) + lam
    lam = 2.0  # illustrative Lambda_DE / K_2 > 1 so rho(0) > 0 at symmetric creation point
    p_u0 = 1.0 - lam
    rho_u0 = -1.0 + lam
    w_u0 = p_u0 / rho_u0

    eps = 1.0e-6
    branches = {}
    for label, sign in [("forward_sheet_plus", +1.0), ("cpt_conjugate_sheet_minus", -1.0)]:
        u = sign * (1.0 + eps)
        j0_dimless = 4.0 * u * (u * u - 1.0)
        rho_dust_dimless = u * j0_dimless - ((u * u - 1.0) ** 2)
        p_dust_dimless = (u * u - 1.0) ** 2
        branches[label] = {
            "u_value": round(u, 7),
            "noether_charge_J0_dimless": round(j0_dimless, 9),
            "dust_energy_density_dimless": round(rho_dust_dimless, 9),
            "dust_equation_of_state_w_dust": float(f"{p_dust_dimless / rho_dust_dimless:.4e}"),
        }

    net_noether_charge = (
        branches["forward_sheet_plus"]["noether_charge_J0_dimless"]
        + branches["cpt_conjugate_sheet_minus"]["noether_charge_J0_dimless"]
    )

    # Cogenesis / Asymmetric Dark Matter mass ratio vs condensate chemical-potential interpretation:
    omega_c_over_b = OMEGA_C / OMEGA_B
    m_p_gev = (M_P * (C_SI ** 2)) / 1.602176634e-10
    adm_equal_number_mass_gev = omega_c_over_b * m_p_gev
    eta_b_cmb = 6.12e-10
    annihilated_pair_fraction_visible = 1.0 - eta_b_cmb

    return {
        "epistemic_status": (
            "COMPUTED (KINETIC MEXICAN-HAT & COGENESIS ALGEBRA) & "
            "CONJECTURE (COSMOLOGICAL CPT PAIR-CREATION ORIGIN OF CONDENSATE CHARGE)"
        ),
        "unbroken_creation_state_u0": {
            "w_u0_exact": round(w_u0, 6),
        },
        "cpt_conjugate_pair_branches": branches,
        "global_net_noether_charge_sum": round(net_noether_charge, 12),
        "both_sheets_positive_dust_gravity": bool(
            branches["forward_sheet_plus"]["dust_energy_density_dimless"] > 0.0
            and branches["cpt_conjugate_sheet_minus"]["dust_energy_density_dimless"] > 0.0
        ),
        "baryon_dark_matter_remnant_scales": {
            "planck_Omega_c_over_Omega_b": round(omega_c_over_b, 4),
            "visible_baryon_to_photon_eta_B": eta_b_cmb,
            "visible_pair_annihilation_completion": round(annihilated_pair_fraction_visible, 10),
            "cogenesis_equal_charge_particle_mass_GeV": round(adm_equal_number_mass_gev, 3),
            "audit_distinction": (
                "Collisionless 5.03 GeV ADM particles would form cold dwarf cusps (sigma_J = 0), "
                "failing galactic RAR without MOND; storing the conserved cogenesis/Bogoliubov Noether "
                "charge in the coherent P(Q, Y) condensate keeps linear dust scaling while preserving "
                "galactic phonons and the Wave-10 Dark-WHIM Jeans floor."
            ),
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
    c28 = audit_c28_machian_inertia_and_horizon_scales()
    c29 = audit_c29_zero_energy_and_desi_turnaround()
    c30 = audit_c30_cpt_pair_bifurcation_and_cogenesis()

    assert c28["sciama_compactness_GMH_over_RH_c2"] == 0.5
    assert c28["frame_dragging_induction_partition"]["total_inertial_coefficient_K_tot"] == 1.0
    assert 1.35 <= c29["future_deceleration_onset_scale_factor_a_slow"] <= 1.45
    assert c30["unbroken_creation_state_u0"]["w_u0_exact"] == -1.0
    assert c30["global_net_noether_charge_sum"] == 0.0
    assert c30["both_sheets_positive_dust_gravity"] is True

    cert11 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE11-MACHIAN-PAIRING/1.0",
        "claim_c28_machian_inertia_and_horizon_induction": c28,
        "claim_c29_zero_energy_and_desi_turnaround": c29,
        "claim_c30_cpt_pair_bifurcation_and_noether_remnant": c30,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave11_machian_pairing_certificates.json"
    emit_or_verify(cert11, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
