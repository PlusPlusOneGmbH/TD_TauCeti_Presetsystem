


'''Info Header Start
Name : extTweener
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : TauCeti_PresetSystem.toe
Saveversion : 2023.12000
Info Header End'''

import TweenObject
import TweenValue
import Exceptions

from asyncio import sleep as asyncSleep

from typing import Callable, Union, Hashable, Dict, List, Literal, Type
from argparse import Namespace

def _emptyCallback( value:TweenObject._tween ):
	pass

_type = type

class extTweener:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 						= ownerComp
		self.Tweens:Dict[int, TweenObject._tween] 	= {}

		self.Modules = Namespace(
			Exceptions 	= Exceptions
		)
		self.Constructor = Namespace(
			Expression 	= TweenValue.expressionValue,
			Static 		= TweenValue.staticValue,
			FromPar		= TweenValue.tweenValueFromParameter
		)
		self.callback 	= self.ownerComp.op('callbackManager')

		# Bacwards compatible stuff. 
		# CLearer naming conventions.

		self.StopFade 	= self.StopTween
		self.getFadeId  = self.getTweenId
		self.FadeStep	= self.TweenStep
		self.StopAllFades = self.StopAllTweens

	def getTweenId(self, parameter:Par):
		return hash(parameter)

	def TweenStep(self, step_in_ms = None):
		"""
			Progresses all active tweens for the given time. 
			Should be called from the internal clock but can be also run from an external source if wished.
		"""
		fadesCopy = self.Tweens.copy()
		for fade_id, tween_object in fadesCopy.items():
			if not tween_object.Active: continue
			tween_object.Step(step_in_ms)
			if tween_object.done: del self.Tweens[ fade_id ]
		

	def AbsoluteTweens(self, list_of_tweens:List[Dict], curve 	= "s", time 	= 1) -> List[TweenObject._tween]:
		"""
			Calls AbsoluteTween for each element of the given List of dicts
			which needs at least par and end memeber. otional time, curve, delay nd callback
		"""
		return [
			self.AbsoluteTween( tweenDict["par"], tweenDict["end"], tweenDict.get("time", time), **tweenDict )
			for tweenDict in list_of_tweens 
		]
			

	def RelativeTweens(self, list_of_tweens : List[Dict], curve 	= "s", time	= 1):
		"""
			Calls AbsoluteTween for each element of the given List of dicts
			which needs at least par and end memeber. otional time, curve, delay nd callback
		"""
		return [
			self.RelativeTween( tweenDict["par"], tweenDict["end"], tweenDict.get("time", time), **tweenDict )
			for tweenDict in list_of_tweens 
		]
	
	def AbsoluteTween(self, 
					parameter:Par, 
					end:any, 
					time:float, 
					curve:Literal["Linear", "s"] = "LinearInterpolation", 
					delay:float = 0, 
					callback: Callable = _emptyCallback):
		"""
			Creates a tween that will resolve in the defines time.
		"""
		self.CreateTween(parameter, end, time, curve = curve, delay = delay, callback = callback)
		return

	def RelativeTween(self, 
					parameter:Par, 
					end:any, 
					speed:float, 
					curve:Literal["Linear", "s"] = "LinearInterpolation", 
					delay:float = 0, 
					callback: Callable = _emptyCallback):
		"""
			Creates a tween that will resolve with the given peed ( value increment per seconds )
		"""
		difference = abs(end - parameter.eval())
		time = difference / speed
		self.CreateTween(parameter, end, time, curve = curve, delay = delay, callback = callback)
		return

	def CreateTween(self,parameter, 
					end		:float, 
					time	:float, 
					type	:Literal["fade", "startsnap", "endsnap"] = 'fade', 
					curve	:str				= "LinearInterpolation", 
					mode	:Union[str, ParMode]= 'CONSTANT', 
					expression	:str			= None, 
					delay		:float			= 0.0,
					callback	:Callable		= _emptyCallback,
					id		:Hashable			= '',  ) -> TweenObject._tween:
		"""
			Creates the given tween object based on the definition. 
		"""
		if not isinstance( parameter, Par):
			raise self.Exceptions.TargetIsNotParameter(f"Invalid Parameterobject {parameter}")
		
		targetValue	:TweenValue._tweenValue 	= TweenValue.tweenValueFromArguments( parameter, mode, expression, end )
		startValue	:TweenValue._tweenValue 	= TweenValue.tweenValueFromParameter( parameter )

		tweenClass: Type[TweenObject._tween]	  		= getattr( TweenObject, type, TweenObject.startsnap )

		tweenOject 	= tweenClass( 
			parameter, 
			self.ownerComp,
			time, 
			startValue, 
			targetValue, 
			interpolation = curve, 
			id = id
		)
		tweenOject.OnDoneCallbacks.append( callback or _emptyCallback ) 
		
		tweenOject.Delay( delay )
		self.Tweens[self.getTweenId( parameter )] = tweenOject

		tweenOject.Step( stepsize = 0 )

		return tweenOject
		

	def StopTween(self, target: Union[Par, TweenObject._tween]):
		""" Stops a tween by the tween object or the parameter wich it points to. """
		if isinstance( target, TweenObject._tween):
			target = target.parameter
			
		del self.Tweens[self.getTweenId(target)]

	def StopAllTweens(self):
		""" Stops all tweens."""
		self.Tweens = {}

	def ClearFades(self):
		self.Tweens.clear()

	def PrintFades(self):
		raise DeprecationWarning("Yeah, please dont.")

	def TweensByOp(self, targetOp:OP):
		""" Return all Tweens filtered by the given operator. """
		return {
			key : tween for key, tween in self.Tweens.items() if tween.parameter.owner == targetOp
		}