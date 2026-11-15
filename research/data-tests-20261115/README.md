# Tests of the 185 km/s claims against published data

This folder tests the repository's velocity-threshold story against published measurements of galaxies, groups and clusters. It also holds the fit of the acceleration-evolution idea to galaxy data and a study of a light-particle idea, which is marked as conjecture. Every result has a program, a saved output and one command.

**Status: REPRODUCED by the programs here. The collapse scale and the 60-system comparison are also VERIFIED by a separately written program (`threshold-185/g185_independent.py`). Prepared by an automated agent team. Not reviewed by a person.** No claim label or ledger entry is changed. The proposals for the ledger are in [FOR-THE-OWNERS.md](FOR-THE-OWNERS.md).

It refers to issue 1 (tests on the SPARC galaxy sample) and issue 6 (the redshift prediction). The SPARC tables are used here for a different question than issue 1 asks, the threshold, and no `d_s` fit is made. Issue 6 is tested directly in section 2.

## How to run

From the repository root. Python 3.11 or later, `numpy` and `scipy` ([requirements.txt](requirements.txt)), `python-flint` for one job, and `curl` plus `pdftotext` to fetch the published tables.

```sh
python3 research/data-tests-20261115/fetch_sources.py   # downloads the published tables into sources/
python3 research/data-tests-20261115/check.py           # re-runs everything in a temporary copy and compares
python3 -O research/data-tests-20261115/check.py        # the same, with the programs run under -O
```

`check.py` writes nothing into the folder. It compares each program's output byte for byte with the saved file. It also changes four inputs and expects the program to fail. Without `sources/` the jobs that read published tables are skipped and the exit status is 3. The fit in section 5 takes about six minutes and runs only with `--full`.

The downloaded files are not stored here. [SOURCES.md](SOURCES.md) lists each file with its address and the date it was read.

## Layout

| Folder | Question | Section |
|---|---|---|
| `threshold-185/` | Does extra mass switch on above about 185 km/s | 1 |
| `redshift-prediction/` | Does the threshold fall with redshift as issue 6 says | 2 |
| `unified-table/` | One table of 763 systems, the fits, and what is forced by definition | 3 |
| `four-speeds/` | How likely is the four-speed coincidence | 4 |
| `acceleration-evolution-fit/` | Does the acceleration scale follow the expansion rate | 5 |
| `neutrino-like-conjecture/` | A light particle in clusters, and a woven picture. Conjecture | 6 |

Marks used below: **[F]** a fact from data or a run, **[I]** an inference, **[P]** a published value, **[C]** a conjecture.

## 1. The 185 km/s threshold against published data

The wave scripts say that extra dark mass switches on in systems whose velocity scale is above a threshold. They say the threshold is the collapse scale of the standard cosmology, 185.59 km/s today. The repository's own table cannot test this, because part of it is computed by the model. These programs predict the same quantity the data holds.

Two parameter sets were tested. Set A is the repository's claim: threshold 185.59 km/s, dark-to-baryon ratio R = 8.524. Set B is the best like-for-like fit to the repository's table: 200 km/s and R = 4.0. The model is re-implemented in `threshold-185/model.py` and imports nothing from the repository.

**Result.** [F] The like-for-like chi-squared of set A is 256.53 on the 60-system subset, against 60.26 as the scripts compare. The scripts compare a ratio of accelerations. The table holds a ratio of baryonic masses. With R free, the table prefers about 4, not 8.52, and a threshold near 200 km/s (chi-squared 54.0 with two fitted parameters).

| Test | Data | Set A | Set B |
|---|---|---|---|
| Early-type galaxies inside the half-light radius | ATLAS3D, 187 galaxies, 36 above threshold | fails, 9 standard errors | fails, 3.4 to 8 |
| Giant spirals | SPARC with Di Teodoro et al. 2021 and 2023, 179 galaxies | fails | passes |
| Groups and clusters at two radii | 51 systems | fails | fails unless a mass bias grows outward |
| Groups and clusters at the outer radius | 63 systems | fails | marginal |

- **Early-type galaxies.** [F] Above the threshold the measured mass inside the half-light radius equals the stellar mass for a Salpeter mix, to within 0.05 dex in every bin. Set A predicts 0.21 to 0.75 dex more. A test that does not depend on the star mix uses galaxies at 120 to 186 km/s as the control. The step falls short of set A by 0.35 ± 0.04 dex and of set B by 0.10 ± 0.03 dex.

  [I] Galaxies sorted by velocity dispersion are pushed toward the model, so the failure is conservative.
- **Giant spirals.** [F] Sorted by speed, the eight fastest SPARC spirals sit 0.10 dex above the standard relation. Sorted by baryonic mass the excess is gone, so the first result is a selection effect. Set A predicts no spirals between about 262 and 435 km/s, and spirals fill that range. Above 1.6e11 solar masses, 55 spirals sit 0.047 dex above the standard line, which set B predicts.

  A bend in the speed-mass line is gentle and sits near 5e10 solar masses, below the model's threshold mass of 2.98e11.
- **The double count.** [F] Set A takes R from the full non-baryonic share at the inner cluster radius and then adds the boost nu on top. That counts the boost twice. Measured the model's own way, R at the inner radius is 4 to 7 per system, not 8.5.
- **Two radii.** [F] The model needs R to be one number. In the same system the residual at the inner radius is 2.1 times that at the outer radius (median of 51). The two agree only if the hydrostatic mass bias at the outer radius exceeds the inner one by about 0.23.

  At the outer radius a threshold form fits better than a constant or a power law in all four treatments, with an onset between 230 and 345 km/s. A threshold of 200 km/s is excluded in three of the four. No system in these samples lies between 200 and 280 km/s.

**What is dead and what survives.**

- Dead: the zero-parameter version (set A), at galaxy scale and at cluster scale.
- Dead: a threshold that falls with redshift, for either set (section 2).
- Dead: extra mass in proportion to the baryons at every radius. Fast galaxies have none inside the half-light radius, and clusters have more at small radii than at large ones.
- Survives: an excess over the standard relation in every massive class of system, growing with baryonic mass. A threshold form fits the groups and clusters with an onset between 230 and 345 km/s. Across all classes a smooth rise fits as well (section 3). [I] This is close to a known result. Modified gravity fits galaxies and falls short in groups and clusters.

**Commands** (from `research/data-tests-20261115/threshold-185/`, after `fetch_sources.py`):

```sh
python3 t0_checks.py                          # sanity and corruption checks
python3 t1_sparc_threshold.py                 # SPARC, outputs t1_sparc_threshold.out
python3 t1b_sparc_by_mass.py
python3 t2_massive_spirals.py
python3 t3_atlas3d.py                         # early-type galaxies
python3 t4_data.py && python3 t4_clusters.py  # groups and clusters
python3 t5_btfr_break.py
python3 -I g185_independent.py ../../..       # separate program: collapse scale and the 60-system test
python3 g185_like_for_like.py                 # the chi-squared grid over R and the threshold
```

`g185_independent.py` is written from the formulas in `CLAIMS.md`. It takes only the 126-row table from `wave7_group_cluster_threshold_audit.py`, because that table is the claim's stated input. It gives 185.59 km/s with the same transfer function and 186.93 with the fuller Eisenstein and Hu form.

**Not verified.** Stars inside the inner cluster radius come from a prescription, not a measurement. The high-redshift tests use a thin-disc approximation at the half-light radius. The bootstrap for the bend has 60 simulations. The SLACS lens sample was not used. The 28 table rows computed from cluster masses with a halo model (`wave7...py:101-119`) were not rebuilt from tables.

## 2. The redshift prediction in issue 6

Issue 6 states that the trapped fraction in a 200 km/s system rises from 0.14 today to 0.67 at redshift 0.5 and 0.88 at redshift 1. This follows from a threshold that falls as the collapse scale does. The test compares the model's dark fraction inside the half-light radius with the measured one for 41 galaxies at redshift 0.66 to 2.45.

**Result.** [F] The measured dark fraction has median 0.25. The standard relation alone predicts 0.21. Set A predicts at least 0.79 for every galaxy. Set B with a falling threshold predicts at least 0.64.

**No galaxy of 41 reaches the set A value, and two reach the set B value.** [F] In a second sample (KMOS3D, 65 galaxies near redshift 0.9 and 46 near 2.2) the mean offset from today's speed-mass line is +0.13 and +0.09 dex. The model's extra term alone would add 0.29 to 0.45 dex for set A and 0.18 to 0.31 for set B.

[I] The falling threshold is the part of the idea that is specific to this repository. These data reject it. For set A to hold, the published baryonic masses would have to be about seven times too large. Set B with the threshold held at 200 km/s predicts a median of 0.37 against 0.25 measured.

```sh
cd research/data-tests-20261115/redshift-prediction && python3 t6_highz_fdm.py   # output t6_highz_fdm.out
```

**Not verified.** The test uses the thin-disc approximation. The two samples come from the same team and are not independent. The dark fraction at the half-light radius is a published quantity that depends on its own modelling.

## 3. The table of 763 systems, the fits and the forced part of the law

`unified-table/unified_table.csv` has one row per system and radius: 663 local rows in six classes, from dwarf galaxies to clusters, and 100 galaxies at redshift 0.6 to 2.5 that are kept apart. `unified_table_columns.txt` defines each column. The extra mass is the mass that must be added to the baryons for the standard relation to give the measured total.

Each law is scored by how well it predicts the total mass, with every class weighted equally. The standard relation alone scores 0.190 dex.

**Result.**

- [F] A law in the measured velocity scale and the radius fits best: extra mass proportional to sigma^4.2 r^0.4, score 0.126 dex. A separately written fit (`unified_check.py`) gives 4.17 and 0.41.
- [F] Three reference laws do worse: a component packed to a fixed phase-space density (0.170), an isothermal halo (0.161) and extra mass in proportion to the baryons (0.174).
- [F] Left free, the onset is as gradual as the fit allows. Its position moves from 55 to 356 km/s with the assumed shape and with a shift of 0.2 dex in stellar masses.
- [F] **The velocity-scale law is partly forced by definition.** The velocity scale is a dynamical quantity. At low accelerations the definition of the extra mass gives, identically, baryons plus extra mass equal to 4 sigma^4/(G a0). With no free parameter that identity reproduces the clusters to 0.05 and 0.10 dex. The exponent near 4 is partly built in.
- [F] **The baryon-only law.** Laws that use the baryons alone cannot be circular. The best is extra mass = 10^10.38 (M_b / 1e11 solar masses)^1.36 solar masses, score 0.148 dex. The exponent is 1.36 with a 95% range of 1.32 to 1.39, above 1 in all 300 resamples. Shuffling the velocity scale within each class gives 0.171.

  A threshold in baryonic mass with the same number of parameters scores 0.147, so the data cannot tell a threshold from a smooth rise.
- [F] A law fitted to galaxies alone predicts the inner regions of clusters, three orders of magnitude up in mass, to 0.03 dex (offset +0.29 before, +0.03 after). It then overshoots at the outer radius (+0.12 before, -0.23 after). A law fitted to clusters puts extra mass into ordinary spirals that they do not have.
- [F] Applied to the 100 high-redshift galaxies with no refit, the baryon-only law gives a median offset of -0.04 dex. The standard relation alone gives +0.01.
- [I] No law in one variable describes all classes and both cluster radii. The shared excess may be a real component or two separate systematic effects that happen to point the same way. The excess in early-type galaxies depends on the assumed star mix. The excess in clusters grows if hydrostatic masses are biased low.

**Commands** (from `research/data-tests-20261115/unified-table/`, after `fetch_sources.py`):

```sh
python3 build_table.py                                   # rebuilds unified_table.csv (needs sources/)
python3 part2b.py                                        # fits, onset position, bootstrap
python3 part2c.py
python3 rank_variables.py && python3 summarize_rank.py   # about 80 seconds
python3 unified_check.py unified_table.csv               # separately written fit
python3 unified_circularity.py unified_table.csv         # the forced part of the law
python3 unified_baryon_law.py unified_table.csv          # the baryon-only law
```

`unified_check.py`, `unified_circularity.py` and `unified_baryon_law.py` read only the saved table and need no download. The other scripts rebuild the table from `sources/` first.

**Not verified.** The stellar mass inside the cluster radii, the assumed errors (listed in `NOTES.md`) and the assumed radii of the giant spirals are inputs of the table, not measurements. The best-fit onset is set by the assumed sharpness. The law is not a physical model.

## 4. The four speeds near 185 km/s, with honest ranges

Claim C-27 compares four speeds: the collapse scale, the knee of the galaxy mass function, a cooling scale and the onset in the data. `four-speeds/coincidence_audit.py` varies each over choices that a careful author could defend. It uses the repository's own Wave 10 script, imported without change, for the collapse and cooling scales.

| Speed | Repository value | Range from defensible choices |
|---|---|---|
| Collapse scale | 185.59 | 141 to 261 km/s |
| Knee of the galaxy mass function | 175.82 | 152 to 221 km/s |
| Cooling scale | 178.42 | 89 to 446 km/s |
| Onset in the data | 180 to 190 | 95 to 356 km/s |

**Result.** [F] The chance that four speeds drawn independently between 30 and 1,500 km/s land as close as the repository's values is about 1 in 100,000. With the ranges above it is about 2% (0.4% to 5%). With wider but still defensible ranges it is about 6%. [F] The cooling scale is linear in an overdensity that the script sets to 1,000.

The knee speed is a rotation speed and the others are dispersions. As a dispersion it would be 107 to 157 km/s. [I] The collapse scale and the cooling scale are both built from the critical density and the Hubble time. The largest galaxies sit where gas stops cooling within the age of the universe, a standard result. There are about two independent scales, not four.

```sh
cd research/data-tests-20261115/four-speeds && python3 coincidence_audit.py   # output coincidence_audit.out
```

**Not verified.** The ranges are choices made in the script and listed in the output. The onset range uses the fits in sections 1 and 3, which depend on the assumptions listed there.

## 5. The acceleration scale and the expansion rate

The folder `acceleration-evolution/` sets up `a0(z) = A E(z)^q` and stops before fitting data. This section does the fit, with p in place of q. The data are 100 star-forming galaxies at redshift 0.6 to 2.5 (Nestor Shachar et al. 2023, Table 3, typed in by hand, see `data/rc100_table3.csv`).

For each galaxy the rotation speed at the half-light radius is predicted from the published baryonic mass and size, and compared with the measured speed.

**Result: undecided.** The one like-for-like fit that could be done leans against the hypothesis. The lean does not survive plausible errors in the masses.

| Treatment of A | Best p | 95% range | How much worse p = 1 fits (-2 ln L) |
|---|---|---|---|
| Fixed at 1.2e-10 | 0.10 | -0.25 to 0.40 | 32.8 |
| Within 20% of 1.2e-10 | -0.01 | -0.50 to 0.45 | 18.4 |
| Free | -0.74 | -1.8 to 0.25 | 9.8 |

- [F] In four redshift bins the fitted scale is 1.82, 1.51, 1.15 and 1.26 in units of 1e-10 at redshift 0.81, 1.41, 2.11 and 2.30. The hypothesis predicts 1.92, 2.71, 3.83 and 4.16.
- [F] If baryonic masses are biased low by 0.2 dex per unit of redshift, the preference flips to p near 1.2. If the correction for pressure support is 1.5 times the published one, the preference for a constant scale shrinks to about 4. About half the baryonic mass is gas, and the gas masses come from scaling relations.
- [F] The median baryonic acceleration at the half-light radius is 1.6 times a0, so the sample does reach the regime where the scale matters. The limit is systematic error, not lack of signal.
- [F] The per-galaxy data of the 79-galaxy sample named in `acceleration-evolution/evidence.json` could not be retrieved. At summary level its fitted lines correspond to p between 1.0 and 1.15.
- [F] The three ratios in `acceleration-evolution/comparison.json` (1.9207, 2.1575 and 1.9341) are reproduced by separate exact code (`repro_repo_numbers.py`).

**What would decide it.** Outer rotation speeds where the baryonic acceleration is below 0.3 a0, for 50 to 100 discs each near redshift 1 and 2, with measured gas masses and stellar masses from the same method used locally. The hypothesis predicts a shift of the speed-mass line of -0.25 dex in mass at redshift 1 and -0.48 at redshift 2.

Mass errors that drift with redshift must be below about 0.08 dex.

```sh
cd research/data-tests-20261115/acceleration-evolution-fit
python3 theory_numbers.py && python3 muse_summary.py && python3 repro_repo_numbers.py   # outputs/*.txt
python3 check_transcription.py data/rc100_table3.csv                                   # flags 0
python3 ubler_bound.py ../sources/from_accel/ubler2017_vizier.tsv ubler_bound.json
python3 rc100_fit.py data/rc100_table3.csv outputs/rc100_fit.json > outputs/rc100_fit.txt   # about 6 minutes
```

**Not verified.** No test with injected signals was run, so the fit's ability to recover a known p is assumed. The two samples used come from the same team. The baryon model is a thin disc with one global thickness factor. The table was typed from an image of the paper.

Two readings agreed on 1,295 of 1,300 cells and the five differences were resolved on enlarged images (`xcheck/rc100_xcheck.csv`, `outputs/xcheck_diff.txt`). The zoomed page images used for that are not included. The saved fit output is reproduced byte for byte by `check.py --full`.

This work sits beside the `acceleration-evolution/` folder and not in it. That folder's CI checks its own `results.json`, and its README states that it makes no fit to galaxy data. Nothing in `acceleration-evolution/` is changed.

## 6. A light particle in clusters, and a woven picture (CONJECTURE)

**Everything in this section beyond the first part is a conjecture, not a result.** The first part tests a published-style idea against the table of section 3. The second part, `woven-hypothesis/`, writes down one picture that the threads fit into, with numbers and a list of what would kill it.

**The question.** The table of section 3 scored a law in which a particle is packed to its maximum density everywhere, and that law did badly. A real halo of fermions is packed only in its core. The study asks where a neutrino-like particle fails to line up with the data and what could explain each mismatch. The sample is 51 groups and clusters.

**Result.**

1. [F] The extra mass falls with radius in 41 of 51 systems (median ratio 0.58, negative at the outer radius in 8). No mass component can do that.
2. [F] The mean extra density inside the inner radius sets a lower limit on the particle mass of 1.6 to 2.8 eV for two spin states, rising toward cooler systems.
3. [F] A species with the full thermal abundance and mass m supplies m / 2.084 eV times the baryons. Inside the outer radius the median system holds the equivalent of 1.2 eV and the six richest hold 3.3 eV. An 11 eV species would supply 11 eV.
4. [F] Early-type galaxies and giant spirals sit 0.08 dex above the standard relation inside a few kiloparsecs. The packing limit allows a 12 eV particle to supply under 1% of that. [I] A stellar mass-to-light ratio 0.135 dex higher accounts for it, which lies between the two usual choices.

**The correction on external fields.** [F] An earlier halo study reported that an external field of 0.05 a0 closes the radial mismatch almost alone. In the formula it used, the field entered is the Newtonian one. A Newtonian field of 0.05 a0 is a physical field of 0.25 a0, which is larger than a cluster's own field at the outer radius.

`n3_efe_check.py` restates everything in physical fields and reproduces the earlier numbers at 0.10 and 0.25 a0. With physical fields of plausible size (0.03 a0) and a mass shortfall of 10% inside and 31% outside, the extra mass stops falling in 98% of systems. With no shortfall, only 33%. [I] The size of the shortfall at the outer radius is the most important unknown.

**What published work says against it.** [P] Simulations of modified gravity with 11 eV neutrinos produce too many very rich clusters and too few poor ones (arXiv:1104.5040, 1309.6094). A 2026 study excludes the combination at more than five standard errors (arXiv:2602.21975).

A fully thermal 11 eV species adds about one light species, and the standard analysis of the microwave background allows 2.99 ± 0.17 (arXiv:1807.06209), under the standard cold-matter model.

**The woven picture (`woven-hypothesis/fabric_numbers.py`).** [C] Gravity in galaxies follows the standard relation with one acceleration scale. One new light fermion of about 11 eV, populated at three quarters of the thermal level, is capped by the exclusion principle in cluster cores and outer galaxy halos.

It predicts extra mass of about half the baryons inside 300 kpc of an isolated galaxy, a ratio of extra mass to baryons that levels off near 4.0 in the richest clusters, and a core density that cannot exceed about 2.0e8 solar masses per cubic kiloparsec at 8 keV.

[C] What would kill it: lensing around isolated galaxies with errors halved that finds less than about 0.2 times the baryons inside 300 kpc, a cluster core denser than the cap, or an X-ray mass shortfall near 6% at the outer radius. [I] Taken at face value, the light-species count at recombination disfavours the central case by four standard errors.

That analysis assumes the standard cold-matter model, so the test is a re-analysis without it.

It is a hypothesis about what the missing mass in clusters might be. It is not a theory of gravity and not a unification.

```sh
cd research/data-tests-20261115/neutrino-like-conjecture
for n in n1_bounds n2_bias_scan n3_efe_check n4_window; do python3 $n.py ../unified-table/unified_table.csv; done
python3 check_numbers.py
(cd model && python3 m1_requirements.py && python3 m2_radial.py && python3 m3_fermion_halo.py && python3 m3b_decompose.py && python3 m5_galaxies.py && python3 m5b_lensing_mmax.py)
python3 woven-hypothesis/fabric_numbers.py
```

The scripts in `model/` need `sources/`. The scripts that start with `n` read only the table.

**Not verified.** The halo profiles are simple curves through two radii. The external field is treated with a one-dimensional formula. The temperature trend under the halo model was not checked against published temperature profiles. The factor of three in the printed packing-limit formula comes from arithmetic on the published formulas and was not checked with the authors.

Whether a species populated below the thermal level forms structure acceptably has not been simulated. The published values marked [P] were read from the cited papers and are not re-derived here.

## Tables typed in from papers

| Where | What | Source line |
|---|---|---|
| `acceleration-evolution-fit/data/rc100_table3.csv` | 100 galaxies, 1,300 cells | Nestor Shachar et al. 2023, ApJ 944, 78, arXiv:2209.12199, Appendix B, Table 3. The header of the file gives the pages and the date. |
| `redshift-prediction/t6_highz_fdm.py` (`Z`, `VC_T1`) | redshift and circular speed of 41 galaxies | Genzel et al. 2020, ApJ 902, 98, arXiv:2006.03046, Table 1. Used to check that each parsed row of Table D1 is the right galaxy. |
| `neutrino-like-conjecture/model/m5_galaxies.py` (`T2`) | 11 lensing bins | Mistele et al. 2024, ApJL 969, L3, arXiv:2406.09685, Table 2. |
| `threshold-185/t4_systems.json` | 68 cluster and group rows | Parsed by `t4_data.py` from the TeX of Vikhlinin et al. 2006 (astro-ph/0507092), Sun et al. 2009 (0805.2320), Lovisari et al. 2015 (1409.3845) and Gonzalez et al. 2013 (1309.3565). |
| `unified-table/unified_table.csv` | 763 rows | Built by `build_table.py` from the sources in [SOURCES.md](SOURCES.md). The `src` column names the source of each row. |

## Not in this folder

The downloaded tables and papers. Any change to a claim label or to `CLAIMS.md`. Any change to `index.html` or the Lean files. A fit of the full SPARC sample for `d_s`, which issue 1 asks for.
