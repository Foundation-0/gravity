/-/-
  Foundation-0 / gravity -- Wave-6 Arithmetic Lemmas (formal/Wave6Convergence.lean)
  =================================================================================
  Stock Lean 4 Init verification (zero external dependencies, zero simp warnings)
  of the three elementary integer identities and bounds accompanying Wave 6:

    1. c18_hbar_cancels_identically: Commutative-ring rearrangement over Int
       showing (twoPi * M * c * RH) * (hbar * G) * (c * c) = hbar * (c * c * c) * (twoPi * G * M * RH).
       NOTE: Algebraic product identity only; does NOT derive a_dS = c H_0 / (2*pi),
       r_M = 8.958 kpc, or d_s = 1.
    2. c19_potential_depth_clean_window: Integer interval check on the Wave-6
       |Phi|/c^2 * 10^8 entries (29 < 187 < 650 < 800 < 6852, 8 * 800 < 6852,
       36 * 187 < 6852, 236 * 29 < 6852), matching 2.8712e-7 <= 29e-8,
       1.8658e-6 <= 187e-8, 6.4938e-6 <= 650e-8, 8.00e-6 = 800e-8, and
       6.8527e-5 >= 6852e-8. NOTE: Does NOT derive Phi_crit/c^2 = 8e-6 or 388.1 km/s.
    3. c20_centroid_diffusion_epoch_and_mass_invariant: Commutative-ring rearrangement
       over Int showing (piVal * c * RH * hbar) * (2 * m) = (2 * piVal * m * c * RH) * hbar.
       NOTE: Algebraic cancellation identity independent of redshift z; NOT an
       experimental Eotvos WEP bound.

  Disclosure: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0);
              not yet reviewed by a person.
  License: Apache-2.0 (code) / CC-BY-4.0 (documentation & proofs).
-/

namespace Foundation0.Gravity.Wave6

theorem c18_hbar_cancels_identically (twoPi M c RH hbar G : Int) :
    (twoPi * M * c * RH) * (hbar * G) * (c * c) =
    hbar * (c * c * c) * (twoPi * G * M * RH) :=
  let X := (twoPi * M) * c
  let H := hbar * (c * c)
  calc
    ((X * RH) * (hbar * G)) * (c * c)
      = (c * c) * ((X * RH) * (hbar * G)) := Int.mul_comm ((X * RH) * (hbar * G)) (c * c)
    _ = (c * c) * ((hbar * G) * (X * RH)) := congrArg (fun t => (c * c) * t) (Int.mul_comm (X * RH) (hbar * G))
    _ = ((c * c) * (hbar * G)) * (X * RH) := (Int.mul_assoc (c * c) (hbar * G) (X * RH)).symm
    _ = (((c * c) * hbar) * G) * (X * RH) := congrArg (fun t => t * (X * RH)) ((Int.mul_assoc (c * c) hbar G).symm)
    _ = (H * G) * (X * RH) := congrArg (fun t => (t * G) * (X * RH)) (Int.mul_comm (c * c) hbar)
    _ = ((H * G) * X) * RH := (Int.mul_assoc (H * G) X RH).symm
    _ = ((H * G) * (c * (twoPi * M))) * RH := congrArg (fun t => ((H * G) * t) * RH) (Int.mul_comm (twoPi * M) c)
    _ = (((H * G) * c) * (twoPi * M)) * RH := congrArg (fun t => t * RH) ((Int.mul_assoc (H * G) c (twoPi * M)).symm)
    _ = ((H * (G * c)) * (twoPi * M)) * RH := congrArg (fun t => (t * (twoPi * M)) * RH) (Int.mul_assoc H G c)
    _ = ((H * (c * G)) * (twoPi * M)) * RH := congrArg (fun t => ((H * t) * (twoPi * M)) * RH) (Int.mul_comm G c)
    _ = (((H * c) * G) * (twoPi * M)) * RH := congrArg (fun t => (t * (twoPi * M)) * RH) ((Int.mul_assoc H c G).symm)
    _ = ((H * c) * (G * (twoPi * M))) * RH := congrArg (fun t => t * RH) (Int.mul_assoc (H * c) G (twoPi * M))
    _ = ((H * c) * ((G * twoPi) * M)) * RH := congrArg (fun t => ((H * c) * t) * RH) ((Int.mul_assoc G twoPi M).symm)
    _ = ((H * c) * ((twoPi * G) * M)) * RH := congrArg (fun t => ((H * c) * (t * M)) * RH) (Int.mul_comm G twoPi)
    _ = ((hbar * ((c * c) * c)) * ((twoPi * G) * M)) * RH := congrArg (fun t => (t * ((twoPi * G) * M)) * RH) (Int.mul_assoc hbar (c * c) c)
    _ = (hbar * ((c * c) * c)) * (((twoPi * G) * M) * RH) := Int.mul_assoc (hbar * ((c * c) * c)) ((twoPi * G) * M) RH

theorem c19_potential_depth_clean_window :
    let phi_lstar_1mpc_hi : Int := 29
    let phi_lstar_10kpc_hi : Int := 187
    let phi_massive_10kpc_hi : Int := 650
    let phi_crit : Int := 800
    let phi_bullet_lo : Int := 6852
    phi_lstar_1mpc_hi < phi_lstar_10kpc_hi /\
    phi_lstar_10kpc_hi < phi_massive_10kpc_hi /\
    phi_massive_10kpc_hi < phi_crit /\
    8 * phi_crit < phi_bullet_lo /\
    36 * phi_lstar_10kpc_hi < phi_bullet_lo /\
    236 * phi_lstar_1mpc_hi < phi_bullet_lo := by
  decide

theorem c20_centroid_diffusion_epoch_and_mass_invariant (piVal c RH hbar m : Int) :
    (piVal * c * RH * hbar) * (2 * m) = (2 * piVal * m * c * RH) * hbar :=
  let A := (piVal * c) * RH
  calc
    (A * hbar) * (2 * m)
      = (2 * m) * (A * hbar) := Int.mul_comm (A * hbar) (2 * m)
    _ = ((2 * m) * A) * hbar := (Int.mul_assoc (2 * m) A hbar).symm
    _ = (((2 * m) * (piVal * c)) * RH) * hbar := congrArg (fun t => t * hbar) ((Int.mul_assoc (2 * m) (piVal * c) RH).symm)
    _ = ((((2 * m) * piVal) * c) * RH) * hbar := congrArg (fun t => (t * RH) * hbar) ((Int.mul_assoc (2 * m) piVal c).symm)
    _ = (((2 * (m * piVal)) * c) * RH) * hbar := congrArg (fun t => ((t * c) * RH) * hbar) (Int.mul_assoc 2 m piVal)
    _ = (((2 * (piVal * m)) * c) * RH) * hbar := congrArg (fun t => (((2 * t) * c) * RH) * hbar) (Int.mul_comm m piVal)
    _ = ((((2 * piVal) * m) * c) * RH) * hbar := congrArg (fun t => ((t * c) * RH) * hbar) ((Int.mul_assoc 2 piVal m).symm)

/-- Earlier C-19 integer interval, retained as arithmetic only.
The current certificate uses the interval in `c19_potential_depth_clean_window`. -/
theorem c19_potential_depth_clean_window_legacy_arithmetic :
    35 < 190 ∧ 190 < 650 ∧ 650 < 800 ∧ 5 * 800 < 6000 ∧ 30 * 190 < 6000 := by decide

end Foundation0.Gravity.Wave6
