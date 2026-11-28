# This file was generated with the assistance of an AI coding tool.
"""Point forces drawn through Bonsai's ShaderInfo.point_force_drawers. Run by tests/run_in_blender.py."""

from unittest import mock

import bpy
import numpy as np
import pytest
from bonsai.bim.module.structural.load_decoration_data import ShaderInfo

from statics_calculator import point_forces


@pytest.fixture
def settings():
    bonsai = bpy.context.scene.BIMStructuralProperties
    bonsai.reference_frame, bonsai.force_display, bonsai.force_scale = "GLOBAL_COORDS", "BOTH", 0.0
    bonsai.force_decimals = bonsai.angle_decimals = 2
    props = point_forces.get_props()
    props.force_display, props.show_force_angles, props.angle_reference = "BONSAI", False, "HORIZONTAL"
    return props


def draw(forces, activities=None):
    """What Bonsai draws for these forces, (x, z) each, at the origin"""
    with mock.patch("bonsai.bim.module.structural.load_decoration_data.DecorationShader"):
        info = ShaderInfo()
    info.force_unit = "kN"
    vectors = [np.array((x, 0.0, z)) for x, z in forces]
    info.draw_point_forces(vectors, np.zeros(3), np.eye(3), activities or [0] * len(forces))
    return info


def labels(info):
    return [entry["text"] for entry in info.text_info]


def test_registered_as_a_drawer():
    assert point_forces.draw_point_forces in ShaderInfo.point_force_drawers


def test_left_to_bonsai_unless_added_or_angled(settings):
    info = draw([(3.0, 4.0), (-2.0, 0.0)])
    # Bonsai's Both: X and Z of the resultant, and the resultant, labelled with its angle.
    assert len(info.info) == 3 and any(text.startswith("R = 4.12 kN at") for text in labels(info))


def test_parallelogram_draws_each_force_and_completes_the_parallelogram(settings):
    settings.force_display = "PARALLELOGRAM"
    info = draw([(3.0, 4.0), (-2.0, 0.0)], activities=[11, 12])
    # Two forces, the resultant, and the two dashed sides of the parallelogram.
    assert len(info.info) == 5
    assert sorted(p["activity"] for p in info.pickables) == [11, 12]
    assert sorted(labels(info)) == ["2.00 kN", "5.00 kN", "R = 4.12 kN at 75.96 deg"]


def test_tip_to_tail_chains_the_forces_labelled_at_their_middles(settings):
    settings.force_display = "TIP_TO_TAIL"
    info = draw([(3.0, 4.0), (-2.0, 0.0)])
    second = next(entry for entry in info.text_info if entry["text"] == "2.00 kN")
    # From the first force's tip at (3, 4) to (1, 4), scaled with the longest arrow to 2: labelled at its middle.
    assert np.allclose(second["position"], np.array((2.0, 0.0, 4.0)) * 2 / 5)


def test_angles_marked_from_the_nearest_horizontal(settings):
    settings.force_display, settings.show_force_angles = "PARALLELOGRAM", True
    texts = labels(draw([(3.0, 4.0), (-2.0, 0.0)]))
    assert "θ = 53.13°" in texts  # The 5 kN force, from +X.
    assert "θ = 75.96°" in texts  # The resultant.
    assert not any(" at " in text for text in texts)  # The arc gives the resultant's angle instead.


def test_angles_alone_take_over_bonsais_drawing(settings):
    settings.show_force_angles = True
    texts = labels(draw([(3.0, 4.0), (-2.0, 0.0)]))
    # Bonsai's Both still, the resultant's components and itself, with its angle marked.
    assert "θ = 75.96°" in texts and sorted(t for t in texts if t.endswith("kN")) == [
        "1.00 kN",
        "4.00 kN",
        "R = 4.12 kN",
    ]
