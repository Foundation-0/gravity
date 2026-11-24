# For the owners: what the evidence means for the ledger

This file lists the ledger entries that the data tests bear on. For each one it says what the evidence shows and what a review would propose. These are proposals only. Nothing in `CLAIMS.md`, `index.html` or any certificate is changed by this folder. The labels and the wording are the owners' decision.

Section numbers refer to [README.md](README.md). "As compared" means the way `wave7` and `wave10` compare model and table. "Like for like" means the model predicts the same quantity the table holds.

## Summary

| Entry | Label now | Evidence | Proposal |
|---|---|---|---|
| C-08 | `EMPIRICAL-FIT (KNOWN-FRAMEWORK)` | The four lens counts are not in the cited paper. The total is. | Correct the four counts. Keep the label. |
| C-21 | `EMPIRICAL-FIT` | The fitted onset depends on the assumed curve shape. The table mixes measured and model-derived rows. | Keep the label. Add the caveats. Report the onset as a range. |
| C-22 | `EMPIRICAL-FIT` | A plateau near R = 4 is supported. It depends on radius and on the stellar and mass-bias treatment. | Keep the label. Add the dependence. |
| C-23 | `COMPUTED & EMPIRICAL-FIT` | The one-parameter Jeans fit compares different quantities. Like for like it is 253.18, not 60.07. | Keep the crossover. Re-state or re-label the Jeans fit. |
| C-26 | `COMPUTED & CONJECTURE` | The collapse scale holds. "Zero free parameters" does not. | Split the entry. Remove "zero-parameter" from the group and cluster test. |
| C-27 | `COMPUTED / CONJECTURE` | The four speeds are about two independent scales. The falling-threshold forecast fails. | Keep `CONJECTURE`. Change "independently defined". |
| Issue 6 | open | The prediction fails in 41 galaxies, 0 reach set A and 2 reach set B. | Add the result. Reframe the statement. |

## C-08: lens counts

**What the evidence shows.** The ledger gives `52,553 + 43,727 + 22,950 + 9,797 = 129,027` isolated lenses in Mistele et al. 2024 (arXiv:2406.09685). None of these four numbers appears in that paper. The paper gives the late-type counts 24,297, 17,183, 22,083 and 11,570 and the early-type counts 1,795, 5,439, 14,220 and 32,440. Those eight counts sum to 129,027.

Per mass bin they are 26,092, 22,622, 36,303 and 44,010, which rise with mass. The ledger's four numbers fall with mass.

**Proposal.** Replace the four counts with the per-bin sums above and keep the total. The same constants are in `wave3_empirical_audit.py` (`KIDS_ISOLATED_LENS_COUNTS_BY_BIN`) and its certificate. The label can stay. The four velocity bins in `wave9_scale_convergence_audit.py` do match the paper's Table 2.

*Evidence outside this folder:* the paper's HTML text, read on 15 November 2026. The folder's section 6 uses Table 2 of the same paper for the lensing limits.

## C-21: the 126-system saturation fit

**What the evidence shows.** Twenty-eight of the table's rows are computed from cluster masses with a halo model, a concentration relation and a baryon fraction of 0.130 (`wave7...py:101-119`). Ten rows are divided by `0.80 + 1.60 * min(1, max(0, (sigma - 180)/220))` (`:81`). One row is set by hand to 1.70 (`:95`).

In the 60-system subset the fastest galaxy row is at 201.5 km/s and the slowest group row at 282.5 km/s, so no system fixes the onset. It is set by the assumed shape of the curve across that gap.

On measured quantities (section 1), the onset at the outer cluster radius is between 230 and 345 km/s and a threshold of 200 km/s is excluded in three of four treatments. In the table of 763 systems (section 3) a smooth rise fits as well as a threshold, and the free onset moves from 55 to 356 km/s.

**Proposal.** Keep `EMPIRICAL-FIT`. State that part of the input is model-derived. State that the onset "190-195 km/s" depends on the assumed curve shape. Quote the onset as the range 230 to 345 km/s (outer radius, measured masses) or drop the single number. Tag each row of the table with its provenance and fit the measured rows alone.

## C-22: plateau and unsaturated growth

**What the evidence shows.** A plateau of the dark-to-baryon ratio near 4 is supported. The like-for-like grid prefers R = 4.0 (section 1). Threshold fits at the outer radius give R between 3.4 and 6.2. The ratio is not one number across radii. Within one system the residual at the inner radius is 2.1 times that at the outer radius.

The evidence here neither supports nor contradicts the comparison with unsaturated `(sigma^2 - sigma_crit^2)^(3/2)` growth.

**Proposal.** Keep the label. Add that the plateau value `R_sat = 3.7-4.2` is not one number across radii, and that at the outer radius the range depends on the stellar and mass-bias treatment.

## C-23: crossover, apparent scales and the Jeans fit

**What the evidence shows.** The crossover `g_b,x = 0.02897 a_0` was recomputed by hand and holds. The one-parameter fit (`chi^2 = 60.07` at `sigma_J = 190 km/s`, `R = 8.5238`) has two faults. First, `R` is taken from the full non-baryonic share at `r2500`, which already contains the boost `nu`, and the model then adds `nu` again. Measured the model's own way, `R` is 4 to 7 per system.

Second, the model predicts a ratio of accelerations and the table holds a ratio of baryonic masses.

Like for like, the same fit has chi-squared 253.18 at 190 km/s. With `R` and `sigma_J` both fitted, the best is 54.0 at 200 km/s and `R = 4.0` (section 1).

**Proposal.** Keep the crossover and the CLASH and X-COP comparison as `COMPUTED`. For the Jeans fit, state that the chi-squared compares different quantities. Either restate it like for like with two fitted parameters (54.0 at 200 km/s and 4.0), or label it `CONJECTURE`. The BIC comparison with Wave 7 uses the same numbers and would change with it.

## C-26: the collapse scale and the "zero-parameter" test

**What the evidence shows.** The collapse scale is computed correctly. Separate code gives 185.59 km/s with the same transfer function and 186.93 km/s with the fuller form. Under defensible conventions it ranges from 141 to 261 km/s (section 4). The claim "zero free parameters" and `chi^2 = 60.26` for 60 degrees of freedom do not hold. Like for like the value is 256.53.

With `R` free the table prefers about 4, not 8.52.

Against measured data set A, the repository's own parameters, fails inside early-type galaxies (9 standard errors), in giant spirals, in groups and clusters, and in 41 galaxies at redshift 0.66 to 2.45 (sections 1 and 2).

**Proposal.** Split the entry. Keep `sigma_*(z=0) = 185.59 km/s` as `COMPUTED (KNOWN-FRAMEWORK)` and add the convention range. Remove "zero-parameter" and `Delta BIC = -10.01` from the group and cluster test, or restate them like for like. Label the test of set A as failed against the data in sections 1 and 2. The `CONJECTURE` scope text on the entropy-conserving dust branch can stay.

## C-27: four speeds and the Euclid forecast

**What the evidence shows.** The chance that four speeds drawn independently between 30 and 1,500 km/s land as close as the stated values is about 1 in 100,000. With the ranges that defensible choices allow it is about 2% (0.4% to 5%), and about 6% with wider ranges. The collapse scale and the cooling scale are both built from the critical density and the Hubble time.

The cooling scale is linear in an overdensity set to 1,000. The galaxy knee is a rotation speed and the others are dispersions. There are about two independent scales (section 4).

The forecast that `f_trap` rises from 0.1389 to 0.6730 and 0.8778 at redshift 0.5 and 1 follows from the falling threshold. The galaxy test in section 2 rejects that.

**Proposal.** Keep `COMPUTED / CONJECTURE`. Replace "four independently defined velocity scales" with wording that gives the ranges and says there are about two independent scales. Add that the falling-threshold forecast fails in galaxies (section 2).

## Issue 6: the falling-threshold statement

**What the evidence shows.** The issue says that `sigma_*(z)` drops from 185.59 to 114.36 and 69.92 km/s, so that the trapped fraction in a 200 km/s system rises from 0.1389 to 0.6730 and 0.8778. The arithmetic is right. The proposed observation is group lensing at redshift 0 to 1. That test has not been done, and no lensing data are used here.

The same formula applied to 41 galaxies at redshift 0.66 to 2.45 (section 2) predicts a dark fraction inside the half-light radius of at least 0.79 for set A and at least 0.64 for set B. The measured median is 0.25. No galaxy of 41 reaches the set A value and two reach the set B value.

**Proposal.** Add the result to the issue. Say that the statement is a prediction of the falling-threshold form and that the form fails in galaxies. The group-lensing test remains open. Decide whether the issue should stay open as a test of a narrower claim, a constant threshold with a different radial dependence, which section 1 does not exclude.

## What this folder does not decide

It does not decide labels, wording or which issues stay open. It does not rebuild the 126-row table of Wave 7 from published tables with a pin per row. That is the step that would settle C-21 and C-22. It does not test the group-lensing observation of issue 6.
