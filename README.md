<!-- This file was generated with the assistance of an AI coding tool. -->

# Statics Calculator

A Blender extension, built on [Bonsai](https://bonsaibim.org/), for the hand calculations of statics as they are
taught: find a resultant, find the one or two forces that keep a point in equilibrium, take moments about a
point to find a reaction or where a force must act. You lock what you know (a magnitude, a direction, a
resultant, a moment), it solves for what is left, draws it on Bonsai's structural analysis model, and writes a
report that shows the working step by step, like a textbook solution.

It is for learning, quick checks and small determinate problems. For analysis, Bonsai's structural tools write
models for a solver.

**Status: a home being prepared.** The calculator still lives in Bonsai, on
[brunopostle/IfcOpenShell `structural-statics-calculator`](https://github.com/brunopostle/IfcOpenShell/tree/structural-statics-calculator).
It moves here piece by piece, each piece with the small extension point in Bonsai it needs, as agreed in
[IfcOpenShell #9866](https://github.com/IfcOpenShell/IfcOpenShell/issues/9866). Until then this extension does
nothing but check that Bonsai is there.

## What goes here and what goes in Bonsai

- **Bonsai:** anything that is model information or helps someone authoring for a solver: forces as components
  in global or a member's local axes, a member's axes, legible load drawings, and the extension points this
  extension uses.
- **Here:** the hand-calculation methods (locks, unknowns, linked magnitudes, resultants, moment centres, kept
  moments), their state, the worked-step reports, textbook inputs (a direction by angle, slope or eighth; a point
  placed by a distance and angle) and textbook defaults.

## State

The calculator's state is kept in the IFC, in its own property set, so that a model carries its unknowns with
it. It is documented in [docs/property-set.md](docs/property-set.md).

## Installing

Not yet packaged. It needs Bonsai installed and enabled first: Blender's extension format cannot declare that,
so enabling this extension without Bonsai stops with a message saying so.

## Tests

- **Public checks:** small models with hand-worked answers, in
  [Community_Troubleshooting](https://hub.openingdesign.com/OSArch/Community_Troubleshooting/src/branch/main/9866_Structural%20Analysis/checks).
- **Textbook problems:** a private suite of problems from a statics textbook, private because the problems are
  the book's.

Both are to run against Bonsai's daily builds once the calculator has moved here, so that a change in Bonsai
that breaks the extension shows up within a day.

## Licence

GPL-3.0-or-later, as Bonsai, which it imports. See [LICENSE](LICENSE).
