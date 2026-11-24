# Sources read by the programs

`fetch_sources.py` downloads these into `sources/` (ignored by git). All were read on 2026-11-15. Nothing downloaded is stored in the repository. Files are kept only if the program needs them. The TeX sources are the arXiv e-print at the version current on that date.

| File in `sources/` | Address | What it is | Read by |
|---|---|---|---|
| `sparc/SPARC_Lelli2016c.mrt` | https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt | SPARC galaxy table (Lelli, McGaugh and Schombert 2016, AJ 152, 157) | `threshold-185/t1`, `t1b`, `t2`, `t5`, `unified-table/build_table.py` |
| `sparc/MassModels_Lelli2016c.mrt` | https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt | SPARC mass models, rotation-curve points | `threshold-185/t1`, `t1b`, `unified-table/build_table.py` |
| `atlas3d/Cappellari2011a_Atlas3D_Paper1_Table3.txt` | https://groups.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt | ATLAS3D sample, distances (Cappellari et al. 2011, MNRAS 413, 813) | `threshold-185/t3`, `unified-table/build_table.py` |
| `atlas3d/Cappellari2013a_Atlas3D_Paper15_Table1.txt` | https://groups.physics.ox.ac.uk/atlas3d/tables/Cappellari2013a_Atlas3D_Paper15_Table1.txt | ATLAS3D scaling relations and dynamical models (Cappellari et al. 2013a, MNRAS 432, 1709) | same |
| `atlas3d/Cappellari2013b_Atlas3D_Paper20_Table1.txt` | https://groups.physics.ox.ac.uk/atlas3d/tables/Cappellari2013b_Atlas3D_Paper20_Table1.txt | ATLAS3D mass-size and mass-sigma data (Cappellari et al. 2013b, MNRAS 432, 1862) | same |
| `arxiv-2109.03828/paper_ss.tex` | https://arxiv.org/e-print/2109.03828 | Di Teodoro et al. 2021, extremely massive spirals, Table 1 | `threshold-185/t2`, `t5`, `build_table.py` |
| `arxiv-2207.02906/paper_ssvla.tex`, `table_dyn.tex` | https://arxiv.org/e-print/2207.02906 | Di Teodoro et al. 2023, "Dark Matter Halos and Scaling Relations of Extremely Massive Spiral Galaxies from Extended HI Rotation Curves", sample and dynamics tables | `threshold-185/t5`, `build_table.py` |
| `arxiv-1909.09080/pogle.tex` | https://arxiv.org/e-print/1909.09080 | Ogle et al. 2019, "A Break in Spiral Galaxy Scaling Relations at the Upper Limit of Galaxy Mass", table | `threshold-185/t5` |
| `arxiv-astro-ph_0507092/mprof.tex` | https://arxiv.org/e-print/astro-ph/0507092 | Vikhlinin et al. 2006, "Chandra sample of nearby relaxed galaxy clusters", table of masses | `threshold-185/t4_data.py`, `neutrino-like-conjecture/model/m_data.py` |
| `arxiv-0805.2320/ms.tex` | https://arxiv.org/e-print/0805.2320 | Sun et al. 2009, "Chandra studies of the X-ray gas properties of galaxy groups", Table 3 | same |
| `arxiv-1409.3845/Lovisari_groups.tex` | https://arxiv.org/e-print/1409.3845 | Lovisari et al. 2015, "Scaling properties of a complete X-ray selected galaxy group sample" | same |
| `arxiv-1309.3565/ms.tex` | https://arxiv.org/e-print/1309.3565 | Gonzalez et al. 2013, "Galaxy Cluster Baryon Fractions Revisited" | same |
| `from_accel/rc41_2006.03046.txt` | https://arxiv.org/pdf/2006.03046, `pdftotext -layout` | Genzel et al. 2020, rotation curves at redshift 1 to 2, Tables 1 and D1 | `redshift-prediction/t6`, `threshold-185/t0` |
| `from_accel/ubler2017_vizier.tsv` | https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/842/121&-out.max=unlimited&-out.all | Ubler et al. 2017, KMOS3D Tully-Fisher sample, VizieR table J/ApJ/842/121/table3 | `redshift-prediction/t6`, `acceleration-evolution-fit/ubler_bound.py` |

The VizieR file starts with comment lines that carry the date of the request. The programs skip them. The ATLAS3D files were first read from `www-astro.physics.ox.ac.uk/atlas3d/`, which now redirects to the address above. The bytes are the same.

The one hand-typed table, the 100 galaxies of Nestor Shachar et al. 2023 (arXiv:2209.12199, Appendix B, Table 3), is in `acceleration-evolution-fit/data/rc100_table3.csv` with its source line. The values marked [P] in the neutrino-like study (limits on neutrino mass and on the number of light species, simulation results) are read from the papers named in the text and are not used by a program.
