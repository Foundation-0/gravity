#!/usr/bin/env python3
"""Re-run the programs in this folder in a temporary copy and compare every result with the saved file.

From the repository root:
    python3 research/data-tests-20261115/check.py            # all but the 6-minute fit
    python3 research/data-tests-20261115/check.py --full     # also the acceleration-evolution fit
    python3 -O research/data-tests-20261115/check.py         # the same, with the programs run under -O

The committed files are never written. The programs that read published tables need `sources/`
(run `python3 fetch_sources.py` first). Without it those jobs are reported as SKIPPED and the exit
status is 3. Every comparison is an explicit test that raises, so `-O` does not weaken it.
Needs numpy and scipy (python-flint for one job), see requirements.txt.
Exit status: 0 all compared files identical, 1 a difference or a failed run, 3 jobs skipped.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
NAME = HERE.name
OPT = ["-O"] if sys.flags.optimize else []
FULL = "--full" in sys.argv

# Each job: name, working directory (inside the folder), script, args,
#   compare = list of (kind, committed file) with kind "stdout" (program output) or "file" (file the program writes)
#   src = needs sources/, slow = only with --full, repo = path of the repository root is the first argument
JOBS = [
    ("t0 sanity and corruption checks", "threshold-185", "t0_checks.py", [], [("stdout", "t0_checks.out")], True, False, False),
    ("t1 SPARC galaxies against the threshold", "threshold-185", "t1_sparc_threshold.py", [], [("stdout", "t1_sparc_threshold.out")], True, False, False),
    ("t1b SPARC by baryonic mass", "threshold-185", "t1b_sparc_by_mass.py", [], [("stdout", "t1b_sparc_by_mass.out")], True, False, False),
    ("t2 giant spirals", "threshold-185", "t2_massive_spirals.py", [], [("stdout", "t2_massive_spirals.out")], True, False, False),
    ("t3 early-type galaxies (ATLAS3D)", "threshold-185", "t3_atlas3d.py", [], [("stdout", "t3_atlas3d.out")], True, False, False),
    ("t4 cluster tables from the TeX sources", "threshold-185", "t4_data.py", [], [("file", "t4_systems.json")], True, False, False),
    ("t4 groups and clusters at two radii", "threshold-185", "t4_clusters.py", [], [("file", "t4_clusters.out")], True, False, False),
    ("t5 speed-mass line break", "threshold-185", "t5_btfr_break.py", [], [("file", "t5_btfr_break.out")], True, False, False),
    ("independent collapse scale and 60-system test", "threshold-185", "g185_independent.py", ["@repo"], [("stdout", "g185_independent.out")], False, False, True),
    ("like-for-like chi-squared grid", "threshold-185", "g185_like_for_like.py", ["@repo"], [("stdout", "g185_like_for_like.out")], False, False, True),
    ("t6 high-redshift galaxies, the issue 6 prediction", "redshift-prediction", "t6_highz_fdm.py", [], [("file", "t6_highz_fdm.out")], True, False, False),
    ("unified table", "unified-table", "build_table.py", [], [("file", "unified_table.csv"), ("stdout", "build_table.out")], True, False, False),
    ("unified fit, separate code", "unified-table", "unified_check.py", ["unified_table.csv"], [("stdout", "unified_check.out")], False, False, False),
    ("unified fit, circularity", "unified-table", "unified_circularity.py", ["unified_table.csv"], [("stdout", "unified_circularity.out")], False, False, False),
    ("unified fit, baryon-only law", "unified-table", "unified_baryon_law.py", ["unified_table.csv"], [("stdout", "unified_baryon_law.out")], False, False, False),
    ("unified fits and onset position", "unified-table", "part2b.py", [], [("file", "part2b.out")], True, False, False),
    ("unified fits, extra checks", "unified-table", "part2c.py", [], [("file", "part2c.out")], True, False, False),
    ("unified variable ranking", "unified-table", "rank_variables.py", [], [], True, False, False),
    ("unified variable ranking, summary", "unified-table", "summarize_rank.py", [], [("file", "summarize_rank.out")], True, False, False),
    ("four-speed coincidence audit", "four-speeds", "coincidence_audit.py", [], [("file", "coincidence_audit.out")], False, False, False),
    ("acceleration scale, theory numbers", "acceleration-evolution-fit", "theory_numbers.py", [], [("stdout", "outputs/theory_numbers.txt")], False, False, False),
    ("acceleration scale, published summaries", "acceleration-evolution-fit", "muse_summary.py", [], [("stdout", "outputs/muse_summary.txt")], False, False, False),
    ("acceleration scale, repository numbers", "acceleration-evolution-fit", "repro_repo_numbers.py", [], [("stdout", "outputs/repro_repo_numbers.txt")], False, False, False),
    ("acceleration scale, KMOS3D bound", "acceleration-evolution-fit", "ubler_bound.py", ["../sources/from_accel/ubler2017_vizier.tsv", "ubler_bound.json"],
     [("stdout", "outputs/ubler_bound.txt"), ("file", "outputs/ubler_bound.json")], True, False, False),
    ("acceleration scale, transcription check", "acceleration-evolution-fit", "check_transcription.py", ["data/rc100_table3.csv"], [], False, False, False),
    ("acceleration scale, 100-galaxy fit (about 6 minutes)", "acceleration-evolution-fit", "rc100_fit.py", ["data/rc100_table3.csv", "outputs/rc100_fit.json"],
     [("stdout", "outputs/rc100_fit.txt"), ("file", "outputs/rc100_fit.json")], False, True, False),
    ("neutrino-like, bounds", "neutrino-like-conjecture", "n1_bounds.py", ["../unified-table/unified_table.csv"], [("stdout", "n1_bounds.out")], False, False, False),
    ("neutrino-like, bias scan", "neutrino-like-conjecture", "n2_bias_scan.py", ["../unified-table/unified_table.csv"], [("stdout", "n2_bias_scan.out")], False, False, False),
    ("neutrino-like, external field in physical units", "neutrino-like-conjecture", "n3_efe_check.py", ["../unified-table/unified_table.csv"], [("stdout", "n3_efe_check.out")], False, False, False),
    ("neutrino-like, mass and population window", "neutrino-like-conjecture", "n4_window.py", ["../unified-table/unified_table.csv"], [("file", "n4_window.out")], False, False, False),
    ("neutrino-like, arithmetic checks", "neutrino-like-conjecture", "check_numbers.py", [], [("stdout", "check_numbers.out")], False, False, False),
    ("halo study 1", "neutrino-like-conjecture/model", "m1_requirements.py", [], [("file", "m1_requirements.out"), ("file", "m1_requirements.csv")], True, False, False),
    ("halo study 2", "neutrino-like-conjecture/model", "m2_radial.py", [], [("file", "m2_radial.out")], True, False, False),
    ("halo study 3", "neutrino-like-conjecture/model", "m3_fermion_halo.py", [], [("file", "m3_fermion_halo.out")], True, False, False),
    ("halo study 3b", "neutrino-like-conjecture/model", "m3b_decompose.py", [], [("file", "m3b_decompose.out")], True, False, False),
    ("halo study 5", "neutrino-like-conjecture/model", "m5_galaxies.py", [], [("file", "m5_galaxies.out")], False, False, False),
    ("halo study 5b", "neutrino-like-conjecture/model", "m5b_lensing_mmax.py", [], [("file", "m5b_lensing_mmax.out")], False, False, False),
    ("woven hypothesis numbers", "neutrino-like-conjecture/woven-hypothesis", "fabric_numbers.py", [], [("stdout", "fabric_numbers.out")], False, False, False),
]

# Corruption tests: the program must fail on the changed input. (name, directory, script, file to change, old text, new text, args)
CORRUPT = [
    ("a changed speed error in the transcribed table", "acceleration-evolution-fit", "check_transcription.py", "data/rc100_table3.csv", ",286,57,30,7,8.66", ",236,57,30,7,8.66", ["data/rc100_table3.csv"]),
    ("a changed error in the transcribed table", "acceleration-evolution-fit", "check_transcription.py", "data/rc100_table3.csv", ",6.49,1.48,0.53,0.09", ",6.49,1.48,0.35,0.09", ["data/rc100_table3.csv"]),
    ("a changed mass in the transcribed table", "acceleration-evolution-fit", "check_transcription.py", "data/rc100_table3.csv", ",9.15,0.52,7.61,1.31", ",9.15,0.52,4.61,1.31", ["data/rc100_table3.csv"]),
    ("a repository number changed by 5e-12 relative", "acceleration-evolution-fit", "repro_repo_numbers.py", "repro_repo_numbers.py", "2.1575391880369907", "2.157539188046991", []),
]


def fail(msg):
    raise SystemExit("CHECK FAILED: " + msg)


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    have_src = (HERE / "sources" / "sparc" / "SPARC_Lelli2016c.mrt").is_file()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="data-tests-"))
    try:
        # A repository-shaped copy: the wave scripts at its root, this folder under research/.
        for p in REPO.glob("wave*.py"):
            shutil.copy(p, tmp / p.name)
        work = tmp / "research" / NAME
        shutil.copytree(HERE, work, ignore=shutil.ignore_patterns("__pycache__"))
        skipped, bad, done = [], [], 0
        for name, d, script, args, compare, src, slow, repo in JOBS:
            if slow and not FULL:
                skipped.append(name + " (--full)"); continue
            if src and not have_src:
                skipped.append(name + " (needs sources/)"); continue
            cwd = work / d
            argv = [str(tmp) if a == "@repo" else a for a in args]
            t0 = time.time()
            r = run([sys.executable, *OPT, script, *argv], cwd)
            if r.returncode != 0:
                bad.append(name); print(f"FAIL  {name}: exit {r.returncode}\n{r.stderr[-300:]}"); continue
            ok = True
            for kind, rel in compare:
                got = r.stdout.encode() if kind == "stdout" else (cwd / rel).read_bytes()
                want = (HERE / d / rel).read_bytes()
                if got != want:
                    ok = False; print(f"DIFF  {name}: {rel} differs from the saved file")
            if ok:
                done += 1; print(f"OK    {name} ({time.time() - t0:.0f} s)")
            else:
                bad.append(name)
        for name, d, script, rel, old, new, args in CORRUPT:
            f = work / d / rel
            text = f.read_text()
            if old not in text:
                fail(f"corruption test text not found: {name}")
            f.write_text(text.replace(old, new, 1))
            r = run([sys.executable, *OPT, script, *args], work / d)
            f.write_text(text)
            if r.returncode == 0:
                bad.append("corruption accepted: " + name); print(f"FAIL  corruption accepted: {name}")
            else:
                done += 1; print(f"OK    rejected {name}")
        print(f"\n{done} passed, {len(bad)} failed, {len(skipped)} skipped")
        for s in skipped:
            print("SKIPPED", s)
        if bad:
            fail("; ".join(bad))
        return 3 if any("sources/" in s for s in skipped) else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
