# Independent correction review

The [review](REVIEW.md) and [replay script](check.py) independently check gravity commit `e5d7ee813e33de03c91857e48a2d55a0caf55506`. The reviewed source hashes are frozen in [evidence.json](evidence.json). The script accepts later commits that preserve those source bytes.

The frozen review covers the old source tree only. It does not review the documentation merge with main d144448. Replay it against the exact old checkout with NumPy, SciPy and SymPy installed:

```sh
git worktree add --detach /tmp/gravity-wave11-12-reviewed-e5d7ee8 e5d7ee813e33de03c91857e48a2d55a0caf55506
python3 research/wave11-12-review-20261112/check.py /tmp/gravity-wave11-12-reviewed-e5d7ee8
```

This reproduces numerical and source-level controls. It does not establish a physical seed-formation mechanism or validate the repository's wider claims. The nine inherited manifest discrepancies recorded in the review describe the reviewed commit, before the separate checksum repair.

The wider [research synthesis](https://github.com/Foundation-0/physics0/pull/18) connects the field, mechanical and observational results and identifies what would justify further research.
