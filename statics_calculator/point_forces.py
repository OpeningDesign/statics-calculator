# This file was generated with the assistance of an AI coding tool.
#
# Statics Calculator, an extension built on Bonsai.
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# <http://www.gnu.org/licenses/>.

"""Point forces added graphically, by the parallelogram law or tip to tail, and their angles, drawn through
Bonsai's ShaderInfo.point_force_drawers. See docs/point-force-drawer.md for what of Bonsai this uses."""

import itertools

import bpy
import numpy as np
from bpy.props import BoolProperty, EnumProperty
from bpy.types import PropertyGroup

# Each force's colour when they are drawn one by one, in turn.
COLORS = [(0.3, 0.8, 1, 1), (1, 0.4, 0.8, 1), (1, 0.9, 0.3, 1), (0.5, 1, 0.5, 1)]
AXIS_COLORS = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]


def update_display(self, context: bpy.types.Context) -> None:
    from bonsai.bim.module.structural.prop import update_loads_display

    update_loads_display(self, context)


class StaticsCalculatorProperties(PropertyGroup):
    force_display: EnumProperty(
        items=[
            ("BONSAI", "As Bonsai", "Draw point forces as Bonsai's Point Forces setting chooses"),
            (
                "PARALLELOGRAM",
                "Parallelogram",
                "Show each point force from its point, adding them into their resultant by the parallelogram law",
            ),
            (
                "TIP_TO_TAIL",
                "Tip-to-Tail",
                "Show each point force tip to tail, with their resultant closing the chain",
            ),
        ],
        name="Add Forces",
        default="BONSAI",
        update=update_display,
    )
    show_force_angles: BoolProperty(
        name="Angles",
        description="Mark the angle of each point force from a horizontal reference axis",
        default=True,
        update=update_display,
    )
    angle_reference: EnumProperty(
        items=[
            (
                "HORIZONTAL",
                "Nearest Horizontal",
                "The acute angle from the nearest horizontal axis, as statics texts draw",
            ),
            ("POSITIVE_X", "+X Axis", "The angle counter-clockwise from the +X axis"),
        ],
        name="Angle From",
        default="HORIZONTAL",
        update=update_display,
    )


def get_props() -> StaticsCalculatorProperties:
    return bpy.context.scene.StaticsCalculatorProperties


def draw_panel(self: bpy.types.Panel, context: bpy.types.Context) -> None:
    """Rows added to Bonsai's Show Loads panel"""
    props = get_props()
    layout = self.layout
    layout.label(text="Statics Calculator")
    row = layout.row(align=True)
    row.prop(props, "force_display")
    row = layout.row(align=True)
    row.prop(props, "show_force_angles")
    if props.show_force_angles:
        row.prop(props, "angle_reference", text="")


def draw_point_forces(builder, forces, activities, location, axes, scale, size) -> bool:
    """Draw the forces at a point added by the parallelogram law or tip to tail, or as Bonsai would with their
    angles marked, returning whether they were drawn; one of Bonsai's ShaderInfo.point_force_drawers"""
    props = get_props()
    bonsai_props = bpy.context.scene.BIMStructuralProperties
    mode = bonsai_props.force_display if props.force_display == "BONSAI" else props.force_display
    if mode not in ("PARALLELOGRAM", "TIP_TO_TAIL") and not props.show_force_angles:
        return False  # Bonsai draws them as they are.

    # Arrows can be picked to edit their load only when they stand for one applied load.
    single = activities[0] if len(activities) == 1 else 0
    resultant = sum(forces)
    # Components lie on the axes, so they get no angle.
    values = axes.T @ resultant
    components = [(values[j] * axes[:, j], AXIS_COLORS[j], False, single) for j in range(3) if abs(values[j]) > 1e-9]
    if mode in ("PARALLELOGRAM", "TIP_TO_TAIL"):
        # A single force has nothing to add to, so show it resolved into its components instead:
        # they are the legs of its parallelogram, and it is the diagonal.
        vectors = (
            components
            if len(forces) == 1
            else [(f, COLORS[i % len(COLORS)], True, activities[i]) for i, f in enumerate(forces)]
        )
        show_resultant = len(vectors) > 1
    elif mode == "RESULTANT":
        vectors, show_resultant = [], True
    else:
        vectors = components
        # A resultant drawn over a single component would only hide it.
        show_resultant = mode == "BOTH" and len(components) > 1

    decimals = bonsai_props.force_decimals
    start = location
    running = np.zeros(3)
    arcs_at_tail: dict[tuple, int] = {}
    reference_axes: dict[tuple, tuple] = {}
    # In a tip-to-tail chain every tip is the next tail, so labels go at the middle of each arrow, outside
    # the polygon the chain and its resultant make; elsewhere tails are shared, so labels go at the tips.
    chain = np.cumsum([np.zeros(3)] + [vector for vector, *_ in vectors], axis=0) * scale + location
    centre = chain.mean(axis=0) if mode == "TIP_TO_TAIL" else None
    for i, (vector, color, has_angle, activity) in enumerate(vectors):
        tail = start if mode == "TIP_TO_TAIL" else location
        if mode == "PARALLELOGRAM" and i:
            # Complete the parallelogram of the vectors so far and this one. Each side is coloured
            # as the vector it is parallel to; the sum of the vectors so far is a resultant, in white.
            corner = location + (running + vector) * scale
            running_color = vectors[0][1] if i == 1 else (1, 1, 1, 1)
            builder.add_dashed_line(location + running * scale, corner, size, color)
            builder.add_dashed_line(location + vector * scale, corner, size, running_color)
            if i < len(vectors) - 1:
                builder.add_dashed_line(location, corner, size, (1, 1, 1, 1))  # An intermediate resultant.
        tip = tail + vector * scale
        label = f"{np.linalg.norm(vector):.{decimals}f} {builder.force_unit}"
        if centre is None:
            builder.add_force_arrow(tail, tip, color, label, size, activity=activity)
        else:
            side = builder.get_label_side(vector, (tail + tip) / 2 - centre)
            builder.add_force_arrow(
                tail, tip, color, label, size, label_away=side, label_at_middle=True, activity=activity
            )
        if props.show_force_angles and has_angle:
            add_force_angle(builder, tail, vector, size, color, arcs_at_tail, reference_axes)
        start = tip
        running = running + vector

    if show_resultant:
        label = f"{'R = ' if len(forces) > 1 else ''}{np.linalg.norm(resultant):.{decimals}f} {builder.force_unit}"
        if abs(resultant[1]) < 1e-9 and not props.show_force_angles:
            label += f" at {np.degrees(np.arctan2(resultant[2], resultant[0])):.{bonsai_props.angle_decimals}f} deg"
        # Alpha 2 because the shader caps opacity at half of it; the resultant draws fully opaque.
        # Labelled to the side, as a resultant often runs along one of the forces: outside the chain's
        # polygon, or else above.
        tip = location + resultant * scale
        outside = np.array((0, 0, 1.0)) if centre is None else (location + tip) / 2 - centre
        builder.add_force_arrow(
            location,
            tip,
            (1, 1, 1, 2),
            label,
            size,
            spacing=0.3,
            label_away=builder.get_label_side(resultant, outside),
            label_at_middle=centre is not None,
            activity=single,
        )
        if props.show_force_angles:
            add_force_angle(builder, location, resultant, size, (1, 1, 1, 1), arcs_at_tail, reference_axes)
    add_reference_axes(builder, reference_axes, size)
    return True


def add_force_angle(builder, tail, vector, size, color, arcs_at_tail: dict, reference_axes: dict) -> None:
    """Mark a force's angle from a horizontal reference axis, as an arc in the X-Z plane"""
    if abs(vector[1]) > 1e-9 * np.linalg.norm(vector):
        return  # Not in the X-Z plane, so one angle does not describe it.
    props = get_props()
    end = np.degrees(np.arctan2(vector[2], vector[0]))
    start = 0.0
    if props.angle_reference == "HORIZONTAL" and vector[0] < -1e-9 * np.linalg.norm(vector):
        # Measured from -X, so that the angle is the acute one statics texts draw.
        start = 180.0
        end = end if end > 0 else end + 360
    if abs(end - start) < 0.01:
        return
    key = tuple(np.round(tail, 6))
    arcs_at_tail.setdefault(key, 0)
    # Arcs sharing a tail get growing radii so that they do not overlap.
    radius = size * (0.18 + 0.05 * arcs_at_tail[key])
    arcs_at_tail[key] += 1
    reference_axes.setdefault((key, start), (tail, start, []))[2].append((radius, color))
    steps = max(4, int(abs(end - start) / 5))
    points = [
        tail + radius * np.array((np.cos(a), 0, np.sin(a))) for a in np.radians(np.linspace(start, end, steps + 1))
    ]
    for a, b in itertools.pairwise(points):
        builder.add_dashed_line(a, b, size, color, dashed=False)
    middle = np.radians((start + end) / 2)
    outward = np.array((np.cos(middle), 0, np.sin(middle)))
    # Away from the arc, and above or below the reference axis so small angles keep off the lines.
    away = outward + np.array((0, 0, np.sign(vector[2])))
    angle = abs(end - start) if props.angle_reference == "HORIZONTAL" else end
    decimals = bpy.context.scene.BIMStructuralProperties.angle_decimals
    builder.text_info.append(
        {
            "position": tail + radius * outward,
            "text": f"θ = {angle:.{decimals}f}°",
            "color": color,
            "away": away / np.linalg.norm(away),
        }
    )


def add_reference_axes(builder, reference_axes: dict, size: float) -> None:
    """Draw the horizontal axes angles are measured from, each band coloured as the arc that starts in it"""
    for tail, start, arcs in reference_axes.values():
        direction = np.array((np.cos(np.radians(start)), 0, 0))
        arcs.sort(key=lambda arc: arc[0])
        band_start = 0.0
        for i, (radius, color) in enumerate(arcs):
            # Bands end just past their arc, before the next arc out; the last runs on to the axis' length.
            band_end = radius + size * 0.04 if i < len(arcs) - 1 else max(radius + size * 0.04, size * 0.45)
            builder.add_dashed_line(tail + direction * band_start, tail + direction * band_end, size, color)
            band_start = band_end
