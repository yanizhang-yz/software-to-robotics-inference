# Budget and Hardware Paths

Choose the least expensive path that can answer the current milestone's
question. Simulation and cloud work are the hardware-free core; a real arm is
an optional capstone, not a prerequisite for progress.

## Path A — Existing Laptop and CPU

Use the laptop already available for M0 planning, small CPU inference in M1,
LeRobot dataset inspection or simulation in M2, and synthetic or simulated
loop work in M4. Keep inputs small enough for the machine, record the command
and environment, and describe the limits of CPU-only results. Do not buy
hardware merely to advance the guide.

## Path B — Simulation plus Budget-Capped Cloud GPU

Use simulation locally and reserve a cloud GPU for work that genuinely needs
one, such as a representative inference, policy, or serving experiment. Before
starting, write a purpose, a spending cap, and a shutdown plan. Stop or remove
the resource when the planned measurement is complete; do not leave a resource
running while deciding what to measure next.

## Path C — Real SO-ARM101 Capstone

Choose this path only after M2 and only when safe SO-ARM101 access,
supervision, recovery procedures, and local safety rules are available. It is
the advanced M3 capstone. If any of those conditions are unavailable, continue
with the simulation or cloud path instead.

## Cost Recording Contract

For every cloud run, commit the measurement record when the run occurs. It
must name the provider, instance, active runtime, billed runtime, and actual
cost. Include the command, workload, and limitations so another engineer can
interpret the cost alongside the result. Do not publish estimated prices as
actual costs, and do not treat a planned run as evidence.

## Stop Conditions

Stop a cloud step when its purpose changes, its spending cap would be exceeded,
the billing record cannot be captured, or the resource cannot be shut down.
Stop a hardware step when safety, supervision, or recovery conditions are not
met. In either case, record the limitation and select a lower-risk path rather
than filling the gap with an unsupported claim.
