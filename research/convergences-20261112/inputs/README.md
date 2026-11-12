# Historical gravity inputs

These files preserve the gravity calculations used by the scales and robustness probes. They are exact copies from [Foundation-0/gravity at d8c7544](https://github.com/Foundation-0/gravity/tree/d8c7544e89388720fc1c13de816ddb7dd03d2096). `manifest.json` records each upstream path and SHA-256 digest.

- `wave10_covariant_jeans_unification.py` supplies the approximate Eisenstein-Hu power spectrum and fixed cosmology used by the scales probe.
- `wave7_group_cluster_threshold_audit.py` is the wave10 module's import dependency. Its catalog fitting routines are not called by these probes.
- `wave10_covariant_jeans_certificates.json` supplies the previously computed collapse-dispersion trajectory used by the robustness probe. That column is a reused calculation, not an independent recomputation.

The module headers retain their original attribution. The upstream code is Apache-2.0 and the results are CC-BY-4.0, as stated in those headers. The certificate is retained whole so its original digest remains verifiable. The checker verifies every digest before running the probes. It never substitutes current repository data for these historical files.
