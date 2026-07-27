# M2 — Learn Robot Data and Policies with LeRobot

Status: verified

## Why This Matters

Robot behavior depends on data structure and policy assumptions, not only serving speed.

## Prerequisites

Complete M1 and have a LeRobot dataset or simulation available.

## Learn

Learn how observations, actions, episodes, datasets, and policies relate.

## Build

Create a notebook or script that inspects a dataset or evaluates a simulation.

## Measure

Record observations about the data or policy behavior.

## Present

Explain what the observations and actions mean for the evaluated policy.

## Hardware-Free Path

Inspect a public dataset or run a simulation evaluation.

## Advanced Path

Compare policy behavior using a safely collected hardware dataset.

## Completion Gate

Completion gate: An inspected dataset or simulation evaluation explaining observations, actions, episodes, and policy behavior.

## Evidence

The
[merged PushT evaluation build log](https://github.com/yanizhang-yz/software-to-robotics-inference/blob/main/docs/build-log/2026-07-26-evaluating-a-robot-policy-without-hardware.md)
records the result and its claim boundary. The authoritative experiment evidence
includes the
[PushT README](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/README.md),
[saved manifest](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/manifest.json),
[saved metrics](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/results/run-2026-06-15T22-05-45%2B00-00/metrics.json),
and
[rollout video](https://github.com/yanizhang-yz/robotics-experiments/blob/master/pusht-diffusion/pusht_rollout.mp4).

This verifies evaluation execution and artifact writing: three seeded episodes
ran, success was `0/3`, the 95% Wilson interval was `0.0–0.562`, and all three
failures were classified as `low_coverage`. It does not verify policy quality
or current LeRobot compatibility.
