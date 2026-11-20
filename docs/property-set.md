<!-- This file was generated with the assistance of an AI coding tool. -->

# The calculator's property set

**Draft.** The name is being agreed in [IfcOpenShell #9866](https://github.com/IfcOpenShell/IfcOpenShell/issues/9866);
`BBIM_StaticsCalculator` is proposed. On the calculator branch these properties are in `BBIM_Structural`, which
Bonsai itself does not otherwise use. Files saved with `BBIM_Structural` are read once and written under the
new name.

Each property's meaning and units are filled in as it moves here.

## On applied loads (IfcStructuralActivity)

| Property | Meaning |
| --- | --- |
| `MagnitudeLocked` | |
| `DirectionLocked` | |
| `KnownComponent` | |
| `MagnitudeRatio` | |
| `SameMagnitudeAs` | |
| `Push` | |
| `DrawOrder` | |

## On structural items (IfcStructuralItem)

| Property | Meaning |
| --- | --- |
| `Resultants` | |
| `ResultantEighths` | |
| `AxesRise` | |
| `AxesRun` | |

## On load cases and load groups (IfcStructuralLoadGroup)

| Property | Meaning |
| --- | --- |
| `MomentCentre` | |
| `MomentCentreUnknown` | |
| `ResultantMoment` | |
