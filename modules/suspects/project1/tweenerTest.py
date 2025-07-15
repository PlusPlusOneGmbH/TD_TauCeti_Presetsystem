'''Info Header Start
Name : tweenerTest
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : TauCeti_PresetSystem.toe
Saveversion : 2023.12000
Info Header End'''
from asyncio import sleep
tweener = op("Tweener")
parComp = op("parameter1")
async def naiveTweenerTest():
    parComp.par.Float1.val = 0
    parComp.par.Float2.val = 0
    # Test awaitability
    await tweener.AbsoluteTween(
        parComp.par.Float1,
        1,
        1
    ).Resolve()

    assert parComp.par.Float1.eval() == 1
    
    await tweener.RelativeTween(
        parComp.par.Float2,
        1,
        1
    ).Resolve()

    assert parComp.par.Float2.eval() == 1
    

    tweener.AbsoluteTweens(
        [
            { "par" : parComp.par.Float1, "end" : 0},
            { "par" : parComp.par.Float2, "end" : 0, "time" : 2}
        ],
        time = 1
    )
    await sleep(2)
    assert parComp.par.Float1.eval() == 0 and  parComp.par.Float2.eval() == 0
    
    
     
    tweener.RelativeTweens(
        [
            { "par" : parComp.par.Float1, "end" : 1},
            { "par" : parComp.par.Float2, "end" : 1, "speed" : 2}
        ],
        speed = 1
    )
    await sleep(1)

    assert parComp.par.Float1.eval() == 1 and  parComp.par.Float2.eval() == 1
    

op("TDAsyncIO").Run( naiveTweenerTest() )