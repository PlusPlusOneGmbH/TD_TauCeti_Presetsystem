

'''Info Header Start
Name : extTauCetiManager
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : TauCeti_PresetSystem.toe
Saveversion : 2023.12000
Info Header End'''

TDFunctions = op.TDModules.mod.TDFunctions
import uuid
from extParStack import InvalidOperator
from typing import Literal, Union


def snakeCaseToCamelcase( classObject ):
	import inspect
	from optparse import OptionParser
	for methodName, methodObject in inspect.getmembers(OptionParser, predicate=inspect.isfunction) :
		if methodName[0].isupper():
			setattr( 
				classObject, 
				"".join( word.capitalize() for word in methodName.split("_")),
				methodObject
			)


class PresetDoesNotExist(Exception):
	pass

class extTauCetiManager:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 		= ownerComp
		# self.stack     		= self.ownerComp.ext.extParStack # ????
		# self.tweener   		= self.ownerComp.op('olib_dependancy').Get_Component()
		self.tweener 		= self.ownerComp.op("remote_dependency").GetGlobalComponent()
		self.modeler 		= self.ownerComp.op('modeler')
		self.preview 		= self.ownerComp.op("previews")
		self.logger 		= self.ownerComp.op("logger")
		self.prefab 		= self.ownerComp.op("emptyPreset")
		self.Record_Preset	= self.Store_Preset
		self.PresetDoesNotExist = PresetDoesNotExist
		snakeCaseToCamelcase( self )

	@property
	def stack(self):
		return self.ownerComp

	@property
	def preset_folder(self):
		return self.ownerComp.op("Presetfolder_RepoMaker").Repo

	def Find_Presets(self, name:str="", tag:str="") -> list[str]:
		"""
			Returns a listpreset_ids of presets given the defined parameters.
		"""
		return_values = []
		for child in self.preset_folder.findChildren(depth = 1):
			if name and child.par.Name.eval() != name: continue
			if tag and child.par.Tag.eval() != name: continue
			return_values.append( child.name )
		return return_values

	def Export_Presets(self, path:str):
		"""
			Save the preset as a TOX for the given path.
		"""
		self.preset_folder.save( path, createFolders = True )

	def Import_Presets(self, path:str):
		"""
			Load a TOX as the external presets.
		"""
		self.preset_folder.par.externaltox = path
		self.preset_folder.par.reinitnet.pulse()
		self.preset_folder.par.externaltox = ""

	def store_prev(self, prefab):
		prefab.op("preview").par.top = self.ownerComp.op("preview")			
		prefab.op("preview").bypass = False
		prefab.op("preview").lock = False
		prefab.op("preview").bypass = not self.ownerComp.par.Storepreviews.eval()
		prefab.op("preview").lock = self.ownerComp.par.Storepreviews.eval()
		prefab.op("preview").par.top = ""

	def Get_Preset_Comp(self,preset_id) -> COMP :
		"""
			Returns the COMP defining the presets given thepreset_id.
		"""
		return self.preset_folder.op(id) or self.ownerComp.op("emptyPreset")

	def Get_Preset_Name(self,preset_id:str) -> str:
		"""
			Return the Name of a Preset bypreset_id.
		"""
		return self.Get_Preset_Comp(id).par.Name.eval()

	def Get_Preview(self,preset_id:str) -> TOP:
		"""
			Return the TOP showing the preview of the Presets.
		"""

		return self.Get_Preset_Comp(id).op("preview")

	def Store_Preset(self, name:str, tag = '',preset_id = "") -> str:
		"""
			Store the Preset unter the given name. 
			Ifpreset_id is not not supplied thepreset_id will be generated based on Parameters.
		"""
		#creating newpreset_id if nopreset_id given.
		if self.ownerComp.par.Idmode.eval() == "Name":
			name = tdu.legalName( name )
			preset_id = name
		
		preset_id =preset_id or tdu.legalName( str( uuid.uuid4() ) )

		#checking for existing preset
		existing_preset 	= self.preset_folder.op( preset_id ) 

		if existing_preset:
			handle_override = self.ownerComp.par.Handleoverride.eval()
			if handle_override == "Request":
				if not ui.messageBox(
					"Override Preset",
					f"You are about to override the preset with the name {name} andpreset_id {preset_id}. Are you sure?",
					buttons = ["Cancel", "Ok"]
				): return ""
			if handle_override == "Exception":
				raise Exception(f"Preset {preset_id} {name} already exists!")
		#calling update or create, depending on if a preset already exists. 
		preset_comp 		= (self._update_preset if existing_preset else self._create_preset)(name, tag, preset_id)

		#storing the preview
		self.store_prev( preset_comp )
		
		#aranging the node
		TDFunctions.arrangeNode( preset_comp )

		#writing stack to preset-table
		stack_data =  self.ownerComp.op("callbackManager").Do_Callback("getStack", self.ownerComp) or  self.stack.Get_Stack_Dict_List() 
		
		preset_comp.seq.Items.numBlocks = len( stack_data )
		data_seq = preset_comp.seq.Items
		for index,item in enumerate( stack_data ):
			for key, value in item.items():
				data_seq[index].par[key] = value
			pass
		return preset_id
	

		# If enabled, we update existing presets with the current stack.
		if self.ownerComp.par.Pushstacktoallpresets.eval():
			self.Push_Stack_To_Presets()
		return preset_id

	def _create_preset(self, name, tag,preset_id):
		new_preset = self.preset_folder.copy( self.prefab, name =preset_id)
		new_preset.par.Tag 	= tag or self.ownerComp.par.Tag.eval()
		new_preset.par.Name = name
		self.ownerComp.op("callbackManager").Do_Callback(	"onPresetRecord", 
															new_preset.par.Name.eval(), 
															new_preset.par.Tag.eval(), 
															new_preset.name,
															self.ownerComp)
		return new_preset

	def _update_preset(self, name, tag,preset_id):
		preset_comp = self.preset_folder.op(id)
		self.ownerComp.op("callbackManager").Do_Callback(	"onPresetUpdate", 
															preset_comp.par.Name.eval(), 
															preset_comp.par.Tag.eval(), 
															preset_comp.name,
															self.ownerComp)
		return preset_comp

	def Remove_Preset(self,preset_id:str ):
		try:
			self.preset_folder.op(preset_id ).destroy()
		except :
			pass
	
	def Remove_All_Presets(self):
		for preset_comp in self.preset_folder.findChildren( depth = 1):
			preset_comp.destroy()

	def Preset_To_Stack(self,preset_id:str):
		preset_comp = self.preset_folder.op(preset_id )
		if not preset_comp: return
		self.stack.Clear_Stack()

		for target_dict in self.modeler.Table_To_List( preset_comp.op("values") ):
			try:
				self.stack.Add_Par( self.stack.Get_Parameter( target_dict["parOwner"], target_dict["parName"] ), 
								fade_type = target_dict["type"] )
			except AttributeError:
				continue

	def Recall_Preset(self,preset_id:str, time:float, curve = "s", load_stack = False):
		preset_comp = self.preset_folder.op(preset_id )
		self.logger.Log("Recalling preset", preset_id, time, curve, load_stack)
		
		if not preset_comp: 
			if self.ownerComp.par.Handlenopreset.eval() == "Raise Exception": 
				raise self.PresetDoesNotExist()
			return False
		
		self.ownerComp.op("callbackManager").Do_Callback(
			"onPresetRecall", 
			preset_comp.par.Name.eval(), 
			preset_comp.par.Tag.eval(), 
			preset_comp.name,
			self.ownerComp
		)

		if load_stack: self.Preset_To_Stack( preset_id )


		for block in preset_comp.seq.Items:
			parameter = block.par.Parameter.eval()
			if parameter is None: 
				self.logger.Log(
					"Could not find Parameter stored in Preset", 
					id, 
					block.par.Operator.eval(),
					block.par.Parname.eval()
				)
				continue

			self.tweener.CreateTween(	block.par.Parameter.eval(), 
										block.par.Value.eval(), 
										time, 
										type 	= block.par.Type.eval(), 
										curve 	= curve, 
										id 		= preset_comp, 
										mode 	= block.par.Mode.eval(), 
										expression = block.par.Expression.eval() )
		return True
	
	def Rename(self,preset_id:str, new_name:str ):
		preset_comp = self.preset_folder.op(preset_id )
		if not preset_comp: return
		
		if self.ownerComp.par.Renamemode.eval() == "Replacepreset_id":
			new_name = tdu.legalName( new_name )
			preset_comp.name 			= new_name
			preset_comp.par.Name.val 	= new_name
		else:
			preset_comp.par.Name 		= new_name
		return preset_comp

	def Push_Stack_To_Presets(self, 
						   mode:Literal["keep", "overwrite"] 		= "keep", 
						   _stackelements:Union[str, list, tuple] 	= "*", 
						   _presets:Union[str, list, tuple] 			= "*"):
		"""
			Pushes all the parameters of the current stack to all presets.
			When using "overwrite" mode all parameters will b overwritten. CAUTION!
		"""
		stackelements = " ".join( _stackelements ) if isinstance(_stackelements, (list, tuple)) else _stackelements
		presets = " ".join( _presets ) if isinstance(_presets, (list, tuple)) else _presets

		_stackData = { stackElement["id"] : stackElement for stackElement in self.stack.Get_Stack_Dict_List() }
		stackData = { key : _stackData[key] for key in tdu.match( stackelements, list(_stackData.keys()) )}
		presetNames = tdu.match( presets, [ operator.name for operator in self.preset_folder.findChildren(depth = 1) ] )
		for presetName in presetNames:
			preset_comp = self.preset_folder.op( presetName )
			updateData = { stackElement["id"] : stackElement for stackElement in self.modeler.Table_To_List( preset_comp.op("values") ) }
			for key, value in stackData.items():
				if key in updateData and mode == "keep": continue
				updateData[key] = value
			self.modeler.List_To_Table( preset_comp.op("values"), 
										updateData.values() )
		return

	@property
	def PresetParMenuObject(self):
		return tdu.TableMenu(
			self.ownerComp.op("id_to_name"), labelCol = "name"
		)