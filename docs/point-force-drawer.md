<!-- This file was generated with the assistance of an AI coding tool. -->

# Drawing point forces through Bonsai

Bonsai draws the forces at a point as their components, their resultant, or both. This extension adds them
graphically, by the parallelogram law or tip to tail, and marks their angles, as statics is taught. It does so
through one hook in Bonsai, `ShaderInfo.point_force_drawers`, agreed in
[IfcOpenShell #9866](https://github.com/IfcOpenShell/IfcOpenShell/issues/9866#issuecomment-7237875998). The
same Bonsai change takes the parallelogram, tip-to-tail and angle drawing out of Bonsai, so it lives here only.

## The hook

`bonsai.bim.module.structural.load_decoration_data.ShaderInfo.point_force_drawers` is a list of callables.
Bonsai calls each in turn, for every point drawn, as

```python
drawer(builder, forces, activities, location, axes, scale, size) -> bool
```

after leaving out forces of no size, for point loads and for the resultants of line loads alike:

| Argument | Meaning |
| --- | --- |
| `builder` | the `ShaderInfo` drawing the loads |
| `forces` | the X, Y and Z components of each force in Blender's axes, numpy arrays |
| `activities` | the id of the applied load each force is, or 0; pass it to `add_force_arrow` so that the arrow can be picked to edit its load |
| `location` | the point |
| `axes` | a matrix whose columns are the X, Y and Z axes shown, global or the item's own |
| `scale` | Blender length per unit of force |
| `size` | the longest arrow's length, which arrowheads and dashes are sized to |

A drawer that returns True has drawn the forces, and Bonsai draws nothing more there. One that returns False
leaves them to the next drawer, or to Bonsai.

## What of Bonsai a drawer may use

Only these, which Bonsai keeps as an interface:

- `builder.add_force_arrow(tail, tip, color, label, size, spacing=0.2, label_away=None, label_at_middle=False, activity=0)`
- `builder.add_dashed_line(start, end, size, color, dashed=True)`
- `builder.get_label_side(vector, towards)`
- `builder.force_unit`
- `builder.text_info`, a list of labels, each a dict of `position`, `text`, `color` and `away` (the direction the
  label keeps to from its position)

This extension also reads three of Bonsai's Show Loads settings, `force_display`, `force_decimals` and
`angle_decimals` on `scene.BIMStructuralProperties`, refreshes the drawing with
`bonsai.bim.module.structural.prop.update_loads_display` when its own settings change, and adds its settings to
the Show Loads panel, `BIM_PT_show_structural_activities`, with Blender's `Panel.append`.

## This extension's drawer

[`statics_calculator/point_forces.py`](../statics_calculator/point_forces.py). Its settings, under the Show Loads
panel:

- **Add Forces:** *As Bonsai* (Bonsai's Point Forces setting decides), *Parallelogram* or *Tip-to-Tail*.
- **Angles**, from the nearest horizontal or from +X.

It draws when forces are added or angles are on, and otherwise leaves the point to Bonsai. Installed, with its
defaults, the drawing is as Bonsai drew it before the hook.

## Plan

1. **Bonsai** (branch `structural-point-force-drawers` from v0.9.0): the hook, the interface written down, the
   parallelogram, tip-to-tail and angle drawing and their settings removed, and tests with a dummy drawer.
2. **This extension:** the drawer above, its settings in Show Loads, and tests run against that Bonsai branch
   (`blender -b --python tests/run_in_blender.py`).
3. Both tried together by hand, with `blender --python dev/launch.py`, which registers the extension from this
   repo for one session without installing it.
4. Then both published, the Bonsai pull request linking this extension's commit.

Later, the calculator's own additions to point-force drawing on its development branch (slope triangles, angles
between forces, moved loads, what its reports read) move into this drawer, and the load dialog and picking get
hooks of their own.
