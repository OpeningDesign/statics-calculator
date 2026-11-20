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
    if not any(name == "bonsai" or name.endswith(".bonsai") for name in bpy.context.preferences.addons.keys()):
        return "Bonsai is not enabled. Install and enable Bonsai first: https://bonsaibim.org/"
    try:
        import bonsai.tool  # noqa: F401
    except ImportError as error:
        return f"Bonsai is enabled but could not be imported: {error}"
    return ""


def register():
    if problem := find_bonsai():
        raise RuntimeError(f"Statics Calculator needs Bonsai. {problem}")


def unregister():
    pass
