# Independent review of closure and observational identifiability

**Scientific review: pass at the stated scope. No required mathematical or scientific wording correction was found in the reviewed reports.** Both probes reproduce their saved results in temporary copies. Separate calculations confirm the central equations and counterexamples. These are diagnostic controls and proposed research tests, not new AeST simulations or new observational fits.

Reviewed on 12 November 2026 by gpt-forge, using the requested gpt-6-astra model with ultra reasoning. The reviewer authored the separate Wave 12 audit, but did not author either report reviewed here. The independent checks do not import the authors' probes. No author artifact was changed. The repository assessment boundary remains gravity commit `70a1204a536b3dca0b3053d1a056daf22601ac00`.

**Closure.** The wave momentum flux is correct: T=epsilon²|psi_x|²-epsilon² rho_xx/4. I independently verified the local mass and momentum balances symbolically. Omitting the field-gradient term would change the measured stress. The report correctly calls the filtered quantity longitudinal stress and labels its density-normalized expression a proxy rather than thermodynamic entropy.

An independent Jacobi-Anger/Bessel construction of the wave, followed by real-space Gaussian quadrature, reproduces the reported central density, stress and proxy across five times to a maximum absolute difference of 1.07e-14. At t=1.5 it gives density 4.7906751105 and stress 2.6582099863. Adaptive quadrature of the classical particle map gives density 4.7721078637 and stress 2.6520459181.

The modal second and fourth moments are 0.5 and 0.3752 for epsilon=0.02, as stated. The matched-density preparations have a fourfold central stress range. This disproves closure by the stated local density, mean velocity, time and filter alone. It does not disprove a model retaining energy, gradients, more moments or memory. The report makes that restriction explicit.

The homogeneous kinetic response control also checks: the sine-velocity marginal has response J0(kt), while the equal-variance Gaussian has exp[-(kt)²/4]. At the first zero of J0, direct quadrature gives approximately zero against 0.2355583817. The report distinguishes these prepared kinetic states from its finite-time coherent wave.

Reversibility is handled correctly. Hamiltonian reversibility alone does not exclude thermodynamics. Here, the fixed mode occupations and noninteracting generator establish the narrower point that the increasing proxy is not evidence of thermalization. The report also excludes an inference about isolated-halo retention from its periodic box.

The primary [AeST paper, equations 7-12](https://arxiv.org/html/2007.00082v3) supports the stated dependence of pressure on additional fields. The [Schrodinger-Poisson correspondence paper](https://arxiv.org/html/1801.03507v2) supports the distinction between caustic regularization and collisionless multistream behavior. Neither converts this free-field control into an AeST collapse result.

The proposed action, constraint and response test is a reasonable bounded next step. Its 5% response target is explicitly a prospective project tolerance. The full canonical initial-state map, physical preparation of extra modes, nonlinear evolution and a universal 185 km/s scale remain unestablished.

**Observations.** Independent symbolic differentiation confirms t=x/[2(exp(x)-1)] and the stated sensitivities to acceleration scale and baryonic calibration. The full relation has two exact scaling symmetries when both calibration functions are unconstrained.

For parameter order (ln A, ln B, q, s, ln C, u), the null directions are (1,1,0,0,-1,0) and (0,0,1,1,0,-1). An independent random design gives rank four for six parameters. Exponent and amplitude transformations preserve the full predictions to better than 7e-16 relative error, including z=0. The q=1 and calibrated q=0 example is exact within this model.

The deep-limit combination is correctly q+s+2u. With sufficient acceleration and redshift coverage, constraining one calibration exponent can remove the full-curve exponent symmetry. In the strict deep limit, the combined nuisance contribution must also be bounded. The report correctly distinguishes formal matrix rank from useful precision.

The reported calibration thresholds reproduce independently. Over z=0 to 1, the signal is 0.252914 dex. Under the stated single-error Gaussian assumption, the differential mass uncertainty must be below 0.129040 dex, or the differential velocity uncertainty below 0.032260 dex.

These are conditional precision targets, not achieved survey errors or guarantees of interval coverage.

The covariance example also reproduces from an explicit matrix and generalized least-squares mean: 0.101550 dex with shared error, versus 0.039528 dex under independence, a factor 2.569 difference. Independent integration of the truncated Gaussian confirms the selection-control means to 9.8e-17 dex.

The selection thresholds were deliberately chosen to imitate an evolving relation. That construction is an existence proof. It does not estimate the MUSE selection effect. Similarly, the exact calibration symmetry does not establish that the required drifts survive actual observational constraints.

This qualification is essential and is already present in the report. The primary [MUSE-DARK III paper](https://arxiv.org/html/2604.22613v1) documents independent kinematic and stellar-mass checks, gas uncertainties and alternative reconstructions. The report acknowledges those checks and does not claim to overturn them.

[Desmond's analysis](https://arxiv.org/html/2303.11314v2) also confirms that joint inference of shared galaxy parameters is established prior work.

I independently inspected the retained image and extracted text of the later Rusishvili manuscript: the prose says 89 galaxies, while its four listed bin counts sum to 93. This supports a request for reconciliation, not rejection of its physical hypothesis. Neither report claims that its numerical corrections were independently replicated.

**Publication scope.** The material can support the conclusions to pursue a finite AeST response test and a calibrated galaxy-data sufficiency audit, while parking large collapse simulations and another fit to published bins. It cannot support measured thermalization, a new gravitational law, an actual MUSE bias estimate, or a completed new data analysis.

There are no blocking scientific findings. A minor metadata follow-up is to link this review in the publication package: the closure source ledger's original `not_done` list says that a separate-agent review had not yet occurred. That was accurate when written and is superseded by this review. Final branch composition and public serving were outside this review.

The reproducible independent checks are `second-review-checks.py` and `second-review-checks.json`. Both author scripts ran successfully in temporary copies, with every saved JSON value reproduced. All eight reviewed artifact hashes remained unchanged during the checks.

| Reviewed artifact | SHA-256 |
|---|---|
| closure/research.md | 259cc3e1d8d51dd31d9f922912ac5a36469b0e508f4506e23966ef251548011f |
| closure/caustic_control.py | e326f8c636b5f782dc2a245c1376e199f4bdbbb3a01974cb8f1bc20c3dbb9bdc |
| closure/results.json | f951fc8f17edadb60fef688e20525b0c85601e62c259d8982c6f2883c2710781 |
| closure/sources.json | c77c247ee5193dcdae4d1764e66914532ede2b80e9ff508b863f111f8315193c |
| observations/research.md | d6cd8c559c29d7a3c6c8c516cccd8304c1b7ea459f5563c53529c9aa0e7a5abe |
| observations/probe.py | e61535ad2e5c6dfaa98c250ef827b60903863e52f33368ac7d36e07f4c0cf53b |
| observations/results.json | d4fe6c69cc06562ca737e504dfbe449df18a59f49254ff536c014ee09b4726d3 |
| observations/sources.json | 276f639649b197e7dfa2a59ed97c6162562b2371169006852676e63b56e4dbfb |
