from importlib import import_module
from typing import Literal



def FetchTox( path:Literal["PresetCuelist", "PresetDashboard", "PresetManager", "PresetMapper", "Tweener"] ):
    """
        A helper function to enable importing nested modules in TouchDesigner using Module on Demand. 
        TouchDesigners Module on Deman (mod) can not import nested packages and will fail. 
        While you can run 
        from TauCeti.PresetCuelist import ToxFile
        in any script, running
        mod.TauCeti.PresetCuelist.ToxFile
        will fail. Instead you need to use this helper-function
        mod.TauCeti.FetchTox("PresetCuelist")

        Still evaluating is there is a better way, but this is close enough.
    """
    return import_module( f".{path}", "TauCeti" ).ToxFile