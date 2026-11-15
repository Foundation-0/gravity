#!/usr/bin/env python3
"""Fetch the published tables that the programs in this folder read, into ./sources/.

Python standard library, plus `curl` and, for one PDF, `pdftotext` (poppler). Nothing here is stored in the repository:
sources/ is ignored by git. See SOURCES.md for what each file is, where it comes from and the date it was read.

Usage:  python3 fetch_sources.py            # fetch what is missing
        python3 fetch_sources.py --list     # print the table of files and addresses
One request per 1.5 s. Existing files are kept.
"""
import gzip
import io
import pathlib
import shutil
import subprocess
import sys
import tarfile
import time

ROOT = pathlib.Path(__file__).resolve().parent / "sources"

PLAIN = [  # (relative path, address)
    ("sparc/SPARC_Lelli2016c.mrt", "https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt"),
    ("sparc/MassModels_Lelli2016c.mrt", "https://astroweb.case.edu/SPARC/MassModels_Lelli2016c.mrt"),
    ("atlas3d/Cappellari2011a_Atlas3D_Paper1_Table3.txt",
     "https://groups.physics.ox.ac.uk/atlas3d/tables/Cappellari2011a_Atlas3D_Paper1_Table3.txt"),
    ("atlas3d/Cappellari2013a_Atlas3D_Paper15_Table1.txt",
     "https://groups.physics.ox.ac.uk/atlas3d/tables/Cappellari2013a_Atlas3D_Paper15_Table1.txt"),
    ("atlas3d/Cappellari2013b_Atlas3D_Paper20_Table1.txt",
     "https://groups.physics.ox.ac.uk/atlas3d/tables/Cappellari2013b_Atlas3D_Paper20_Table1.txt"),
    ("from_accel/ubler2017_vizier.tsv",
     "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/842/121&-out.max=unlimited&-out.all"),
]
# arXiv e-print archives: (directory name, arXiv identifier, members to keep)
EPRINT = [
    ("arxiv-2109.03828", "2109.03828", ["paper_ss.tex"]),
    ("arxiv-2207.02906", "2207.02906", ["paper_ssvla.tex", "table_dyn.tex"]),
    ("arxiv-1909.09080", "1909.09080", ["pogle.tex"]),
    ("arxiv-astro-ph_0507092", "astro-ph/0507092", ["mprof.tex"]),
    ("arxiv-0805.2320", "0805.2320", ["ms.tex"]),
    ("arxiv-1409.3845", "1409.3845", ["Lovisari_groups.tex"]),
    ("arxiv-1309.3565", "1309.3565", ["ms.tex"]),
]
PDF = ("from_accel/rc41_2006.03046.txt", "https://arxiv.org/pdf/2006.03046")


def get(url):
    """Download with curl, which uses the system certificate store (certificates are always verified)."""
    r = subprocess.run(["curl", "-fsSL", "--max-time", "180", "-A", "research-script", url], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl exit {r.returncode}: {r.stderr.decode(errors='replace').strip()[:200]}")
    return r.stdout


def main():
    if "--list" in sys.argv:
        for rel, url in PLAIN:
            print(f"{rel}\t{url}")
        for d, ident, members in EPRINT:
            print(f"{d}/{','.join(members)}\thttps://arxiv.org/e-print/{ident}")
        print(f"{PDF[0]}\t{PDF[1]} (pdftotext -layout)")
        return 0
    failed = []
    jobs = []
    jobs += [("plain", rel, url) for rel, url in PLAIN]
    jobs += [("eprint", d, (ident, members)) for d, ident, members in EPRINT]
    jobs += [("pdf", PDF[0], PDF[1])]
    for kind, rel, arg in jobs:
        try:
            if kind == "plain":
                dest = ROOT / rel
                if dest.exists() and dest.stat().st_size > 0:
                    print("kept", rel); continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(get(arg)); print("fetched", rel)
            elif kind == "eprint":
                ident, members = arg
                dest = ROOT / rel
                if all((dest / m).exists() for m in members):
                    print("kept", rel); continue
                raw = get(f"https://arxiv.org/e-print/{ident}")
                dest.mkdir(parents=True, exist_ok=True)
                try:
                    tf = tarfile.open(fileobj=io.BytesIO(raw), mode="r:*")
                    names = {pathlib.PurePosixPath(n).name: n for n in tf.getnames()}
                    for m in members:
                        (dest / m).write_bytes(tf.extractfile(names[m]).read())
                except tarfile.ReadError:  # a single gzipped TeX file
                    (dest / members[0]).write_bytes(gzip.decompress(raw))
                print("fetched", rel, members)
            else:
                dest = ROOT / rel
                if dest.exists() and dest.stat().st_size > 0:
                    print("kept", rel); continue
                if not shutil.which("pdftotext"):
                    raise RuntimeError("pdftotext not found")
                dest.parent.mkdir(parents=True, exist_ok=True)
                tmp = dest.with_suffix(".pdf")
                tmp.write_bytes(get(arg))
                subprocess.run(["pdftotext", "-layout", str(tmp), str(dest)], check=True)
                tmp.unlink(); print("fetched", rel)
        except Exception as e:  # report and go on
            failed.append(rel); print("ERROR", rel, repr(e))
        time.sleep(1.5)
    if failed:
        print("FAILED:", ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
