# Scales probe

These calculations test scaling assumptions and sensitivity in ideal models. The collapse calculation reuses the pinned approximate gravity power spectrum in `../../inputs/`, rather than independently validating that approximation.

Run from the repository root:

```sh
python3 research/convergences-20261112/probes/scales/scale_probes.py
```

This rewrites `results.json` beside the script. Use the bundle command `python3 research/convergences-20261112/check.py` to regenerate in a temporary directory and verify all saved numerical results.
