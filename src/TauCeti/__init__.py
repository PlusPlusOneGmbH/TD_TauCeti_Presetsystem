from importlib import import_module
from typing import Literal

# Lets check if this can be automated or if we need to do some more manual work
def FetchTox( path:Literal["PresetCuelist", "PresetDashboard", "PresetManager", "PresetMapper", "Tweener"] ):
    return import_module( path ).ToxFile