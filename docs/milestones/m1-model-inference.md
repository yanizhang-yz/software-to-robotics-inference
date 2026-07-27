# M1 — Execute and Measure a Model

Status: verified

## Why This Matters

Inference work starts with a reproducible baseline rather than an anecdotal run.

## Prerequisites

Complete M0 and have access to a CPU or GPU runtime.

## Learn

Learn warmup behavior, latency percentiles, and the limits of a benchmark.

## Build

Create a repeatable inference command and measurement script.

## Measure

Capture warmup and latency percentiles in the target environment.

## Present

Explain the command, results, environment, and limitations.

## Hardware-Free Path

Run a small model on CPU or a cloud GPU.

## Advanced Path

Compare configurations across accelerators or model sizes.

## Completion Gate

Completion gate: A reproducible CPU or GPU inference run with warmup, P50/P95/P99 latency, environment, and limitations.

## Evidence

The
[merged benchmark build log](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/build-log/2026-07-26-measuring-model-inference.md)
indexes the command, environment, measured results, and claim boundaries. The
authoritative lab evidence includes the
[benchmark overview](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/README.md),
[committed MobileNetV3 Small JSON](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/results/mobilenet_v3_small.json),
[percentile report](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/experiments/model-benchmarks/torch-modes-report.md),
[implementation](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/src/robotics_inference_lab/torch_benchmark.py),
and
[tests](https://github.com/yanizhang-yz/robotics-inference-lab/blob/main/tests/test_torch_benchmark.py).

This verifies a reproducible CPU forward-pass benchmark with committed JSON and
a percentile report. It does not verify GPU performance, server request
latency, preprocessing or postprocessing, prediction quality, or robot-policy
performance.
