# Human and Agentic Workflow

Agents can accelerate drafting and checking, but they do not replace human
judgment, executed evidence, or publication approval. Every public claim must
remain traceable to a source or a committed, reproducible artifact.

## Responsibilities

| Agent responsibilities | Human verification responsibilities |
|---|---|
| Draft a bounded plan, documentation, commands, and issue or pull-request text | Decide scope, budget, and whether any hardware step is safe to perform |
| Identify missing evidence, conflicting claims, and unclear limitations | Run commands in the intended environment and inspect their outputs |
| Format a build-log entry or portfolio map from human-provided evidence | Validate sources, measurement records, and links before publication |
| Suggest a contribution route in LeRobot-first, SGLang-second order | Approve every public claim, contribution submission, and milestone-status change |

An agent must label uncertainty rather than infer a result. A human alone may
mark a milestone `verified`, and only after the evidence contract is met.

## Review Gates

1. **Scope gate:** a human confirms the milestone, route, budget cap, and any
   hardware safety conditions before work starts.
2. **Evidence gate:** a human checks that each changed claim has a source or a
   committed artifact and that limitations are stated.
3. **Execution gate:** a human runs the listed validation or measurement
   command and records the actual output where evidence is required.
4. **Publication gate:** a human reviews links, contribution state, and claim
   status before merging or publishing.

The approved milestone statuses are `planned`, `active`, `blocked`, and
`verified`. Do not use agent conclusions, a draft, or an unrun command as a
status change.

## Prohibited Publication Data

Do not publish secrets, credentials, private keys, access tokens, personal
contact details, local account-identifying absolute paths, unapproved images
or recordings of people, restricted datasets, or raw logs containing any of
those items. Do not publish fabricated measurements, estimated cloud charges
as actual costs, unsafe hardware instructions, or results that a human has not
reviewed. Redact sensitive information before sharing an artifact for review.
