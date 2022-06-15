# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# From type library 'Structnra.tlb'
# On Wed Jun 15 09:38:46 2022
'Structnra Type Library'
makepy_version = '0.5.01'
python_version = 0x30703f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{0DE25124-3FA2-42E8-8290-25FED76CB878}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IApp(DispatchBaseClass):
	'Dispatch interface for App Object'
	CLSID = IID('{5AAB7F69-EB60-4CF8-B4FA-68EFCDD38186}')
	coclass_clsid = IID('{6D987FB9-FDD1-42D2-A179-46E16CDC0103}')

	def CalculateSingle(self, x=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(207, LCID, 1, (11, 0), ((5, 1),),x
			)

	def CalculateUniform(self):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), (),)

	def CalculateWeighted(self):
		return self._oleobj_.InvokeTypes(210, LCID, 1, (11, 0), (),)

	def Hide(self):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (24, 0), (),)

	def Import(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def ImportStream(self, Stream=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (11, 0), ((13, 1),),Stream
			)

	def Open(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def Reset(self):
		return self._oleobj_.InvokeTypes(203, LCID, 1, (24, 0), (),)

	def SaveAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(202, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def Show(self):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"Accuracy": (209, 2, (3, 0), (), "Accuracy", None),
		"DistributionOfTrajectories": (216, 2, (3, 0), (), "DistributionOfTrajectories", None),
		"LastMessage": (213, 2, (8, 0), (), "LastMessage", None),
		"NumberOfUniformTrajectories": (215, 2, (3, 0), (), "NumberOfUniformTrajectories", None),
		"OLEUser": (214, 2, (8, 0), (), "OLEUser", None),
		"SubStructureSize": (206, 2, (3, 0), (), "SubStructureSize", None),
	}
	_prop_map_put_ = {
		"Accuracy": ((209, LCID, 4, 0),()),
		"DistributionOfTrajectories": ((216, LCID, 4, 0),()),
		"NumberOfUniformTrajectories": ((215, LCID, 4, 0),()),
		"OLEUser": ((214, LCID, 4, 0),()),
		"SubStructureSize": ((206, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ISimnra(DispatchBaseClass):
	CLSID = IID('{AC486B01-7024-4181-BE75-9970C9420104}')
	coclass_clsid = IID('{24660153-1DB4-418B-8F29-034239232515}')

	_prop_map_get_ = {
		"Calc": (202, 2, (12, 0), (), "Calc", None),
		"CrossSec": (208, 2, (12, 0), (), "CrossSec", None),
		"Foil": (203, 2, (12, 0), (), "Foil", None),
		"Forms": (207, 2, (12, 0), (), "Forms", None),
		"Projectile": (205, 2, (12, 0), (), "Projectile", None),
		"Setup": (201, 2, (12, 0), (), "Setup", None),
		"Spectrum": (206, 2, (12, 0), (), "Spectrum", None),
		"Target": (209, 2, (12, 0), (), "Target", None),
		"Window": (204, 2, (12, 0), (), "Window", None),
	}
	_prop_map_put_ = {
		"Calc": ((202, LCID, 4, 0),()),
		"CrossSec": ((208, LCID, 4, 0),()),
		"Foil": ((203, LCID, 4, 0),()),
		"Forms": ((207, LCID, 4, 0),()),
		"Projectile": ((205, LCID, 4, 0),()),
		"Setup": ((201, LCID, 4, 0),()),
		"Spectrum": ((206, LCID, 4, 0),()),
		"Target": ((209, LCID, 4, 0),()),
		"Window": ((204, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IStructure(DispatchBaseClass):
	'Dispatch interface for Structure Object'
	CLSID = IID('{5AAB0DEE-5265-4B56-8136-BF6E14139A5F}')
	coclass_clsid = IID('{21D45C23-6EE9-44E0-BC7D-159F16382679}')

	def AddElement(self, mat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (11, 0), ((3, 1),),mat
			)

	def AddIsotope(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (11, 0), ((3, 1), (3, 1)),mat
			, el)

	def AddMaterial(self):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (11, 0), (),)

	def DeleteAllMaterial(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (11, 0), (),)

	def DeleteElement(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(213, LCID, 1, (11, 0), ((3, 1), (3, 1)),mat
			, el)

	def DeleteIsotope(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (11, 0), ((3, 1), (3, 1), (3, 1)),mat
			, el, iso)

	def DeleteMaterial(self, mat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(216, LCID, 1, (11, 0), ((3, 1),),mat
			)

	# The method ElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentration(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(211, LCID, 2, (5, 0), ((3, 1), (3, 1)),mat
			, el)

	# The method ElementName is actually a property, but must be used as a method to correctly pass the arguments
	def ElementName(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(210, LCID, 2, (8, 0), ((3, 1), (3, 1)),mat
			, el)

	def ElementNameArray(self):
		return self._ApplyTypes_(222, 1, (12, 0), (), 'ElementNameArray', None,)

	# The method IsotopeConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def IsotopeConcentration(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(217, LCID, 2, (5, 0), ((3, 1), (3, 1), (3, 1)),mat
			, el, iso)

	# The method IsotopeMass is actually a property, but must be used as a method to correctly pass the arguments
	def IsotopeMass(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(218, LCID, 2, (5, 0), ((3, 1), (3, 1), (3, 1)),mat
			, el, iso)

	def MakeTargetIn(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(224, LCID, 1, (11, 0), ((5, 1), (5, 1)),x
			, y)

	# The method MaterialADensity is actually a property, but must be used as a method to correctly pass the arguments
	def MaterialADensity(self, mat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(221, LCID, 2, (5, 0), ((3, 1),),mat
			)

	# The method MaterialColor is actually a property, but must be used as a method to correctly pass the arguments
	def MaterialColor(self, mat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 2, (3, 0), ((3, 1),),mat
			)

	# The method MaterialDensity is actually a property, but must be used as a method to correctly pass the arguments
	def MaterialDensity(self, mat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(209, LCID, 2, (5, 0), ((3, 1),),mat
			)

	# The method NumberOfElements is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfElements(self, mat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(206, LCID, 2, (3, 0), ((3, 1),),mat
			)

	# The method NumberOfIsotopes is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfIsotopes(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(207, LCID, 2, (3, 0), ((3, 1), (3, 1)),mat
			, el)

	# The method SetElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentration(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(211, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),mat
			, el, arg2)

	# The method SetElementName is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementName(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(210, LCID, 4, (24, 0), ((3, 1), (3, 1), (8, 1)),mat
			, el, arg2)

	# The method SetIsotopeConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetIsotopeConcentration(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg, arg3=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(217, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1), (5, 1)),mat
			, el, iso, arg3)

	# The method SetIsotopeMass is actually a property, but must be used as a method to correctly pass the arguments
	def SetIsotopeMass(self, mat=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg, arg3=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(218, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1), (5, 1)),mat
			, el, iso, arg3)

	# The method SetMaterialADensity is actually a property, but must be used as a method to correctly pass the arguments
	def SetMaterialADensity(self, mat=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(221, LCID, 4, (24, 0), ((3, 1), (5, 1)),mat
			, arg1)

	# The method SetMaterialColor is actually a property, but must be used as a method to correctly pass the arguments
	def SetMaterialColor(self, mat=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(208, LCID, 4, (24, 0), ((3, 1), (3, 1)),mat
			, arg1)

	# The method SetMaterialDensity is actually a property, but must be used as a method to correctly pass the arguments
	def SetMaterialDensity(self, mat=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(209, LCID, 4, (24, 0), ((3, 1), (5, 1)),mat
			, arg1)

	# The method SetStoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def SetStoppingFactor(self, mat=defaultNamedNotOptArg, Z=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(219, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),mat
			, Z, arg2)

	# The method StoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def StoppingFactor(self, mat=defaultNamedNotOptArg, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(219, LCID, 2, (5, 0), ((3, 1), (3, 1)),mat
			, Z)

	_prop_map_get_ = {
		"Height": (202, 2, (3, 0), (), "Height", None),
		"NumberOfMaterials": (203, 2, (3, 0), (), "NumberOfMaterials", None),
		"PeriodicBoundary": (223, 2, (11, 0), (), "PeriodicBoundary", None),
		"PixelSize": (220, 2, (5, 0), (), "PixelSize", None),
		"Width": (201, 2, (3, 0), (), "Width", None),
	}
	_prop_map_put_ = {
		"Height": ((202, LCID, 4, 0),()),
		"PeriodicBoundary": ((223, LCID, 4, 0),()),
		"PixelSize": ((220, LCID, 4, 0),()),
		"Width": ((201, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'Structnra.App'
class App(CoClassBaseClass): # A CoClass
	# App Object
	CLSID = IID('{6D987FB9-FDD1-42D2-A179-46E16CDC0103}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IApp,
	]
	default_interface = IApp

# This CoClass is known by the name 'Structnra.Simnra'
class Simnra(CoClassBaseClass): # A CoClass
	CLSID = IID('{24660153-1DB4-418B-8F29-034239232515}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ISimnra,
	]
	default_interface = ISimnra

# This CoClass is known by the name 'Structnra.Structure'
class Structure(CoClassBaseClass): # A CoClass
	# Structure Object
	CLSID = IID('{21D45C23-6EE9-44E0-BC7D-159F16382679}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IStructure,
	]
	default_interface = IStructure

IApp_vtables_dispatch_ = 1
IApp_vtables_ = [
	(( 'Open' , 'FileName' , 'Value' , ), 201, (201, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , 'Value' , ), 202, (202, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Reset' , ), 203, (203, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Import' , 'FileName' , 'Value' , ), 204, (204, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ImportStream' , 'Stream' , 'Value' , ), 205, (205, (), [ (13, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SubStructureSize' , 'Value' , ), 206, (206, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SubStructureSize' , 'Value' , ), 206, (206, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'CalculateSingle' , 'x' , 'Value' , ), 207, (207, (), [ (5, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'CalculateUniform' , 'Value' , ), 208, (208, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Accuracy' , 'Value' , ), 209, (209, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Accuracy' , 'Value' , ), 209, (209, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'CalculateWeighted' , 'Value' , ), 210, (210, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Hide' , ), 211, (211, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Show' , ), 212, (212, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'LastMessage' , 'Value' , ), 213, (213, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'OLEUser' , 'Value' , ), 214, (214, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'OLEUser' , 'Value' , ), 214, (214, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfUniformTrajectories' , 'Value' , ), 215, (215, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfUniformTrajectories' , 'Value' , ), 215, (215, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'DistributionOfTrajectories' , 'Value' , ), 216, (216, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'DistributionOfTrajectories' , 'Value' , ), 216, (216, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
]

ISimnra_vtables_dispatch_ = 1
ISimnra_vtables_ = [
	(( 'Setup' , 'Value' , ), 201, (201, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Setup' , 'Value' , ), 201, (201, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Calc' , 'Value' , ), 202, (202, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Calc' , 'Value' , ), 202, (202, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Foil' , 'Value' , ), 203, (203, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Foil' , 'Value' , ), 203, (203, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Window' , 'Value' , ), 204, (204, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Window' , 'Value' , ), 204, (204, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Projectile' , 'Value' , ), 205, (205, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Projectile' , 'Value' , ), 205, (205, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Spectrum' , 'Value' , ), 206, (206, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Spectrum' , 'Value' , ), 206, (206, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Forms' , 'Value' , ), 207, (207, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Forms' , 'Value' , ), 207, (207, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'CrossSec' , 'Value' , ), 208, (208, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'CrossSec' , 'Value' , ), 208, (208, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Target' , 'Value' , ), 209, (209, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'Target' , 'Value' , ), 209, (209, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
]

IStructure_vtables_dispatch_ = 1
IStructure_vtables_ = [
	(( 'Width' , 'Value' , ), 201, (201, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Width' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Height' , 'Value' , ), 202, (202, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Height' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfMaterials' , 'Value' , ), 203, (203, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'AddMaterial' , 'Value' , ), 204, (204, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'DeleteAllMaterial' , 'Value' , ), 205, (205, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfElements' , 'mat' , 'Value' , ), 206, (206, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfIsotopes' , 'mat' , 'el' , 'Value' , ), 207, (207, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'MaterialColor' , 'mat' , 'Value' , ), 208, (208, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'MaterialColor' , 'mat' , 'Value' , ), 208, (208, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'MaterialDensity' , 'mat' , 'Value' , ), 209, (209, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'MaterialDensity' , 'mat' , 'Value' , ), 209, (209, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'mat' , 'el' , 'Value' , ), 210, (210, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'mat' , 'el' , 'Value' , ), 210, (210, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'mat' , 'el' , 'Value' , ), 211, (211, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'mat' , 'el' , 'Value' , ), 211, (211, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'AddElement' , 'mat' , 'Value' , ), 212, (212, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'DeleteElement' , 'mat' , 'el' , 'Value' , ), 213, (213, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'AddIsotope' , 'mat' , 'el' , 'Value' , ), 214, (214, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'DeleteIsotope' , 'mat' , 'el' , 'iso' , 'Value' , 
			 ), 215, (215, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'DeleteMaterial' , 'mat' , 'Value' , ), 216, (216, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeConcentration' , 'mat' , 'el' , 'iso' , 'Value' , 
			 ), 217, (217, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeConcentration' , 'mat' , 'el' , 'iso' , 'Value' , 
			 ), 217, (217, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeMass' , 'mat' , 'el' , 'iso' , 'Value' , 
			 ), 218, (218, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeMass' , 'mat' , 'el' , 'iso' , 'Value' , 
			 ), 218, (218, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'mat' , 'Z' , 'Value' , ), 219, (219, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'mat' , 'Z' , 'Value' , ), 219, (219, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'PixelSize' , 'Value' , ), 220, (220, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'PixelSize' , 'Value' , ), 220, (220, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'MaterialADensity' , 'mat' , 'Value' , ), 221, (221, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'MaterialADensity' , 'mat' , 'Value' , ), 221, (221, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'ElementNameArray' , 'Value' , ), 222, (222, (), [ (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'PeriodicBoundary' , 'Value' , ), 223, (223, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'PeriodicBoundary' , 'Value' , ), 223, (223, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'MakeTargetIn' , 'x' , 'y' , 'Value' , ), 224, (224, (), [ 
			 (5, 1, None, None) , (5, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{5AAB7F69-EB60-4CF8-B4FA-68EFCDD38186}' : IApp,
	'{6D987FB9-FDD1-42D2-A179-46E16CDC0103}' : App,
	'{5AAB0DEE-5265-4B56-8136-BF6E14139A5F}' : IStructure,
	'{21D45C23-6EE9-44E0-BC7D-159F16382679}' : Structure,
	'{AC486B01-7024-4181-BE75-9970C9420104}' : ISimnra,
	'{24660153-1DB4-418B-8F29-034239232515}' : Simnra,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{5AAB7F69-EB60-4CF8-B4FA-68EFCDD38186}' : 'IApp',
	'{5AAB0DEE-5265-4B56-8136-BF6E14139A5F}' : 'IStructure',
	'{AC486B01-7024-4181-BE75-9970C9420104}' : 'ISimnra',
}


NamesToIIDMap = {
	'IApp' : '{5AAB7F69-EB60-4CF8-B4FA-68EFCDD38186}',
	'IStructure' : '{5AAB0DEE-5265-4B56-8136-BF6E14139A5F}',
	'ISimnra' : '{AC486B01-7024-4181-BE75-9970C9420104}',
}


