"""
Foundation-0 / gravity -- Wave-12 Cosmic-Dawn Compact Quasar Pair Audit: J1602+4228AB / Napowawa'enakaulua (C-31..C-33; M-10)
Evaluates Onorato et al. (2026, ApJL 1011, L59, arXiv:2609.31835; NOIRLab Release noirlab2627) against:
  - C-31: Cosmic-Dawn age budget, Salpeter e-folding bottleneck (Schwarzschild vs Kerr spin; pure-H vs H+He), and Pop III vs DCBH seed requirements.
  - C-32: Two-branch condensate + MOND phonon collapse at z = 6.0783 (evaluating the chosen Planck-normalized spectrum approximation sigma_*(z=6.0783) vs z=0 Dark-WHIM inversion and MOND free-fall speedup).
  - C-33: Slim-disk photon-trapping super-Eddington growth, binary orbital / projection constraints at 5.56 pkpc, and Peters (1964) GW chirp-mass budget.
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
M_P = 1.67262192369e-27
SIGMA_T = 6.6524587321e-29
M_SUN = 1.98847e30
MPC = 3.085677581491367e22
KPC = MPC / 1000.0
PC = MPC / 1.0e6
YR = 365.25 * 86400.0
MYR = 1.0e6 * YR
A0_EMP = 1.20e-10

# Planck 2018 flat cosmology including relativistic radiation density Omega_r for high-z accuracy
H_LITTLE = 0.6736
H0_SI = (100.0 * H_LITTLE * 1000.0) / MPC
OMEGA_B = 0.02237 / (H_LITTLE ** 2)
OMEGA_C = 0.1200 / (H_LITTLE ** 2)
OMEGA_M = (0.02237 + 0.1200 + 0.00064) / (H_LITTLE ** 2)
OMEGA_R = 9.236e-5
OMEGA_L = 1.0 - OMEGA_M - OMEGA_R
RHO_CRIT0 = 3.0 * (H0_SI ** 2) / (8.0 * math.pi * G)
N_S = 0.9649
SIGMA_8_TARGET = 0.8111

# Observed J1602+4228AB (Napowawa'enakaulua) parameters from Onorato et al. (2026, ApJL 1011, L59; arXiv:2609.31835)
Z_SYS_A = 6.0781
Z_SYS_B = 6.0785
Z_PAIR = 0.5 * (Z_SYS_A + Z_SYS_B)
THETA_ARCSEC = 0.98
DELTA_V_OBS_KMS = 15.0
M_BH_A_MSUN = 1.5e9
M_BH_B_MSUN = 4.0e8
LAM_EDD_A = 1.23
LAM_EDD_B = 1.07


def e_hubble(z: float) -> float:
    zp1 = 1.0 + z
    return math.sqrt(OMEGA_R * (zp1 ** 4) + OMEGA_M * (zp1 ** 3) + OMEGA_L)


def cosmic_age_myr(z: float, n_steps: int = 4000) -> float:
    """Integrates t(z) = (1/H0) int_z^inf dz' / ((1+z') E(z')) via substitution u = 1/(1+z')."""
    u_max = 1.0 / (1.0 + z)
    du = u_max / n_steps
    acc = 0.0
    for i in range(n_steps + 1):
        u = i * du
        w = 1.0 if (i == 0 or i == n_steps) else (4.0 if i % 2 == 1 else 2.0)
        if u == 0.0:
            integrand = 0.0
        else:
            zp1 = 1.0 / u
            ez = math.sqrt(OMEGA_R * (zp1 ** 4) + OMEGA_M * (zp1 ** 3) + OMEGA_L)
            integrand = 1.0 / (u * ez)
        acc += w * integrand
    t_sec = (acc * du / 3.0) / H0_SI
    return t_sec / MYR


def angular_diameter_distance_kpc(z: float, n_steps: int = 2000) -> float:
    dz = z / n_steps
    acc = 0.0
    for i in range(n_steps + 1):
        zi = i * dz
        w = 1.0 if (i == 0 or i == n_steps) else (4.0 if i % 2 == 1 else 2.0)
        acc += w / e_hubble(zi)
    chi_m = (C_SI / H0_SI) * (acc * dz / 3.0)
    return (chi_m / (1.0 + z)) / KPC


def eh98_no_wiggle_tk(k_hmpc: float) -> float:
    """Eisenstein & Hu (1998, ApJ 496, 605) zero-baryon-oscillation shape transfer function."""
    om_h2 = OMEGA_M * (H_LITTLE ** 2)
    ob_h2 = OMEGA_B * (H_LITTLE ** 2)
    theta_cmb = 2.7255 / 2.7
    s = 44.5 * math.log(9.83 / om_h2) / math.sqrt(1.0 + 10.0 * (ob_h2 ** 0.75))
    alpha_gamma = 1.0 - 0.328 * math.log(431.0 * om_h2) * (ob_h2 / om_h2) + 0.38 * math.log(22.3 * om_h2) * ((ob_h2 / om_h2) ** 2)
    k_mpc = k_hmpc * H_LITTLE
    gamma_eff = OMEGA_M * H_LITTLE * (alpha_gamma + (1.0 - alpha_gamma) / (1.0 + ((0.43 * k_mpc * s) ** 4)))
    q = k_hmpc * (theta_cmb ** 2) / gamma_eff
    l0 = math.log(2.0 * math.e + 1.8 * q)
    c0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return l0 / (l0 + c0 * (q ** 2))


def growth_factor_norm(z: float) -> float:
    """Carroll, Press & Turner (1992) linear growth factor D(z)/D(0) for flat LCDM."""
    a = 1.0 / (1.0 + z)

    def g_approx(om: float, ol: float) -> float:
        return 2.5 * om / ((om ** (4.0 / 7.0)) - ol + (1.0 + 0.5 * om) * (1.0 + ol / 70.0))

    ez2 = OMEGA_M * ((1.0 + z) ** 3) + OMEGA_L
    om_z = OMEGA_M * ((1.0 + z) ** 3) / ez2
    ol_z = OMEGA_L / ez2
    return a * g_approx(om_z, ol_z) / g_approx(OMEGA_M, OMEGA_L)


def build_sigma_r_evaluator():
    """Returns calibrated sigma_lin(R_com_Mpc, z) normalized to Planck 2018 sigma_8 = 0.8111 up to k = 5e4 Mpc^-1."""
    n_k = 1200
    lnk_min, lnk_max = math.log(1.0e-4), math.log(5.0e4)
    dlnk = (lnk_max - lnk_min) / n_k
    ks = [math.exp(lnk_min + i * dlnk) for i in range(n_k + 1)]
    tks = [eh98_no_wiggle_tk(k / H_LITTLE) for k in ks]

    def unnorm_var(r_mpc: float) -> float:
        s = 0.0
        for i, k in enumerate(ks):
            kr = k * r_mpc
            if kr < 1.0e-4:
                w_top = 1.0 - (kr ** 2) / 10.0
            else:
                w_top = 3.0 * (math.sin(kr) - kr * math.cos(kr)) / (kr ** 3)
            pk_un = (k ** N_S) * (tks[i] ** 2)
            wt = 1.0 if (i == 0 or i == n_k) else (4.0 if i % 2 == 1 else 2.0)
            s += wt * (k ** 3) * pk_un * (w_top ** 2)
        return s * dlnk / 3.0

    r8_mpc = 8.0 / H_LITTLE
    norm_factor = (SIGMA_8_TARGET ** 2) / unnorm_var(r8_mpc)

    def sigma_lin(r_mpc: float, z: float) -> float:
        return math.sqrt(norm_factor * unnorm_var(r_mpc)) * growth_factor_norm(z)

    return sigma_lin


def _adaptive_simpson(function, lo, hi, tolerance=1e-10, depth=20):
    """Absolute-error adaptive Simpson quadrature; fail rather than hide nonconvergence."""
    mid = (lo + hi) / 2.0
    fl, fm, fh = function(lo), function(mid), function(hi)
    whole = (hi - lo) * (fl + 4 * fm + fh) / 6

    def refine(a, b, fa, fc, fb, old, tol, remaining):
        c = (a + b) / 2
        fd, fe = function((a + c) / 2), function((c + b) / 2)
        left = (c - a) * (fa + 4 * fd + fc) / 6
        right = (b - c) * (fc + 4 * fe + fb) / 6
        delta = left + right - old
        if abs(delta) <= 15 * tol:
            return left + right + delta / 15
        if remaining == 0:
            raise ArithmeticError('radial potential quadrature did not converge')
        return refine(a, c, fa, fd, fc, left, tol / 2, remaining - 1) + refine(c, b, fc, fe, fb, right, tol / 2, remaining - 1)

    return refine(lo, hi, fl, fm, fh, whole, tolerance, depth)


def radial_point_mass_fall_time(mass_kg, radius_m, a0=None, additive_mass_ratio=0.0, intervals=256):
    """Rest-to-origin radial time in a fixed point-mass force, not filament dynamics.

    Integrate dt=dr/sqrt(2 int_r^r0 g(s)ds). r/r0=cos(theta)^2 removes
    both endpoint singularities. The exact Newton term is separated from the
    exponentially suppressed high-acceleration RAR correction before quadrature.
    """
    if mass_kg <= 0 or radius_m <= 0 or additive_mass_ratio < 0 or (a0 is not None and a0 <= 0):
        raise ValueError('positive mass, radius and a0 and nonnegative added ratio required')
    if intervals < 2 or intervals % 2:
        raise ValueError('an even positive Simpson interval count is required')
    gb0 = G * mass_kg / radius_m ** 2
    q0 = math.sqrt(gb0 / a0) if a0 is not None else None

    def excess(x):
        if q0 is None or x == 0 or q0 / x > 700:
            return 0.0
        return 1.0 / (x * x * math.expm1(q0 / x))

    force_at_start = 1.0 + additive_mass_ratio + excess(1.0)

    def integrand(theta):
        if theta == 0:
            return 2.0 / math.sqrt(force_at_start)
        if theta >= math.pi / 2:
            return 0.0
        x = math.cos(theta) ** 2
        # 1-x is stable near theta=0 when expressed as sin(theta)^2.
        drop = (1.0 + additive_mass_ratio) * math.sin(theta) ** 2 / x
        if a0 is not None:
            # In log radius the scaled excess integrand y/expm1(y) is bounded
            # by one even in the deep-MOND limit, avoiding a sharp inner core.
            def log_excess(t):
                y = q0 * math.exp(t)
                return 0.0 if y > 700 else y / math.expm1(y)
            drop += _adaptive_simpson(log_excess, 0.0, -math.log(x)) / q0
        return 2.0 * math.sin(theta) * math.cos(theta) / math.sqrt(drop)

    step = math.pi / (2 * intervals)
    total = sum((1 if i in (0, intervals) else 4 if i % 2 else 2) * integrand(i * step) for i in range(intervals + 1))
    return math.sqrt(radius_m / (2 * gb0)) * total * step / 3


def slim_disk_growth_time_myr(efoldings, mdot, epsilon_reference=0.10):
    """mdot=epsilon_reference*dotM_in*c^2/L_Edd; no outflows, constant duty one."""
    if mdot <= 0 or not 0 < epsilon_reference < 1:
        raise ValueError('positive inflow and efficiency between zero and one required')
    luminosity_ratio = mdot if mdot < 2 else 2 * (1 + math.log(mdot / 2))
    retained_inflow = mdot - epsilon_reference * luminosity_ratio
    if retained_inflow <= 0:
        raise ValueError('nonpositive retained black-hole growth')
    t_edd = SIGMA_T * C_SI / (4 * math.pi * G * M_P) / MYR
    return luminosity_ratio, efoldings * epsilon_reference * t_edd / retained_inflow


def audit_c31_salpeter_seed_and_clustering_wall() -> dict:
    """Evaluates Cosmic-Dawn age, Salpeter growth bottleneck, and clustering excess for J1602+4228AB."""
    t_pair_myr = cosmic_age_myr(Z_PAIR)
    t_z20_myr = cosmic_age_myr(20.0)
    t_z30_myr = cosmic_age_myr(30.0)
    da_kpc = angular_diameter_distance_kpc(Z_PAIR)
    r_proj_pkpc = THETA_ARCSEC * (math.pi / (180.0 * 3600.0)) * da_kpc

    t_edd_pure_h_myr = (SIGMA_T * C_SI) / (4.0 * math.pi * G * M_P) / MYR
    y_he = 0.245
    mu_e_prim = 2.0 / (2.0 - y_he)
    t_edd_prim_myr = t_edd_pure_h_myr / mu_e_prim

    def salpeter_myr(eps_r: float, pure_h: bool = True) -> float:
        base = t_edd_pure_h_myr if pure_h else t_edd_prim_myr
        return (eps_r / (1.0 - eps_r)) * base

    dt_from_z20 = t_pair_myr - t_z20_myr
    dt_from_z30 = t_pair_myr - t_z30_myr

    efold_a_pop3 = math.log(M_BH_A_MSUN / 100.0)
    efold_b_pop3 = math.log(M_BH_B_MSUN / 100.0)
    efold_a_dcbh = math.log(M_BH_A_MSUN / 1.0e5)
    efold_b_dcbh = math.log(M_BH_B_MSUN / 1.0e5)

    tsal_01_h = salpeter_myr(0.10, pure_h=True)
    tsal_01_prim = salpeter_myr(0.10, pure_h=False)
    tsal_02_kerr = salpeter_myr(0.20, pure_h=True)
    eps_schwarzschild = 1.0 - math.sqrt(8.0 / 9.0)
    tsal_schwarzschild_h = salpeter_myr(eps_schwarzschild, pure_h=True)
    tsal_schwarzschild_prim = salpeter_myr(eps_schwarzschild, pure_h=False)

    return {
        "epistemic_status": "COMPUTED (KNOWN-FRAMEWORK COSMOLOGICAL & SALPETER IDENTITIES; LENSING & VIRIAL MASS CAVEATS NOTED)",
        "observed_system": {
            "designation": "J1602+4228AB (Napowawa'enakaulua)",
            "z_sys_A": Z_SYS_A,
            "z_sys_B": Z_SYS_B,
            "cosmic_age_at_z_Myr": round(t_pair_myr, 2),
            "angular_diameter_distance_kpc": round(da_kpc, 2),
            "computed_projected_sep_pkpc": round(r_proj_pkpc, 2),
            "reported_projected_sep_pkpc": 5.56,
            "M_BH_A_Msun": M_BH_A_MSUN,
            "M_BH_B_Msun": M_BH_B_MSUN,
            "lambda_Edd_A": LAM_EDD_A,
            "lambda_Edd_B": LAM_EDD_B,
            "reported_clustering_excess_orders_of_magnitude": "2 to 3 (100x to 1000x over extrapolated high-z quasar clustering in 199 JWST Aether fields)",
        },
        "salpeter_timescales_Myr": {
            "pure_H_eps_0p10": round(tsal_01_h, 2),
            "primordial_H_He_eps_0p10": round(tsal_01_prim, 2),
            "fixed_Schwarzschild_primordial_H_He": round(tsal_schwarzschild_prim, 6),
            "spinning_Kerr_pure_H_eps_0p20": round(tsal_02_kerr, 2),
        },
        "growth_windows_Myr": {
            "from_z20_to_z6p08": round(dt_from_z20, 2),
            "from_z30_to_z6p08": round(dt_from_z30, 2),
        },
        "seed_duty_cycle_audit_for_J1602A_1p5e9_Msun": {
            "popIII_100Msun_efoldings": round(efold_a_pop3, 3),
            "popIII_100Msun_req_time_primordial_H_He_eps0p10_Myr": round(efold_a_pop3 * tsal_01_prim, 3),
            "popIII_100Msun_duty_primordial_H_He_eps0p10": round(efold_a_pop3 * tsal_01_prim / dt_from_z20, 6),
            "fixed_Schwarzschild_efficiency": eps_schwarzschild,
            "popIII_100Msun_req_time_pure_H_Schwarzschild_Myr": round(efold_a_pop3 * tsal_schwarzschild_h, 3),
            "popIII_100Msun_duty_pure_H_Schwarzschild": round(efold_a_pop3 * tsal_schwarzschild_h / dt_from_z20, 6),
            "popIII_100Msun_req_time_primordial_H_He_Schwarzschild_Myr": round(efold_a_pop3 * tsal_schwarzschild_prim, 3),
            "popIII_100Msun_duty_primordial_H_He_Schwarzschild": round(efold_a_pop3 * tsal_schwarzschild_prim / dt_from_z20, 6),
            "popIII_100Msun_req_time_Edd1_eps0p10_Myr": round(efold_a_pop3 * tsal_01_h, 2),
            "popIII_100Msun_duty_from_z20_Edd1_eps0p10": round((efold_a_pop3 * tsal_01_h) / dt_from_z20, 3),
            "popIII_100Msun_duty_from_z20_obsEdd1p23_eps0p10": round((efold_a_pop3 * tsal_01_h) / (LAM_EDD_A * dt_from_z20), 3),
            "popIII_100Msun_duty_from_z20_Edd1_Kerr_eps0p20": round((efold_a_pop3 * tsal_02_kerr) / dt_from_z20, 3),
            "dcbh_1e5Msun_efoldings": round(efold_a_dcbh, 3),
            "dcbh_1e5Msun_duty_from_z20_Edd1_eps0p10": round((efold_a_dcbh * tsal_01_h) / dt_from_z20, 3),
            "dcbh_1e5Msun_duty_from_z20_obsEdd1p23_eps0p10": round((efold_a_dcbh * tsal_01_h) / (LAM_EDD_A * dt_from_z20), 3),
        },
        "seed_duty_cycle_audit_for_J1602B_4p0e8_Msun": {
            "popIII_100Msun_efoldings": round(efold_b_pop3, 3),
            "popIII_100Msun_duty_from_z20_Edd1_eps0p10": round((efold_b_pop3 * tsal_01_h) / dt_from_z20, 3),
            "dcbh_1e5Msun_efoldings": round(efold_b_dcbh, 3),
            "dcbh_1e5Msun_duty_from_z20_obsEdd1p07_eps0p10": round((efold_b_dcbh * tsal_01_h) / (LAM_EDD_B * dt_from_z20), 3),
        },
        "scientific_caveats": [
            "Efficiency 0.10 is a chosen benchmark, not the Schwarzschild thin-disk efficiency. All growth clocks assume fixed efficiency, opacity, Eddington ratio and duty; present luminosity need not equal its lifetime average.",
            "Single-epoch broad-line virial BH masses carry ~2x (0.3 dex) systematic uncertainty.",
            "Spectral slopes, dust attenuation, and [O III] outflow shapes differ between A and B (favoring a physical pair), but archival HST imaging shows a candidate foreground galaxy near B; a full lens model is pending (Onorato et al. 2026).",
        ],
    }


def audit_c32_two_branch_condensate_and_phonon_collapse() -> dict:
    """Evaluates Wave-10 Dark-WHIM dispersion sigma_*(z=6.0783) and MOND phonon acceleration boost at Cosmic Dawn."""
    sigma_lin = build_sigma_r_evaluator()
    delta_c = 1.686

    lo_r, hi_r = 1.0e-4, 1.0
    assert sigma_lin(lo_r, Z_PAIR) > delta_c > sigma_lin(hi_r, Z_PAIR), "Invalid sigma_lin bracket at z=6.08"
    for _ in range(80):
        mid_r = 0.5 * (lo_r + hi_r)
        if sigma_lin(mid_r, Z_PAIR) > delta_c:
            lo_r = mid_r
        else:
            hi_r = mid_r
    r_star_com_mpc = 0.5 * (lo_r + hi_r)
    rho_m0 = OMEGA_M * RHO_CRIT0
    m_star_msun = ((4.0 / 3.0) * math.pi * ((r_star_com_mpc * MPC) ** 3) * rho_m0) / M_SUN
    hz_si = H0_SI * e_hubble(Z_PAIR)
    v200_star_kms = ((10.0 * G * (m_star_msun * M_SUN) * hz_si) ** (1.0 / 3.0)) / 1000.0
    sigma_star_z6_kms = v200_star_kms / math.sqrt(2.0)

    halo_rarities = []
    for m_h in [1.0e12, 5.0e12]:
        r_lag_mpc = (((3.0 * m_h * M_SUN) / (4.0 * math.pi * rho_m0)) ** (1.0 / 3.0)) / MPC
        sig_m = sigma_lin(r_lag_mpc, Z_PAIR)
        halo_rarities.append({
            "halo_mass_Msun": m_h,
            "comoving_lagrangian_radius_Mpc": round(r_lag_mpc, 3),
            "sigma_lin_z6p08": round(sig_m, 4),
            "gaussian_peak_height_nu": round(delta_c / sig_m, 2),
        })

    sigma_host_kms = 250.0 / math.sqrt(2.0)
    f_trap_z6 = max(0.0, 1.0 - (sigma_star_z6_kms / sigma_host_kms) ** 2)
    sigma_star_z0_kms = 185.59
    f_trap_z0 = max(0.0, 1.0 - (sigma_star_z0_kms / sigma_host_kms) ** 2)

    r_feed_m = 30.0 * KPC
    m_b_feed = 5.0e10 * M_SUN
    g_b_feed = (G * m_b_feed) / (r_feed_m ** 2)
    a0_const = A0_EMP
    a0_hubble_z6 = (C_SI * hz_si) / (2.0 * math.pi)

    def g_rar(gb: float, a0_val: float) -> float:
        return gb / (1.0 - math.exp(-math.sqrt(gb / a0_val)))

    g_mond_const_a0 = g_rar(g_b_feed, a0_const)
    g_mond_hubble_a0 = g_rar(g_b_feed, a0_hubble_z6)
    g_two_branch_const = g_mond_const_a0 + (OMEGA_C / OMEGA_B) * f_trap_z6 * g_b_feed

    t_ff_newt_myr = radial_point_mass_fall_time(m_b_feed, r_feed_m) / MYR
    t_ff_mond_const_myr = radial_point_mass_fall_time(m_b_feed, r_feed_m, a0_const) / MYR
    t_ff_mond_hubble_myr = radial_point_mass_fall_time(m_b_feed, r_feed_m, a0_hubble_z6) / MYR
    t_ff_two_branch_myr = radial_point_mass_fall_time(m_b_feed, r_feed_m, a0_const, (OMEGA_C / OMEGA_B) * f_trap_z6) / MYR
    convergence = [radial_point_mass_fall_time(m_b_feed, r_feed_m, a0_const, intervals=n) / MYR for n in (64, 128, 256)]

    return {
        "epistemic_status": "COMPUTED (CHOSEN SPECTRUM AND FIXED POINT-MASS FORCE BENCHMARKS); NO SEED-FORMATION OR FILAMENT-DYNAMICS SOLUTION",
        "planck_nonlinear_collapse_at_z6p08": {
            "R_star_comoving_Mpc": round(r_star_com_mpc, 5),
            "M_star_Msun": float(f"{m_star_msun:.4e}"),
            "sigma_star_z6p08_kms": round(sigma_star_z6_kms, 3),
            "sigma_star_z0_kms": sigma_star_z0_kms,
            "host_177kms_trapping_at_z6p08": round(f_trap_z6, 6),
            "host_177kms_trapping_at_z0": round(f_trap_z0, 6),
        },
        "lcdm_gaussian_halo_rarity_at_z6p08": halo_rarities,
        "fixed_point_mass_30pkpc_5e10Msun_radial_infall": {
            "method": "Energy-conserving radial quadrature, released from rest; fixed point mass; no pressure, angular momentum or environmental evolution",
            "MOND_const_a0_convergence_intervals": [64, 128, 256],
            "MOND_const_a0_convergence_Myr": convergence,
            "superseded_outer_acceleration_shortcuts_Myr": [182.27, 109.04, 122.79],
            "g_baryon_m_s2": float(f"{g_b_feed:.4e}"),
            "a0_const_m_s2": a0_const,
            "a0_hubble_cHz_over_2pi_m_s2": float(f"{a0_hubble_z6:.4e}"),
            "free_fall_time_pure_baryon_Newton_Myr": round(t_ff_newt_myr, 2),
            "free_fall_time_MOND_const_a0_Myr": round(t_ff_mond_const_myr, 2),
            "free_fall_time_MOND_Hubble_a0_Myr": round(t_ff_mond_hubble_myr, 2),
            "free_fall_time_two_branch_trapped_condensate_Myr": round(t_ff_two_branch_myr, 2),
        },
        "dynamical_friction_audit_note": (
            "The assigned trapping fraction is a prescription, not a capture or friction calculation. "
            "M_star is total nonlinear halo mass, not a black-hole seed. No density profile, phase-space "
            "distribution, gas collapse, cooling or merger hardening history is solved here."
        ),
    }


def audit_c33_slim_disk_and_binary_gw_budget() -> dict:
    """Evaluates slim-disk photon trapping for lambda_Edd > 1, 5.56 pkpc orbital projection, and GW merger timescale."""
    t_edd_pure_h_myr = (SIGMA_T * C_SI) / (4.0 * math.pi * G * M_P) / MYR
    efold_a_pop3 = math.log(M_BH_A_MSUN / 100.0)

    slim_disk_benchmarks = []
    for mdot in [1.0, 2.0, 3.0, 5.0]:
        lam_obs, t_grow_pop3_myr = slim_disk_growth_time_myr(efold_a_pop3, mdot)
        slim_disk_benchmarks.append({
            "dimensionless_mass_inflow_mdot": mdot,
            "radiated_lambda_Edd_slim_disk": round(lam_obs, 3),
            "popIII_100Msun_to_1p5e9Msun_time_Myr": round(t_grow_pop3_myr, 2),
        })

    r_sep_m = 5.56 * KPC
    m_bh_tot_kg = (M_BH_A_MSUN + M_BH_B_MSUN) * M_SUN
    v_kepler_bh_only_kms = math.sqrt((G * m_bh_tot_kg) / r_sep_m) / 1000.0
    m_enc_host_kg = 1.5e11 * M_SUN
    v_circ_host_kms = math.sqrt((G * (m_bh_tot_kg + m_enc_host_kg)) / r_sep_m) / 1000.0
    proj_factor_host = DELTA_V_OBS_KMS / v_circ_host_kms

    m1 = M_BH_A_MSUN * M_SUN
    m2 = M_BH_B_MSUN * M_SUN
    m_chirp_msun = (((M_BH_A_MSUN * M_BH_B_MSUN) ** 0.6) / ((M_BH_A_MSUN + M_BH_B_MSUN) ** 0.2))

    def peters_gw_myr(a_m: float) -> float:
        t_sec = (5.0 / 256.0) * (C_SI ** 5) * (a_m ** 4) / ((G ** 3) * m1 * m2 * (m1 + m2))
        return t_sec / MYR

    t_gw_at_5p56kpc_myr = peters_gw_myr(r_sep_m)
    t_gw_at_0p05pc_myr = peters_gw_myr(0.05 * PC)
    t_gw_at_0p10pc_myr = peters_gw_myr(0.10 * PC)

    return {
        "epistemic_status": "COMPUTED (SLIM-DISK ADVECTION & PETERS 1964 GW INSPIRAL IDENTITIES)",
        "slim_disk_mass_flow_convention": "mdot = epsilon_ref * dotM_in * c^2 / L_Edd; epsilon_ref=0.10; lambda=mdot below 2, otherwise 2*(1+ln(mdot/2)); dotM_BH=(mdot-epsilon_ref*lambda)*L_Edd/(epsilon_ref*c^2); no outflows; fixed coefficients and duty one",
        "slim_disk_photon_trapping_benchmarks": slim_disk_benchmarks,
        "kinematic_projection_at_5p56_pkpc": {
            "v_circ_BHs_only_kms": round(v_kepler_bh_only_kms, 2),
            "v_circ_with_1p5e11Msun_host_kms": round(v_circ_host_kms, 2),
            "observed_delta_v_los_kms": DELTA_V_OBS_KMS,
            "illustrative_abs_sin_i_cos_psi_from_point_velocity": round(proj_factor_host, 4),
        },
        "gravitational_wave_inspiral_budget": {
            "chirp_mass_Msun": float(f"{m_chirp_msun:.4e}"),
            "t_GW_at_5p56_pkpc_Myr": float(f"{t_gw_at_5p56kpc_myr:.3e}"),
            "t_GW_at_0p10_pc_Myr": round(t_gw_at_0p10pc_myr, 2),
            "t_GW_at_0p05_pc_Myr": round(t_gw_at_0p05pc_myr, 2),
            "nanograv_relevance": (
                f"At 5.56 pkpc, pure GW emission is negligible (t_GW = {t_gw_at_5p56kpc_myr:.2e} Myr); "
                f"If the pair reaches 0.05-0.10 pc, the isolated circular point-mass GW clock is "
                f"{t_gw_at_0p05pc_myr:.2f}-{t_gw_at_0p10pc_myr:.2f} Myr. "
                f"No hardening history, population merger rate or GW background prediction is supplied."
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
    c31 = audit_c31_salpeter_seed_and_clustering_wall()
    c32 = audit_c32_two_branch_condensate_and_phonon_collapse()
    c33 = audit_c33_slim_disk_and_binary_gw_budget()

    assert 5.50 <= c31["observed_system"]["computed_projected_sep_pkpc"] <= 5.75
    assert c31["seed_duty_cycle_audit_for_J1602A_1p5e9_Msun"]["popIII_100Msun_duty_from_z20_Edd1_eps0p10"] > 1.0
    assert c31["seed_duty_cycle_audit_for_J1602A_1p5e9_Msun"]["dcbh_1e5Msun_duty_from_z20_obsEdd1p23_eps0p10"] < 0.70
    assert 0.001 <= c32["planck_nonlinear_collapse_at_z6p08"]["R_star_comoving_Mpc"] <= 0.10
    assert c32["planck_nonlinear_collapse_at_z6p08"]["sigma_star_z6p08_kms"] < 2.0
    assert c32["planck_nonlinear_collapse_at_z6p08"]["host_177kms_trapping_at_z6p08"] > 0.9998
    assert c32["planck_nonlinear_collapse_at_z6p08"]["host_177kms_trapping_at_z0"] == 0.0
    assert 6.46e8 <= c33["gravitational_wave_inspiral_budget"]["chirp_mass_Msun"] <= 6.48e8

    cert12 = {
        "schema": "FOUNDATION-0/GRAVITY-WAVE12-COSMIC-DAWN-QUASAR-PAIR/1.1",
        "claim_c31_salpeter_seed_and_clustering_wall": c31,
        "claim_c32_two_branch_condensate_and_phonon_collapse": c32,
        "claim_c33_slim_disk_and_binary_gw_budget": c33,
    }
    out_path = Path(__file__).resolve().parent / "results" / "wave12_cosmic_dawn_quasar_certificates.json"
    emit_or_verify(cert12, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
