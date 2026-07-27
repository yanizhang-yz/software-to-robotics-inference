# From Backend Software to Robotics Inference: My Gap Map

## Starting Strengths

The starting point is software engineering experience with APIs, data flows,
testing, observability, concurrency, and production reliability, plus light
exposure to machine learning, Python, and C++. These skills provide a systems
foundation, but they do not by themselves demonstrate modern model execution or
safe robot operation.

## Missing Model-Execution Skills

- Run modern models and distinguish warmup, forward-pass, preprocessing, and
  end-to-end latency.
- Measure throughput, tail latency, batching behavior, and device memory instead
  of treating "the model ran" as a performance result.
- Operate GPU-backed model servers and explain scheduling, backpressure, and
  cost trade-offs.
- Connect language- or vision-model serving to the observation-to-action
  contracts used by a robot policy.

## Missing Robotics Skills

- Read observations, actions, frames, episodes, and dataset metadata as explicit
  interfaces.
- Evaluate a policy in simulation with reproducible seeds, machine-readable
  metrics, and a failure taxonomy.
- Calibrate hardware, verify cameras and teleoperation, and define safety and
  stop conditions before autonomous motion.
- Measure control-loop timing and handle stale actions, overload, recovery, and
  network failure.

## Skills That Transfer Directly

The guide's
[skill-translation map](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/skill-translation.md)
makes the bridge explicit:

| Existing software skill | New application |
|---|---|
| API and service design | Model-serving endpoints and versioned policy contracts |
| Queues and concurrency | Dynamic batching and asynchronous policy loops |
| Observability | Latency, throughput, device memory, and control frequency |
| Testing | Numerical checks, policy evaluation, and hardware-in-the-loop gates |
| Reliability engineering | Timeouts, stale-action handling, emergency stops, and recovery |
| Data pipelines | Robot demonstrations, episodes, datasets, and replay |

The transfer is useful because the engineering habits already exist. The gap is
learning which robotics and inference signals those habits must protect.

## Selected Learning Order

1. Measure one model locally before attempting serving optimization
   ([M1](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/milestones/m1-model-inference.md)).
2. Learn robot data and policy evaluation with LeRobot and simulation
   ([M2](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/milestones/m2-lerobot-data-policies.md)).
3. Use the SO-ARM101 only as an optional, safety-gated physical capstone
   ([M3](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/milestones/m3-real-arm-capstone.md)).
4. Build and test the asynchronous observation-to-action loop
   ([M4](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/milestones/m4-robotics-inference-loop.md)).
5. Study SGLang serving after robot-policy contracts and timing constraints are
   concrete
   ([M5](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/milestones/m5-sglang-serving.md)).
6. Turn verified evidence into an upstream contribution and an interview story
   ([M6](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/milestones/m6-contribute-and-present.md)).

This order deliberately puts LeRobot before SGLang so serving decisions answer
a robotics requirement instead of becoming an isolated infrastructure demo.

## Command and Environment

This milestone produces a documentation artifact, so it has no runtime command.
The selected core environment is hardware-free simulation plus cloud compute;
safe SO-ARM101 access is an optional advanced path.

## Observable Artifacts

This gap map and selected route are the M0 artifact. The related
[Robotics Inference Foundations roadmap](https://github.com/yanizhang-yz/robotics-inference-foundations/blob/main/ROADMAP.md)
also makes current boundaries visible: its backpropagation and transformer
gates are passed, while reinforcement learning is active and the
behavior-cloning, Diffusion Policy, ACT, VLA, and policy-deployment gates remain
unfinished. Later milestones must link separate runnable evidence rather than
turning this map into a claim that those skills are already complete.

## Limitations

This is a learning-gap snapshot, not proof of professional mastery. It contains
no employer names or private work details, and it does not claim GPU serving,
trained robot policies, autonomous arm success, or upstream contribution
results. Hardware is optional; simulation and cloud work remain the core path.

## Reusable Lesson

Translate familiar engineering skills into observable domain behaviors, then
name the missing artifacts in dependency order. A gap map becomes useful when
each gap ends in a public completion gate rather than a list of topics to read.
