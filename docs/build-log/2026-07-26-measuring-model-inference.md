# Measuring Model Inference Before Optimizing It

## Question

How do execution mode, batch size, and input-shape stability affect latency and
throughput for the same image model?

## Existing Software Skill

This applies familiar performance-engineering habits: hold the workload
constant, warm it up, record tail latency as well as averages, preserve the raw
result, and keep conclusions inside the measured environment.

## New Inference Skill

The benchmark separates eager execution from `torch.inference_mode`, stable
from changing batch shapes, and call latency from item throughput. The
[benchmark overview](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/README.md)
explains why those are distinct inference-system questions.

## Command and Environment

The committed MobileNetV3 Small result records a CPU device, 10 warmup calls,
100 measured iterations per case, batch sizes 1, 4, and 8, random
`[batch, 3, 224, 224]` inputs, and no pretrained weights:

```bash
.venv/bin/python experiments/model-benchmarks/bench_torch_modes.py \
  --model mobilenet_v3_small \
  --batch-sizes 1 4 8 \
  --output-json experiments/model-benchmarks/results/mobilenet_v3_small.json
```

The runnable path is split between the
[benchmark CLI](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/bench_torch_modes.py)
and the reusable
[benchmark implementation](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/src/robotics_inference_lab/torch_benchmark.py).
Its behavior is covered by
[benchmark tests](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/tests/test_torch_benchmark.py).

## Measured Evidence

The
[machine-readable MobileNet result](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/results/mobilenet_v3_small.json)
records stable eager batch 1 at 89.473 ms mean latency and 11.177 items/s, and
stable eager batch 8 at 188.037 ms and 42.545 items/s. In this run, batching
increased per-call latency while increasing item throughput.

The
[torch-modes report](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/torch-modes-report.md)
adds the full percentile table and interprets it. It also shows why
`torch.inference_mode` should be measured instead of assumed to win: its effect
varied by model and batch size in the recorded CPU results.

## What the Numbers Do Not Prove

These are device-specific local forward-pass measurements. They do not establish
GPU performance, prediction quality, preprocessing or postprocessing cost,
server request latency, network overhead, action-decoding cost, or VLA-policy
performance. Random tensors and untrained weights are appropriate for measuring
execution cost, but not for making accuracy claims. The result should not be
generalized to another machine without rerunning it.

## Reusable Lesson

Before optimizing inference, preserve the command, device, warmups, iteration
count, percentiles, and machine-readable rows. Compare latency and throughput
separately: an optimization can improve capacity while making one request wait
longer.

## Portfolio Signal

The evidence demonstrates a reproducible measurement harness and
claim-bounded analysis. It supports discussion of benchmark design and
latency-throughput trade-offs; it does not support a claim of GPU, server, or
robot-policy optimization.
