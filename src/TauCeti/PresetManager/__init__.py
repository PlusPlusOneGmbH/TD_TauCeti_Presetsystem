'''Info Header Start
Name : __init__
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : TauCeti_PresetSystem.toe
Saveversion : 2023.12000
Info Header End'''
from pathlib import Path
ToxFile = Path( Path(  __file__ ).parent, "PresetManager.tox" )
__all__ = ["ToxFile"]
