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

import bpy


def find_bonsai() -> str:
    """Why Bonsai cannot be used, or an empty string if it can. Blender's extension format has no way to depend
    on another extension, so this is checked when enabling."""
    names = bpy.context.preferences.addons.keys()  # Its keys: iterating it gives Addon objects, not names.
    if not any(name == "bonsai" or name.endswith(".bonsai") for name in names):
        return "Bonsai is not enabled. Install and enable Bonsai first: https://bonsaibim.org/"
    try:
        import bonsai.tool  # noqa: F401
    except ImportError as error:
        return f"Bonsai is enabled but could not be imported: {error}"
    return ""


def register():
    if problem := find_bonsai():
        raise RuntimeError(f"Statics Calculator needs Bonsai. {problem}")
    from bonsai.bim.module.structural.load_decoration_data import ShaderInfo
    from bonsai.bim.module.structural.ui import BIM_PT_show_structural_activities

    from . import point_forces

    bpy.utils.register_class(point_forces.StaticsCalculatorProperties)
    bpy.types.Scene.StaticsCalculatorProperties = bpy.props.PointerProperty(
        type=point_forces.StaticsCalculatorProperties
    )
    BIM_PT_show_structural_activities.append(point_forces.draw_panel)
    if hasattr(ShaderInfo, "point_force_drawers"):
        ShaderInfo.point_force_drawers.append(point_forces.draw_point_forces)
    else:
        print("Statics Calculator: this Bonsai has no point_force_drawers, so forces are drawn as Bonsai draws them.")


def unregister():
    from bonsai.bim.module.structural.load_decoration_data import ShaderInfo
    from bonsai.bim.module.structural.ui import BIM_PT_show_structural_activities

    from . import point_forces

    if point_forces.draw_point_forces in getattr(ShaderInfo, "point_force_drawers", []):
        ShaderInfo.point_force_drawers.remove(point_forces.draw_point_forces)
    BIM_PT_show_structural_activities.remove(point_forces.draw_panel)
    del bpy.types.Scene.StaticsCalculatorProperties
    bpy.utils.unregister_class(point_forces.StaticsCalculatorProperties)
