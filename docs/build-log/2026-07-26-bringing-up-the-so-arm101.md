# Bringing Up the SO-ARM101 Before Training a Policy

## Goal

Prepare a real SO-ARM101 for one narrow task—pick up a red cube and place it in
a bowl—while keeping hardware bring-up, dataset collection, training,
evaluation, and serving as separate evidence gates.

## Phase 1: Verified

The
[hardware, calibration, camera, and teleoperation record](https://github.com/yanizhang-yz/so-arm101-policy-platform/blob/main/docs/phases/01-hardware-calibration-teleoperation.md)
documents the completed Phase 1 gate. It records restored and verified
calibration, a name-resolved 640×480 camera stream at 30 frames per second,
smooth leader-to-follower teleoperation, and a 16-minute integrated run with no
disconnect or unsafe motion and a clean shutdown.

That evidence verifies supervised camera-enabled teleoperation. It does not
verify policy-driven motion.

## Phase 2: Active

The
[dataset recording and inspection phase](https://github.com/yanizhang-yz/so-arm101-policy-platform/blob/main/docs/phases/02-record-and-inspect-dataset.md)
defines a three-episode local pilot before full collection. Its completion
checklist remains unchecked, so dataset recording is active rather than
verified.

The
[transition capstone map](https://github.com/yanizhang-yz/so-arm101-policy-platform/blob/main/docs/guides/transition-capstone.md)
keeps the later gates explicit: training, autonomous evaluation, inference
serving, and cost evidence remain planned.

## Command and Environment

Phase 1 used LeRobot 0.6.0 with an SO-ARM101 leader and follower and a W1 camera
on the Mac robot-side computer. The authoritative Phase 1 record preserves the
teleoperation commands while keeping machine-specific serial ports out of the
repository.

## Current Claim Boundary

There is no claim of a recorded dataset, trained checkpoint, autonomous
evaluation, or remote policy server. The verified result is Phase 1 hardware
bring-up; the current work is the Phase 2 pilot protocol.

## Reusable Lesson

Treat physical-system progress as a sequence of irreversible-risk gates. Verify
calibration, cameras, supervised motion, stability, and shutdown before
collecting data; inspect a small pilot before scaling it; and do not let a
working teleoperation session stand in for policy evidence.

## Portfolio Signal

This entry supports a safety-aware hardware bring-up story and shows how
software reliability practices transfer to physical systems. It is not yet
eligible as evidence of dataset quality, training, autonomous task success, or
production serving.
