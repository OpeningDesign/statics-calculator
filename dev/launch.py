# This file was generated with the assistance of an AI coding tool.
"""Run Statics Calculator from this repo in a Blender session, for development, without installing it.

    blender --python dev/launch.py

Blender starts as usual, Bonsai enabled from your preferences, then this registers the extension from the repo for
this session only. It never changes the add-on list or installs anything, and turns off saving preferences for the
session so that nothing done in it is written to userpref.blend: use Save Preferences if you mean to keep a change.
"""

import bpy

bpy.context.preferences.use_preferences_save = False  # First, so that this session writes nothing to userpref.blend.

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

import statics_calculator

statics_calculator.register()
print("Statics Calculator registered from", statics_calculator.__file__)
