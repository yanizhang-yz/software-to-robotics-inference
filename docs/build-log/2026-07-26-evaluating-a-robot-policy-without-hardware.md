# Evaluating a Robot Policy Without Hardware

## Question

Can a pretrained Diffusion Policy be rolled out in PushT with reproducible
episode settings, a failure taxonomy, and paired provenance and metric
artifacts?

## Command and Environment

The
[PushT experiment README](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/README.md)
records the evaluation command:

```bash
python eval_pusht_policy.py --episodes 3 --max-steps 200
```

The saved
[manifest](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/manifest.json)
identifies `gym_pusht/PushT-v0`, MPS, LeRobot 0.5.1, the
`lerobot/diffusion_pusht` policy, a seed base of 1000, and a 200-step episode
limit. It also records that the source tree was dirty and that the Hub policy
was not revision-pinned.

## Observation, Action, and Episode Contracts

The authoritative
[evaluator implementation](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/eval_pusht_policy.py)
creates the environment with `obs_type="pixels_agent_pos"`, which provides a
`pixels` image plus the simulated pusher's 2D `agent_pos`. For policy input, the
evaluator converts the HWC `uint8` image to a CHW float tensor in `[0,1]`, maps
`agent_pos` to `observation.state`, and adds a batch dimension to both tensors.

After applying any loaded postprocessor, the policy output becomes a two-value
`[x, y]` target position for the simulated pusher and is passed to `env.step`.
Before each episode the evaluator calls `policy.reset()`, then resets the
environment with seed `1000 + i`. It runs until the environment terminates or
truncates under the configured 200-step limit, and maps each episode to one
trial record.

## Recorded Evidence

The evaluation ran three seeded episodes and recorded:

- `0/3` successes;
- a 95% Wilson interval of `0.0–0.562`; and
- three failures, all classified as `low_coverage`.

The exact summary and per-trial notes are in the saved
[metrics](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/metrics.json).
A separate
[rollout video](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/pusht_rollout.mp4)
shows that a policy rollout was captured, but it is not a substitute for the
three-episode metric.

In the
[PushT task](https://github.com/huggingface/gym-pusht/blob/main/README.md),
success means pushing the T into the target zone. The three recorded trials
instead reached maximum coverage of `0.02`, `0.00`, and `0.01` after 200 steps,
so every trial was classified as `low_coverage`. This shows that the recorded
episodes did not solve the task and barely covered the target; it does not
identify the cause of the behavior or establish the policy's general quality.

## What This Verifies

The run verifies the evaluation and artifact-writing path: seeded trials ran,
failures were categorized, and paired provenance and metric files were saved.
The reusable
[metrics implementation](https://github.com/yanizhang-yz/robotics-experiments/blob/master/src/robotics_experiments/eval/metrics.py)
and
[artifact-writing tests](https://github.com/yanizhang-yz/robotics-experiments/blob/master/tests/test_run.py)
make that boundary inspectable.

## What This Does Not Verify

The `0/3` result does not establish policy quality. Three episodes are too few
for a strong performance conclusion, and the wide interval makes that
uncertainty visible. The saved run establishes compatibility with the recorded
LeRobot 0.5.1 environment only; it does not establish current LeRobot
compatibility. It also does not provide a clean-source or revision-pinned
reproduction claim.

## Reusable Lesson

Separate "the evaluator works" from "the policy works." Publish failed trials,
provenance, uncertainty, and failure modes together so a weak result can still
be useful engineering evidence without being promoted into a quality claim.

## Portfolio Signal

This supports an interview story about reproducible robot-policy evaluation,
small-sample uncertainty, and honest failure reporting. It does not support a
resume claim of successful PushT control or a high-performing policy.
