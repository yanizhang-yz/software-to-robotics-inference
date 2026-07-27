# Contributing

Contributions improve evidence, reproducibility, and clarity while preserving
the guide's hardware-free core and optional SO-ARM101 capstone.

## Contribution Contract

Every pull request must identify one changed claim, its evidence or source,
the validation command that was run, and its limitations. Keep LeRobot-related
work ahead of SGLang-related work unless the contribution corrects existing
documentation. Do not add a benchmark result unless the committed evidence
artifact contains the command, environment, output, and limitations.

## Before Opening a Pull Request

1. Use the reproduction template for observed behavior and the correction
   template for an inaccurate claim.
2. Keep the change focused on one claim or artifact.
3. Run `python3 -m unittest tests/test_validate_guide.py -v` and
   `python3 scripts/validate_guide.py` when the repository guide changes.
4. State whether the change affects a milestone status. Only the approved
   statuses are `planned`, `active`, `blocked`, and `verified`.

## Evidence and Safety

Never include credentials, restricted data, personal details, unsafe hardware
instructions, or account-identifying local paths. A human reviewer must verify
commands, evidence, limitations, and any public claim before it is merged.
