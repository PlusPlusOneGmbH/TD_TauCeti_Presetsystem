'''Info Header Start
Name : __init__
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : TauCeti_PresetSystem.toe
Saveversion : 2023.12000
Info Header End'''

from pathlib import Path
ToxFile = Path( Path(  __file__ ).parent, "Tweener.tox" )
__all__ = ["ToxFile"]



from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .extTweener import extTweener
    
    # We are missing parameters. Lets look back at the auto creation script from TD_Package.
    # Already did a lot of work there!
    class CompTyping(baseCOMP, extTweener):
        pass

else:
    class CompTyping:
        pass