# This file was generated with the assistance of an AI coding tool.
"""Run the tests in Blender, headless, with Bonsai enabled from your preferences:

blender -b --python tests/run_in_blender.py [-- pytest arguments]
"""

import bpy

bpy.context.preferences.use_preferences_save = False  # First, so that nothing overwrites userpref.blend on exit.

import os
import sys

import pytest

TESTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TESTS)
sys.path.insert(0, REPO)

import statics_calculator

statics_calculator.register()
args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
code = pytest.main([TESTS, "-p", "no:cacheprovider", "-q", *args])
print("PYTEST EXIT", int(code))
sys.stdout.flush()
os._exit(int(code))
