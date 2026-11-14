# Review of the gravity documentation update

The four new commits add documentation and a checksum manifest. They introduce no new model implementation, observation, parameter value or reference relative to the previous main commit. Nine scientific statements need correction or qualification. All nine repeat questions addressed by the earlier audit and correction work. No new parameter exploration is justified by this delta.

Review date: 12 November 2026. Reviewer: gpt-forge. Requested model configuration: gpt-6-astra, ultra. The review reads frozen Git objects and primary sources. It changes no author files and publishes nothing.

The comparison is `364fa3e9f740f42acaa1991428ce043f547e10dd` to `d1444481cdefc59a275ede2fef740ea2cf48eeec`. The correction reference is `e5d7ee813e33de03c91857e48a2d55a0caf55506`, with independent review frozen at `03f96e977c1852930c85d7568aff087e093e4d50`. Those references are separate from the reviewed main snapshot. Their corrections are not assumed to have landed on main.

The change comprises `990d866`, `ab3e633`, `4741930` and `d144448`: 48 inserted lines and nine removed lines across four files. Every other tracked blob is unchanged. [CLAIM_MAP.json](CLAIM_MAP.json) records exact before/after excerpts, source hashes, prior correction locations and reopening conditions.

## What the update adds

`METHODS_AND_PLAYBOOK.md:18-19` now lists the existing Wave 11 and Wave 12 inputs. This improves visibility: the CPL values, curvature examples, polynomial offset, feeder mass, radius, enclosed orbital mass and inflow values were already assigned in the old generators. M-09 and M-10 are new documentation labels for existing calculations.

Notebook section 5 is new prose for existing C-31 through C-33 results. The changelog adds Wave 11 and Wave 12 summaries. No generator, certificate, formal theorem, claim-ledger entry or observation table changes. The checksum refresh can support byte identity, but it adds no scientific validation. This review makes no claim about a complete manifest or Lean build pass.

## Statements requiring correction

The locations below refer to the new main commit. Before-source and prior-correction line references are recorded in the claim map.

| ID | Location | Finding and correction |
|---|---|---|
| D01 | Changelog 13 | The Machian paper is misattributed to Braun. The cited arXiv identifier belongs to Manuel Urueña Palomo. The assigned induction partition is an algebraic benchmark. |
| D02 | Changelog 14 | The Hamiltonian constraint and chosen future CPL continuation do not establish global creation-energy cancellation or an observed future turnaround. The closed-model normalization correction also remains separate. |
| D03 | Changelog 15, methods 31 | Opposite polynomial branch charges and conditional positive densities are proved. Production, stability and a protected relic abundance are not. The dust-density positivity lemma requires its supercritical-branch hypothesis. |
| D04 | Notebook 79-80, changelog 7 | The light-seed duty wall holds for chosen pure-H opacity, efficiency 0.10 and lifetime Eddington ratio one. Existing conventional counterexamples prevent a general exclusion. Heavy-seed duties quoted alongside it use different Eddington ratios. |
| D05 | Notebook 74, 80, methods 32 | The reported clustering excess concerns a small-scale extrapolation. Halo peak heights do not calculate the conditional probability of detecting a luminous quasar pair. No comparative cosmological likelihood is supplied. |
| D06 | Notebook 81-83, changelog 8, methods 32 | The nonlinear total halo mass is not a black-hole seed mass. The trapping fraction is an assigned prescription. Re-evaluating those functions at this redshift does not establish seed formation or capture. |
| D07 | Notebook 84, changelog 8 | The quoted infall shortcut is superseded by force-integrated radial times. Neither calculation supplies filament evolution, dynamical friction or merger hardening. The two quoted force cases also differ in both a0 and assigned extra mass. |
| D08 | Notebook 77, changelog 9 | The slim-disk growth times use the old retained-mass convention. At the stated inflow and luminosity, energy conservation gives corrected clocks of 273.78 and 161.23 Myr for mdot 3 and 5. |
| D09 | Notebook 84, changelog 9 | Projection and Peters clocks remain conditional examples. The observed line-of-sight velocity does not measure inclination, and no path from kiloparsec separation to subparsec hardening or GW population is calculated. |

The [Machian source](https://arxiv.org/abs/2610.09987v2) confirms the author correction. Its proposed mechanism is not newly introduced by these commits. The [reviewed correction](https://github.com/Foundation-0/gravity/blob/e5d7ee813e33de03c91857e48a2d55a0caf55506/CLAIMS.md#L144-L182) supplies the numerical and interpretation changes relevant to D01-D09.

For D03, the conserved homogeneous quantity is `a^3 P_Q`. An initial zero current does not become a nonzero branch current by algebraic selection of opposite states. The minimal scalar polynomial has `P_QQ(0) = -4 K2/Q0^2`. This does not settle stability after full AeST mixing. A shift-invariant derivative portal is also allowed, so constant shift symmetry alone does not prohibit every conversion process.

For D04, the available z=20 growth window is 734.10 Myr. Fixed efficiency 0.10 gives 827.08 Myr with pure H and 725.76 Myr with primordial H/He for the same 100-to-1.5-billion solar-mass growth. Fixed Schwarzschild efficiency gives 451.54 and 396.22 Myr, respectively.

These are counterexamples to a universal clock barrier, not evidence of a realized accretion history.

The heavy-seed duties 0.533 and 0.529 use luminosity ratios 1.23 and 1.07. The light-seed duties 1.127 and 1.037 use ratio one. A comparison should hold the luminosity history convention fixed, or label the change. Present luminosity cannot establish the lifetime average.

[Onorato et al.](https://arxiv.org/html/2609.31835v1), sections III.1, III.3 and III.4, report mass and luminosity systematics, unresolved lens modeling and velocity uncertainty. The clustering excess concerns larger-scale extrapolations. They describe that baseline as unreliable in the one-halo regime and require a statistical sample for stronger conclusions.

The paper reports about 0.36 dex scatter in Eddington ratio and adopts a conservative 100 km/s systemic-velocity uncertainty. These limitations belong beside any projection or growth interpretation. The new notebook retains the mass and lens caveats but omits these additional limits.

For D07, energy conservation requires integrating the radial force over the entire trajectory. Substituting the acceleration at the starting radius into an inverse-square infall formula produces the old 109.04 and 122.79 Myr values.

| Prescribed static force | Corrected radial time, Myr |
|---|---:|
| Newtonian baryonic point mass | 384.82 |
| Constant-a0 RAR | 200.08 |
| Hubble-scaled-a0 RAR, with no assigned extra mass | 121.72 |
| Constant-a0 RAR plus assigned condensate force | 127.16 |

These use release from rest at 30 pkpc around a fixed baryonic point mass of 5e10 solar masses. Pressure, angular momentum, evolving mass and filament geometry are absent. The previously reviewed quadrature and direct radial ODE agree. This documentation review does not rerun those tests or extend their scope.

For D08, the convention `mdot = epsilon_ref dotM_in c^2/L_Edd` requires retained growth proportional to `mdot - epsilon_ref lambda`. The old `0.90 mdot` expression is consistent only where `lambda=mdot`. The corrected example still omits outflows and fixes its coefficients. Its assigned mdot 3 and 5 values are not an inference from the observed luminosities.

## Changes needed in the new documentation

The methods can retain the new input disclosure. M-09 should describe opposite-charge polynomial states and their stated positivity conditions, with formation, stability and interaction rates unresolved. M-10 should distinguish published measurements, conditional benchmarks and actual predictive comparisons. No new fit at the observation redshift is narrower than a parameter-free physical prediction.

Notebook section 5 and the new changelog entries need the corrected radial and slim-disk numbers, the fixed-assumption growth comparison, and the source's clustering limits. The seed-scale coincidence, capture, friction and hardening statements need conditional wording. The existing Wave 11 notebook section is outside this delta, although it repeats the same origin overclaims.

The newly added certificate digests describe the uncorrected generator outputs at the reviewed main commit. They should remain explicitly tied to that version. Any future composition with the reviewed numerical correction requires regenerated digests for the composed bytes, not a claim that the old manifest certifies the correction.

## Evidence that would reopen substantive testing

For the cosmic-dawn proposal, a worthwhile next test requires a specified dynamical model that produces capture, a seed or a friction response from initial conditions. It must identify the governing equations, closure, boundary conditions and observable before choosing extra parameters. The present scalar trapping fraction supplies none of those dynamics.

A lens-model result, host-mass measurement or expanded quasar-pair sample with a selection function would justify an observational update. A comparison of cosmologies would additionally need matched occupation, triggering, duty-cycle and detection models. The reported count and halo peak heights alone do not provide that comparison.

For the origin proposal, a source or boundary prescription that produces branch charge while respecting the stated conservation law, together with full stability and portal-rate calculations, would change the assessment. Another polynomial identity would not address the missing production dynamics.

The methods update does not alter the fixed AeST response or slow-subspace inputs assessed separately. Those conclusions need their own changed equations or evidence before reopening. The current next action is to reconcile the new prose with the already reviewed corrections and preserve these explicit reopening conditions.
