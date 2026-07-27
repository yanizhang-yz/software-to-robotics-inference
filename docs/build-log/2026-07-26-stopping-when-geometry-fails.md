# Stopping When Geometry Fails

## Intended Goal

The SO-ARM101 chess project set out to execute chess moves on a full-size board.
Its software stack covers game rules, move expansion, board transforms, inverse
kinematics, motion choreography, and mock and hardware backends. The physical
full-board goal was not completed.

## Conflicting Evidence

The
[reachability analysis](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/docs/reachability-analysis.md)
separates modeled feasibility from physical reliability. A historical offline
audit found inverse-kinematics candidates with calculated position error of
4 mm or less for all 64 square targets. On hardware, the farthest full-size
board corners measured roughly 1 cm beyond the arm's dependable
position-holding workspace when the complete grasp geometry was considered.

An IK candidate was therefore not treated as proof of a repeatable physical
grasp. Software retries could not add link length or holding authority, and
moving the fixture could improve one edge while degrading another.

## Command and Environment

The hardware result comes from supervised SO-ARM101 bring-up against a
full-size board. The hardware-independent core and `MockArm` checks support
Python 3.10 or newer and run with:

```bash
.venv/bin/python -m pytest -q
```

The physical LeRobot backend requires Python 3.12 or newer. The test command
verifies software behavior; it does not reproduce the physical reach
measurement.

## Stop Decision

The project stopped before claiming a completed physical chess game. The
[transition lessons](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/docs/transition-lessons.md)
explain why that is an engineering result: preserving the working software while
rejecting an unsafe or unreliable product claim protects both users and the
credibility of the evidence.

The
[safety boundary](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/docs/safety.md)
requires supervised, turn-based motion, an accessible power cut, bounded
above-board checks, and a stop when reach or stability is uncertain.

## What Remains Useful

The
[architecture](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/docs/architecture.md)
keeps rules, geometry, motion, and hardware I/O behind explicit interfaces.
`MockArm` can exercise the command path without moving a device, but the
documentation explicitly avoids treating that as physical proof. The
[public-tree test](https://github.com/yanizhang-yz/so-arm101-chess-robot/blob/main/tests/test_public_tree.py)
also guards the published repository against personal paths, concrete hardware
identifiers, and private relationship wording; it does not test reachability.

The measured next experiments are a smaller board or a systematically
repositioned fixture, followed by repeatable corner holds and one isolated piece
before any full move.

## Reusable Lesson

Define physical stop conditions before testing, and keep simulation feasibility,
hardware repeatability, and product completion as separate claims. An honest
decision to stop when geometry invalidates the goal demonstrates engineering
judgment more strongly than retries or polished wording can.

## Portfolio Signal

This is evidence of interface design, safety boundaries, measurement, and scope
control. It is not evidence of a completed autonomous chess robot or reliable
full-board grasping.
