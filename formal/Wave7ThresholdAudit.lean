/-
  Foundation-0 / gravity — Wave-7 Lean 4 Formal Proofs of Empirical Threshold & Supply-Cap Bounds (C-21, C-22)
  Stock Lean 4 Init formal verification (zero external dependencies).
  Disclosure: Written by AI agent (Gemini, Google, via orda-aska for Foundation-0); not yet reviewed by a person.
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
    sigma_lstar < sigma_crit ∧
    sigma_crit < sigma_ngc4125 ∧
    sigma_ngc4125 < sigma_w6 ∧
    365 * 365 < sigma_50_sq ∧
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
  have h_expand_lhs : (x + s) + (rSat - 1) * x = rSat * x + s := by
    rw [Int.sub_mul, Int.one_mul]
    omega
  have h_expand_rhs : rSat * (x + s) = rSat * x + rSat * s := by
    rw [Int.mul_add]
  rw [h_expand_lhs, h_expand_rhs]
  have h_diff : s < rSat * s := by
    have h1 : 1 * s < rSat * s := Int.mul_lt_mul_of_pos_right hr hs
    simpa [Int.one_mul] using h1
  omega

end Foundation0.Gravity.Wave7
