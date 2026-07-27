# Portfolio Map

Convert public, evidence-backed work into narrow case studies. Eligibility
applies only to the wording supported by the linked artifact, not to an entire
milestone or skill area.

| Artifact | Demonstrated skill | Recruiter proof | Interview story | Resume eligibility |
|---|---|---|---|---|
| [Measured model-inference benchmark](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/results/mobilenet_v3_small.json) | Reproducible CPU inference measurement and latency/throughput analysis | Committed JSON plus a [percentile report](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/torch-modes-report.md) preserve the environment, warmups, iterations, and limits | Why batch 8 increased item throughput while increasing per-call latency in this measured run | eligible now — for the CPU benchmark and its bounded analysis, not GPU, server, or policy optimization |
| [PushT evaluation](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/metrics.json) | Seeded simulation evaluation, artifact writing, uncertainty, and failure taxonomy | Saved [provenance](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/manifest.json) and metrics report three trials and every failure | How a `0/3` result can verify an evaluator without establishing policy quality | eligible now — for evaluation execution and honest failure reporting, not policy success or current LeRobot compatibility |
| [SO-ARM101 verified bring-up](https://github.com/yanizhang-yz/so-arm101-policy-platform/blob/main/docs/phases/01-hardware-calibration-teleoperation.md) plus [active dataset work](https://github.com/yanizhang-yz/so-arm101-policy-platform/blob/main/docs/phases/02-record-and-inspect-dataset.md) | Safety-gated hardware bring-up, camera verification, supervised teleoperation, and staged data collection | Phase 1 records calibration, camera-enabled teleoperation, stability, and clean shutdown; the Phase 2 checklist remains open | Why hardware, dataset, training, and autonomous evaluation require separate gates | eligible now — for verified supervised bring-up only; dataset collection is active and policy success is unverified |
| [Chess reachability stop decision](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/docs/reachability-analysis.md) | Separating offline feasibility from physical reliability, with explicit safety limits | The analysis records offline IK candidates and the conflicting physical workspace measurement | Why an IK solution and working software did not justify claiming reliable full-board grasps | eligible now — for measurement, scope control, and the stop decision, not an autonomous chess robot |
| [Python/C++ interview ramp](https://github.com/yanizhang-yz/robotics-inference-interview/blob/main/README.md) | Public, test-driven language and systems practice | The repository exposes Python drills, C++20 contracts, reference implementations, and practice commands | How a Java/C-oriented engineer is deliberately building Python and C++ fluency for inference work | eligible now — as an active public practice resource, not as proof of professional Python/C++ mastery |

## Evidence-Backed Wording

- [Benchmarked MobileNetV3 Small on CPU](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/results/mobilenet_v3_small.json), recording stable eager batch-1 mean latency of 89.473 ms and 11.177 items/s versus batch-8 mean latency of 188.037 ms and 42.545 items/s.
- [Evaluated a Diffusion Policy across 3 seeded PushT episodes](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/metrics.json), recording `0/3` successes, a 95% Wilson interval of `0.0–0.562`, and three `low_coverage` failures.
- [Verified supervised SO-ARM101 bring-up](https://github.com/yanizhang-yz/so-arm101-policy-platform/blob/main/docs/phases/01-hardware-calibration-teleoperation.md) with a camera-enabled teleoperation workflow and a 16-minute stability run without disconnect or unsafe motion; policy-driven motion remains unverified.
- [Stopped a full-size chess-board hardware goal](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/docs/reachability-analysis.md) after offline IK/software results conflicted with physical corner reach and holding reliability, preserving the software work without claiming reliable physical execution.

## Not Yet Eligible Claims

- **not yet eligible** — trained-policy success: there is no public trained checkpoint and policy evaluation supporting this claim.
- **not yet eligible** — autonomous real-arm task success: no public autonomous trial metrics pass the real-arm completion gate.
- **not yet eligible** — SGLang performance: no actual SGLang run with committed serving metrics exists.
- **not yet eligible** — merged upstream contributions: no qualifying merged upstream contribution is part of the current evidence set.

For every eligible bullet, keep the command, environment, result, and
limitation available for follow-up. Do not promote active or planned work into
an outcome.
