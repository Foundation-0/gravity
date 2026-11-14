/-/-
  Foundation-0 / gravity -- Wave-7 Arithmetic Lemmas (formal/Wave7ThresholdAudit.lean)
  ====================================================================================
  Stock Lean 4 Init verification (zero external dependencies, zero simp warnings) of
  three integer inequalities accompanying the Wave-7 empirical curve fit (C-21, C-22):

    1. c21_stratified_onset_and_half_saturation_window:
       Checks 152 < 190 < 283 < 388 and 365^2 < 190^2 + 320^2 < 390^2.
       NOTE: Arithmetic check on fitted/reference velocity numbers only; does NOT derive
       group or cluster dynamics from first principles.
    2. c22_unbounded_tf_exceeds_cosmic_supply_cap:
       Checks 11 * (1000^2 - 388^2)^3 < (1494^2 - 388^2)^3, showing an unsaturated
       (sigma^2 - sigma_crit^2)^(3/2) curve grows by > sqrt(11) > 3.31 between 1000 and
       1494 km/s.
    3. c22_supply_capped_trapping_strictly_bounded:
       Checks over Int that (x + s) + (rSat - 1) * x < rSat * (x + s) whenever 0 < s
       and 1 < rSat (cross-multiplied Hill saturation ceiling).

  Disclosure: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0);
              not yet reviewed by a person.
  License: Apache-2.0 (code) / CC-BY-4.0 (documentation & proofs).
-/

namespace Foundation0.Gravity.Wave7

theorem c21_stratified_onset_and_half_saturation_window :
    let sigma_lstar : Int := 152
    let sigma_crit : Int := 190
    let sigma_half : Int := 320
    let sigma_ngc4125 : Int := 283
    let sigma_w6 : Int := 388
    let sigma_50_sq : Int := sigma_crit * sigma_crit + sigma_half * sigma_half
    sigma_lstar < sigma_crit /\
    sigma_crit < sigma_ngc4125 /\
    sigma_ngc4125 < sigma_w6 /\
    365 * 365 < sigma_50_sq /\
    sigma_50_sq < 390 * 390 := by
  decide

theorem c22_unbounded_tf_exceeds_cosmic_supply_cap :
    let ds_bullet : Int := 1000 * 1000 - 388 * 388
    let ds_macs : Int := 1494 * 1494 - 388 * 388
    11 * (ds_bullet * ds_bullet * ds_bullet) < (ds_macs * ds_macs * ds_macs) := by
  decide

theorem c22_supply_capped_trapping_strictly_bounded (x s rSat : Int)
    (hs : 0 < s) (hr : 1 < rSat) :
    (x + s) + (rSat - 1) * x < rSat * (x + s) := by
  have h_lhs : (x + s) + (rSat - 1) * x = rSat * x + s := by
    rw [Int.sub_mul, Int.one_mul]
    omega
  have h_rhs : rSat * (x + s) = rSat * x + rSat * s := by
    rw [Int.mul_add]
  have h_mul : 1 * s < rSat * s := Int.mul_lt_mul_of_pos_right hr hs
  have h_one : 1 * s = s := Int.one_mul s
  omega

end Foundation0.Gravity.Wave7
