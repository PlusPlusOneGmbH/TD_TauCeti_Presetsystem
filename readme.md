# TauCeti PresetSystem + Tweener
Highly customisable and setup agnostic system for presets management in TouchDesigner

## Tweener
The tweener is the heart of the whole system and a great component in itself. It allows for programmatic creation and management of Tweens, transitions between states of a parameter. Be it Expression or Static, fadeable and non-fadeable parameters, the Tweener should be able to handle them.

__ There should only be one tweener per project. Use GlobalOP-Shortcuts or other means of dependency management __


The tweener offers several ways of creating tweens. All do wrap arround CreateTween as the most important method.
```python
op("Tweener").AbsoluteTween(	   
					parameter : Par, 
					targetValue : any, 
					time : float, 
					curve : str            = "LinearInterpolation", 
					delay : float          = 0, 
					callback : Callable    = _emptyCallback ) -> TweenObject
# Creates a tween that will resolve in the defines time.

op("Tweener").RelativeTween( 
				   parameter:Par, 
				   targetValue:any, 
				   speed:float, 
				   curve:str            = "LinearInterpolation", 
				   delay:float          = 0, 
				   callback: Callable   = _emptyCallback) -> TweenObject
# Creates a Tween that will resolve with the given speed in distance per seconds.

```

Both functions are clearly aimed at fadeable, meaning numeric, parameters. They will fail for non-numeric values.

For nun-numeric parameters the underlying CreateTween is required.
```python
op("Tweener"):CreateTween(
					parameter :Par, 
					targetValue	:float, 
					time	:float, 
					type	:Literal["fade", "startsnap", "endsnap"] = 'fade', 
					curve	:str				= "LinearInterpolation", 
					mode	:Union[str, ParMode]= 'CONSTANT', 
					expression	:str			= None, 
					delay		:float			= 0.0,
					callback	:Callable		= _emptyCallback,
					id		:Hashable			= '',  ) -> TweenObject:
# Creates a Tween for the given paramaters.
# If mode is set to ParMode.EXPRESSION, the targetValue will be ignored and expression wil be used instead.
```

calback is a function that takes a single arguments in form of the TweenObject.

The TweenObject has the following attributes and methods:

```python
Active : bool # If False, the tween will not be continued until Active is back to True
OnDoneCallbacks : List[Callable] # A list of callales that will be executed once the tween is done.
Done : bool # True if the Tween is done.
Remaining : float # seconds left unti complition.

Pause() # Halts the continuation of the tween untils resumed.
Resume() # Continues the tween.
Stop() # Stops the tween right where it is and removes it. 
Reset() # Reverses all changes done by the tween and stops it.
Reverse() # Changes target and startingpoint mid flight. 
Delay(offset:float) # Reduces the current ime by offset. When at 0, this results in a delay, when above 0 will result in a stepback.
```


The Tweener itself also offers some additional utility functions.
```python
StopTween( target: Union[Par, TweenObject._tween]) # Stops a tween by the tween object or the parameter wich it points to.
StopAllFades() # Does exactly what it sais it does. Should be named StopAllTweens though. 
Tweens : Dict[int, TweenObject] # A dict containing all tweens, keyed by an unique ID per parameter.
TweensByOp( targetOpartor:OP) # Returns a list of all tweens that are running and pointing at a prameter of the given operator.
```


## TauCeti: TBD