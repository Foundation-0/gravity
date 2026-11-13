"""Optional scientific figure. Install the pinned plot requirements to regenerate."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import FIDUCIAL_A, expansion
from compare import comparison_document

ROOT = Path(__file__).resolve().parent
matplotlib.rcParams.update({"font.size": 10, "svg.hashsalt": "gravity-acceleration-evolution-v1"})
evidence = json.loads((ROOT / "evidence.json").read_text())
comparison = comparison_document()
lo, hi = comparison["interval"]


def grid(start, end, n=250):
    return [start + (end - start) * i / (n - 1) for i in range(n)]


fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2))
fig.patch.set_facecolor("#fafaf7")
for ax in axes:
    ax.set_facecolor("#fafaf7")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.16)
    ax.set_xlabel("Redshift z  (earlier epochs to the right)")

left, right = axes
left.axvspan(lo, hi, color="#e4e9ef", alpha=0.7, label="MUSE sample range")
left.axhline(FIDUCIAL_A / 1e-10, color="#72767e", lw=2, ls="--", label="Constant benchmark")
for start, end, style in ((0, lo, ":"), (lo, hi, "-"), (hi, 3, ":")):
    x = grid(start, end)
    left.plot(x, [FIDUCIAL_A * expansion(z) / 1e-10 for z in x], color="#165fba", lw=2.6,
              ls=style, label="H tracking; A = 1.2" if start == lo else None)

x = grid(lo, hi)
right.plot(x, [1.0] * len(x), color="#72767e", lw=2, ls="--", label="Constant")
right.plot(x, [expansion(z) / expansion(lo) for z in x], color="#165fba", lw=2.6, label="H tracking")
for item, color, label in zip(evidence["published_linear_curves"], ("#a43b6a", "#2a8a64"),
                              ("Published DC14 curve", "Published MOND curve")):
    a, b = item["intercept_m_s2"], item["slope_m_s2_per_redshift"]
    left.plot(x, [(a + b * z) / 1e-10 for z in x], color=color, lw=2, label=label)
    right.plot(x, [(a + b * z) / (a + b * lo) for z in x], color=color, lw=2, label=label)

left.set(xlim=(0, 3), ylim=(0.7, 5.8), ylabel="Acceleration scale  [10⁻¹⁰ m s⁻²]",
         title="Fixed local benchmark normalization")
right.set(xlim=(lo, hi), ylim=(0.95, 2.25), ylabel="Scale divided by its value at z = 0.33",
          title="Shape comparison within the sample")
left.legend(loc="upper left", frameon=False, fontsize=8.5)
right.legend(loc="upper left", frameon=False, fontsize=8.5)
fig.suptitle("Does the galactic acceleration scale track expansion?", x=0.07, ha="left", fontsize=16, fontweight="bold")
fig.text(0.07, 0.05, "Pending independent reproduction. Published curves: Ciocan et al. (2026), Eqs. 4 and 14; same 79 galaxies. No new data fit or confidence bands.", fontsize=9)
fig.text(0.07, 0.015, "Flat matter + Λ background, Ωm = 0.315. Dotted H-tracking segments are forecasts outside the sample.", fontsize=9, color="#555c64")
fig.tight_layout(rect=(0.02, 0.085, 0.995, 0.93))
fig.savefig(ROOT / "comparison.png", dpi=170, metadata={"Software": "matplotlib"})
fig.savefig(ROOT / "comparison.svg", metadata={"Date": None, "Creator": "gravity acceleration-evolution plot.py"})
svg = ROOT / "comparison.svg"
svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
plt.close(fig)
print("wrote comparison.png and comparison.svg")
