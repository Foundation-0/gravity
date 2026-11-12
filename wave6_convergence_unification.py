"""
Foundation-0 / gravity -- Wave-6 Algebraic Re-Parameterizations & Potential Ansatz (C-18..C-20)
attribution: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
license: Apache-2.0 (code) / CC-BY-4.0 (results).
"""

from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path

G = 6.67430e-11
HBAR = 1.054571817e-34
C = 299792458.0
M_E = 9.1093837015e-31
M_N = 1.67492749804e-27
DALTON_KG = 1.66053906660e-27
M_SUN = 1.98847e30
PC = 3.085677581491367e16
KPC = 1.0e3 * PC
MPC = 1.0e6 * PC
H0_SI = 67.4e3 / MPC
R_H = C / H0_SI
A_DS = C * H0_SI / (2.0 * math.pi)
A0_EMP = 1.20e-10
L_PLANCK = math.sqrt(HBAR * G / (C ** 3))


def check_c18_milgrom_radius_identity() -> dict:
    bodies = [
        ("proton", 1.67262192369e-27),
        ("Sun_1Msun", M_SUN),
        ("dwarf_galaxy_1e8Msun", 1.0e8 * M_SUN),
        ("Lstar_spiral_6e10Msun", 6.0e10 * M_SUN),
    ]
    rows = []
    max_float_diff = 0.0
    for label, m_kg in bodies:
        n_fil = (2.0 * math.pi * m_kg * C * R_H) / HBAR
        r_from_nfil = L_PLANCK * math.sqrt(n_fil)
        r_mond_ds = math.sqrt(G * m_kg / A_DS)
        rel_diff = abs(r_from_nfil - r_mond_ds) / r_mond_ds
        max_float_diff = max(max_float_diff, rel_diff)
        rows.append({
            "system": label,
            "defined_N_fil": float(f"{n_fil:.4e}"),
            "r_M_at_a_dS_m": float(f"{r_mond_ds:.4e}"),
            "ieee754_float64_rounding_rel_diff": float(f"{rel_diff:.3e}"),
        })

    r_m_lstar_kpc = math.sqrt(G * 6.0e10 * M_SUN / A_DS) / KPC
    return {
        "epistemic_status": "COMPUTED (ALGEBRAIC RE-PARAMETERIZATION OF MILGROM 1983) & CONJECTURE",
        "caveat": (
            "hbar cancels algebraically by definition of N_fil; 8.9580 kpc is the standard MOND "
            "radius r_M = sqrt(G*M_b/a_dS) for 6e10 M_sun; float64 residual is machine rounding."
        ),
        "a_dS_cH0_over_2pi_m_s2": float(f"{A_DS:.5e}"),
        "lstar_MOND_radius_at_a_dS_kpc": round(r_m_lstar_kpc, 4),
        "postulated_filament_spectral_dimension_ds": 1.0,
        "max_ieee754_float64_rounding_rel_diff": float(f"{max_float_diff:.3e}"),
        "benchmarks": rows,
    }


def check_c19_potential_depth_ansatz() -> dict:
    m_gal = 6.0e10 * M_SUN
    v_flat = (G * m_gal * A0_EMP) ** 0.25
    r_efe = 834.8 * KPC
    phi_1kpc = ((v_flat ** 2) / (C ** 2)) * (1.0 + math.log(r_efe / (1.0 * KPC)))
    phi_10kpc = ((v_flat ** 2) / (C ** 2)) * (1.0 + math.log(r_efe / (10.0 * KPC)))
    phi_100kpc = ((v_flat ** 2) / (C ** 2)) * (1.0 + math.log(r_efe / (100.0 * KPC)))
    phi_1mpc_kepler = ((v_flat ** 2) / (C ** 2)) * (r_efe / (1.0 * MPC))

    v_massive = 300.0e3
    r_efe_massive = math.sqrt(G * 5.0e11 * M_SUN / A0_EMP) / 0.01
    phi_massive_10kpc = ((v_massive ** 2) / (C ** 2)) * (1.0 + math.log(r_efe_massive / (10.0 * KPC)))

    sigma_bullet = 1000.0e3
    phi_bullet_250kpc = (2.0 * (sigma_bullet ** 2) / (C ** 2)) * (1.0 + math.log(2000.0 / 250.0))

    phi_crit_c2 = 8.0e-6
    sigma_onset_kms = (C * math.sqrt(phi_crit_c2 / (2.0 * (1.0 + math.log(4.0))))) / 1.0e3

    return {
        "epistemic_status": "CONJECTURE / PHENOMENOLOGICAL-THRESHOLD-ANSATZ",
        "caveat": (
            "Phi_crit/c^2 = 8.0e-6 is placed by hand between galactic logarithmic MOND potentials "
            "and the Bullet Cluster isothermal well (following the Berezhiani & Khoury 2015 galaxy/cluster "
            "phase split); sigma_onset = 388.1 km/s solves 2*(sigma/c)^2*(1+ln 4) = 8.0e-6 at r/R_vir = 1/4; "
            "Delta_N_eff = 0.0 is assumed via a non-thermal T=0 condensate."
        ),
        "potential_depth_Phi_over_c2": {
            "Lstar_logMOND_1kpc": float(f"{phi_1kpc:.4e}"),
            "Lstar_logMOND_10kpc": float(f"{phi_10kpc:.4e}"),
            "Lstar_logMOND_100kpc": float(f"{phi_100kpc:.4e}"),
            "Lstar_KeplerTail_1Mpc": float(f"{phi_1mpc_kepler:.4e}"),
            "massive_300kms_logMOND_10kpc": float(f"{phi_massive_10kpc:.4e}"),
            "Bullet_isothermal_250kpc": float(f"{phi_bullet_250kpc:.4e}"),
            "bullet_to_Lstar_10kpc_ratio": round(phi_bullet_250kpc / phi_10kpc, 2),
            "bullet_to_Lstar_1Mpc_ratio": round(phi_bullet_250kpc / phi_1mpc_kepler, 2),
        },
        "chosen_threshold_Phi_crit_over_c2": phi_crit_c2,
        "assumed_nonthermal_T0_Delta_N_eff": 0.0,
        "implied_single_zone_onset_sigma1D_kms": round(sigma_onset_kms, 1),
    }


def check_c20_algebraic_cancellation() -> dict:
    species = [
        ("electron", M_E),
        ("neutron", M_N),
        ("C60_720Da", 720.64 * DALTON_KG),
        ("oligoporphyrin_25kDa", 25000.0 * DALTON_KG),
    ]
    d1_today = math.pi * C * R_H
    max_float_diff = max(
        abs((d1_today / ((2.0 * math.pi * m_kg * C * R_H) / HBAR)) - (HBAR / (2.0 * m_kg))) / (HBAR / (2.0 * m_kg))
        for _, m_kg in species
    )
    omega_r, omega_m, omega_l = 9.2e-5, 0.315, 0.6849
    epoch_rows = []
    for name, z in [("today_z0", 0.0), ("quasar_z3", 3.0), ("CMB_z1100", 1100.0), ("BBN_z1e9", 1.0e9)]:
        hz_ratio = math.sqrt(omega_r * ((1.0 + z) ** 4) + omega_m * ((1.0 + z) ** 3) + omega_l)
        rh_z = R_H / hz_ratio
        d1_z = math.pi * C * rh_z
        n_fil_z = (2.0 * math.pi * M_E * C * rh_z) / HBAR
        hbar_ratio = (2.0 * M_E * (d1_z / n_fil_z)) / HBAR
        epoch_rows.append({
            "epoch": name,
            "redshift_z": z,
            "algebraic_identity_hbar_over_hbar0": round(hbar_ratio, 12),
            "calogero1997_sqrt_RH_ratio_contrast": float(f"{math.sqrt(rh_z / R_H):.4e}"),
        })
    return {
        "epistemic_status": "COMPUTED (ALGEBRAIC CANCELLATION IDENTITY, NOT A WEP OR REDSHIFT MEASUREMENT)",
        "caveat": (
            "Defining N_fil = 2*pi*m*c*R_H(z)/hbar cancels m and R_H(z) identically in D_1/N_fil = hbar/(2m). "
            "Float64 residual (~2.3e-16) is IEEE-754 rounding, not an Eotvos WEP parameter eta."
        ),
        "single_filament_D1_today_m2_s": float(f"{d1_today:.4e}"),
        "max_ieee754_float64_rounding_rel_diff": float(f"{max_float_diff:.3e}"),
        "epoch_cancellation_table": epoch_rows,
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
    c18 = check_c18_milgrom_radius_identity()
    c19 = check_c19_potential_depth_ansatz()
    c20 = check_c20_algebraic_cancellation()

    assert c18["max_ieee754_float64_rounding_rel_diff"] < 1.0e-14
    assert c19["potential_depth_Phi_over_c2"]["bullet_to_Lstar_10kpc_ratio"] > 35.0
    assert c19["implied_single_zone_onset_sigma1D_kms"] == 388.1
    assert c20["max_ieee754_float64_rounding_rel_diff"] < 1.0e-15

    cert6 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE6-CONVERGENCE-UNIFICATION/1.1",
        "claim_c18_milgrom_radius_identity": c18,
        "claim_c19_potential_depth_ansatz": c19,
        "claim_c20_algebraic_cancellation": c20,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave6_convergence_certificates.json"
    emit_or_verify(cert6, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
