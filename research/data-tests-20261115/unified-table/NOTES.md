# Notes on building the unified table

- An early version of `threshold-185/t3_atlas3d.py` read the distance from the wrong column (M_K instead of D) of ATLAS3D paper I Table 3. It is fixed. The conclusions of the early-type test did not change: step test A -0.351 +/- 0.039 (9.1 sigma), B -0.104 +/- 0.030 (3.4 sigma).
- The 41-galaxy sample of Genzel et al. 2020 is not a separate class. At least 31 of its 41 galaxies are in the 100-galaxy sample of Nestor Shachar et al. 2023, which is used here.
- Assumed errors: SPARC M_b 0.1 dex times the stellar share, giant spirals 0.2 dex, ATLAS3D M_tot 0.05 and M_b 0.10 dex, cluster stars 30%.
- The giant-spiral radii are not tabulated. The table uses r = 3 R_d with R_d = j*/(2 V_flat) and M_b(<r) = 0.8 M_b. The `sel` column flags this.
- Fit score: class-balanced mean square of log10(M_tot observed / M_tot predicted). Each local class has equal weight.
- Threshold sharpness is bounded to s in (0.5, 6). Free fits sit at s = 0.5 (soft onset), so the position of a "threshold" depends on s.
- Multiprocessing on macOS re-imports `part2b.py` in the workers, so a console log of that script repeats section (1). The saved `part2b.out` is clean.
- The collapse and cooling scales in `../four-speeds/` use the repository's own Wave 10 script, imported from the repository root without change.
- The KATRIN bound m_nu < 0.45 eV (90% CL), arXiv:2406.13516, is quoted from memory and was not re-fetched.
