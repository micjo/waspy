# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 22:22:05) [MSC v.1916 64 bit (AMD64)]
# From type library 'Simnra.exe'
# On Wed Jun 15 11:11:18 2022
'Simnra Type Library'
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

CLSID = IID('{9F51F4E0-754F-11D5-B742-0040332FCEB4}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IApp(DispatchBaseClass):
	'Dispatch interface for App Object'
	CLSID = IID('{9F51F4E1-754F-11D5-B742-0040332FCEB4}')
	coclass_clsid = IID('{9F51F4E3-754F-11D5-B742-0040332FCEB4}')

	def BringToFront(self):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (24, 0), (),)

	def BringToRear(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (24, 0), (),)

	def CalculateDualScatteringBackground(self, AddToSpectrum=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(221, LCID, 1, (11, 0), ((11, 1),),AddToSpectrum
			)

	def CalculatePileup(self):
		return self._oleobj_.InvokeTypes(220, LCID, 1, (11, 0), (),)

	def CalculateSpectrum(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), (),)

	def CalculateSpectrumFast(self):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (11, 0), (),)

	def CalculateSpectrumFromTargets(self, V=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(228, LCID, 1, (11, 0), ((12, 1),),V
			)

	def CalculateSpectrumFromTargetsFast(self, V=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(229, LCID, 1, (11, 0), ((12, 1),),V
			)

	def CalculateSpectrumToDepth(self, Depth=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((5, 1),),Depth
			)

	def Copy(self, App1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(226, LCID, 1, (11, 0), ((13, 1),),App1
			)

	def CopySpectrumData(self):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (24, 0), (),)

	def CreateListOfCrSecs(self):
		return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), (),)

	def FitSpectrum(self):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (11, 0), (),)

	def GetThumbnailAsVariant(self, Width=defaultNamedNotOptArg):
		return self._ApplyTypes_(231, 1, (12, 0), ((3, 1),), 'GetThumbnailAsVariant', None,Width
			)

	def Hide(self):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (24, 0), (),)

	def Maximize(self):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), (),)

	def Minimize(self):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

	def Open(self, FileName=defaultNamedNotOptArg, FileType=-1):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((8, 1), (3, 33)),FileName
			, FileType)

	def OpenAs(self, FileName=defaultNamedNotOptArg, FileType=-1):
		return self._oleobj_.InvokeTypes(202, LCID, 1, (11, 0), ((8, 1), (3, 49)),FileName
			, FileType)

	def OpenMemory(self, S=defaultNamedNotOptArg, FileType=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(224, LCID, 1, (11, 0), ((8, 1), (3, 1)),S
			, FileType)

	def OpenStream(self, Stream=defaultNamedNotOptArg, FileType=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), ((13, 1), (3, 1)),Stream
			, FileType)

	def ReadSpectrumData(self, FileName=defaultNamedNotOptArg, Format=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), ((8, 1), (3, 1)),FileName
			, Format)

	def Reset(self):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (24, 0), (),)

	def ResizeSpectrum(self, NumChannels=defaultNamedNotOptArg, ResizeCalibration=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(216, LCID, 1, (24, 0), ((3, 1), (11, 1)),NumChannels
			, ResizeCalibration)

	def Restore(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), (),)

	def SaveAs(self, FileName=defaultNamedNotOptArg, FileType=2):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((8, 1), (3, 49)),FileName
			, FileType)

	def SaveMemory(self, WS=pythoncom.Missing):
		return self._ApplyTypes_(225, 1, (11, 0), ((16392, 2),), 'SaveMemory', None,WS
			)

	def SaveThumbnailAs(self, FileName=defaultNamedNotOptArg, Width=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, Width)

	def Show(self):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (24, 0), (),)

	def Standalone(self):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (11, 0), (),)

	def WriteSpectrumData(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	_prop_map_get_ = {
		"Active": (10, 2, (11, 0), (), "Active", None),
		"BorderStyle": (217, 2, (3, 0), (), "BorderStyle", None),
		"CalculatingSpectrum": (19, 2, (11, 0), (), "CalculatingSpectrum", None),
		"DeleteSpectrumOnCalculate": (14, 2, (11, 0), (), "DeleteSpectrumOnCalculate", None),
		"FileName": (21, 2, (8, 0), (), "FileName", None),
		"Height": (26, 2, (3, 0), (), "Height", None),
		"IncidentIonEnergyIsZero": (209, 2, (11, 0), (), "IncidentIonEnergyIsZero", None),
		"LastMessage": (16, 2, (8, 0), (), "LastMessage", None),
		"Left": (23, 2, (3, 0), (), "Left", None),
		"LegendOutsideOfChart": (206, 2, (11, 0), (), "LegendOutsideOfChart", None),
		"LegendVisible": (203, 2, (11, 0), (), "LegendVisible", None),
		"MenuVisible": (213, 2, (11, 0), (), "MenuVisible", None),
		"OLEUser": (218, 2, (8, 0), (), "OLEUser", None),
		"Priority": (227, 2, (19, 0), (), "Priority", None),
		"SRIMDirectory": (219, 2, (8, 0), (), "SRIMDirectory", None),
		"ShowMessages": (15, 2, (11, 0), (), "ShowMessages", None),
		"SimulationMode": (230, 2, (3, 0), (), "SimulationMode", None),
		"SpectrumChanged": (20, 2, (11, 0), (), "SpectrumChanged", None),
		"StatusbarVisible": (214, 2, (11, 0), (), "StatusbarVisible", None),
		"TargetOutItemVisible": (223, 2, (11, 0), (), "TargetOutItemVisible", None),
		"ToolbarVisible": (212, 2, (11, 0), (), "ToolbarVisible", None),
		"Top": (25, 2, (3, 0), (), "Top", None),
		"TopAxisCaption": (207, 2, (8, 0), (), "TopAxisCaption", None),
		"Version": (27, 2, (8, 0), (), "Version", None),
		"Visible": (210, 2, (11, 0), (), "Visible", None),
		"Width": (24, 2, (3, 0), (), "Width", None),
	}
	_prop_map_put_ = {
		"BorderStyle": ((217, LCID, 4, 0),()),
		"CloseButtonEnabled": ((222, LCID, 4, 0),()),
		"ControlsVisible": ((215, LCID, 4, 0),()),
		"DeleteSpectrumOnCalculate": ((14, LCID, 4, 0),()),
		"Height": ((26, LCID, 4, 0),()),
		"IncidentIonEnergyIsZero": ((209, LCID, 4, 0),()),
		"Left": ((23, LCID, 4, 0),()),
		"LegendOutsideOfChart": ((206, LCID, 4, 0),()),
		"LegendVisible": ((203, LCID, 4, 0),()),
		"MenuVisible": ((213, LCID, 4, 0),()),
		"OLEUser": ((218, LCID, 4, 0),()),
		"Priority": ((227, LCID, 4, 0),()),
		"SRIMDirectory": ((219, LCID, 4, 0),()),
		"ShowMessages": ((15, LCID, 4, 0),()),
		"SimulationMode": ((230, LCID, 4, 0),()),
		"SpectrumChanged": ((20, LCID, 4, 0),()),
		"StatusbarVisible": ((214, LCID, 4, 0),()),
		"TargetOutItemVisible": ((223, LCID, 4, 0),()),
		"ToolbarVisible": ((212, LCID, 4, 0),()),
		"Top": ((25, LCID, 4, 0),()),
		"TopAxisCaption": ((207, LCID, 4, 0),()),
		"Width": ((24, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICalc(DispatchBaseClass):
	CLSID = IID('{9DD33B20-A8EC-11D5-B749-0040332FCEB4}')
	coclass_clsid = IID('{9DD33B22-A8EC-11D5-B749-0040332FCEB4}')

	def Copy(self, Calc1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (11, 0), ((13, 1),),Calc1
			)

	def Open(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def OpenAs(self, FileName=defaultNamedNotOptArg, FileType=-1):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (11, 0), ((8, 1), (3, 49)),FileName
			, FileType)

	def OpenMemory(self, WS=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(209, LCID, 1, (11, 0), ((8, 1),),WS
			)

	def SaveAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def SaveAsDefault(self):
		return self._oleobj_.InvokeTypes(213, LCID, 1, (11, 0), (),)

	def SaveMemory(self, WS=pythoncom.Missing):
		return self._ApplyTypes_(210, 1, (11, 0), ((16392, 2),), 'SaveMemory', None,WS
			)

	_prop_map_get_ = {
		"Accuracy": (207, 2, (3, 0), (), "Accuracy", None),
		"AutoStepwidthIn": (8, 2, (11, 0), (), "AutoStepwidthIn", None),
		"AutoStepwidthOut": (9, 2, (11, 0), (), "AutoStepwidthOut", None),
		"CalculateToEMin": (208, 2, (11, 0), (), "CalculateToEMin", None),
		"CreateSpectrum": (21, 2, (11, 0), (), "CreateSpectrum", None),
		"CreateSpectrumFromLayerNr": (206, 2, (3, 0), (), "CreateSpectrumFromLayerNr", None),
		"CrossSecStraggling": (201, 2, (3, 0), (), "CrossSecStraggling", None),
		"DualScattering": (6, 2, (11, 0), (), "DualScattering", None),
		"DualScatteringRoughness": (203, 2, (3, 0), (), "DualScatteringRoughness", None),
		"ElementSpectra": (12, 2, (11, 0), (), "ElementSpectra", None),
		"Emin": (3, 2, (5, 0), (), "Emin", None),
		"GeometricalStraggling": (216, 2, (11, 0), (), "GeometricalStraggling", None),
		"HighEnergyStopping": (15, 2, (11, 0), (), "HighEnergyStopping", None),
		"IsotopeSpectra": (13, 2, (11, 0), (), "IsotopeSpectra", None),
		"Isotopes": (5, 2, (11, 0), (), "Isotopes", None),
		"LogFile": (20, 2, (11, 0), (), "LogFile", None),
		"MultipleScattering": (7, 2, (11, 0), (), "MultipleScattering", None),
		"MultipleScatteringModel": (217, 2, (3, 0), (), "MultipleScatteringModel", None),
		"NuclearStoppingModel": (205, 2, (3, 0), (), "NuclearStoppingModel", None),
		"NumberOfAngleVariations": (11, 2, (3, 0), (), "NumberOfAngleVariations", None),
		"NumberOfDVariations": (10, 2, (3, 0), (), "NumberOfDVariations", None),
		"PUModel": (19, 2, (3, 0), (), "PUModel", None),
		"ScreeningModel": (18, 2, (3, 0), (), "ScreeningModel", None),
		"StoppingModel": (204, 2, (3, 0), (), "StoppingModel", None),
		"Straggling": (4, 2, (11, 0), (), "Straggling", None),
		"StragglingModel": (17, 2, (3, 0), (), "StragglingModel", None),
		"StragglingShape": (202, 2, (3, 0), (), "StragglingShape", None),
		"SubstrateRoughnessDimension": (16, 2, (3, 0), (), "SubstrateRoughnessDimension", None),
		"ZBStopping": (14, 2, (11, 0), (), "ZBStopping", None),
		"dEin": (1, 2, (5, 0), (), "dEin", None),
		"dEout": (2, 2, (5, 0), (), "dEout", None),
	}
	_prop_map_put_ = {
		"AutoStepwidthIn": ((8, LCID, 4, 0),()),
		"AutoStepwidthOut": ((9, LCID, 4, 0),()),
		"CalculateToEMin": ((208, LCID, 4, 0),()),
		"CreateSpectrum": ((21, LCID, 4, 0),()),
		"CreateSpectrumFromLayerNr": ((206, LCID, 4, 0),()),
		"CrossSecStraggling": ((201, LCID, 4, 0),()),
		"DualScattering": ((6, LCID, 4, 0),()),
		"DualScatteringRoughness": ((203, LCID, 4, 0),()),
		"ElementSpectra": ((12, LCID, 4, 0),()),
		"Emin": ((3, LCID, 4, 0),()),
		"GeometricalStraggling": ((216, LCID, 4, 0),()),
		"HighEnergyStopping": ((15, LCID, 4, 0),()),
		"IsotopeSpectra": ((13, LCID, 4, 0),()),
		"Isotopes": ((5, LCID, 4, 0),()),
		"LogFile": ((20, LCID, 4, 0),()),
		"MultipleScattering": ((7, LCID, 4, 0),()),
		"MultipleScatteringModel": ((217, LCID, 4, 0),()),
		"NuclearStoppingModel": ((205, LCID, 4, 0),()),
		"NumberOfAngleVariations": ((11, LCID, 4, 0),()),
		"NumberOfDVariations": ((10, LCID, 4, 0),()),
		"PUModel": ((19, LCID, 4, 0),()),
		"ScreeningModel": ((18, LCID, 4, 0),()),
		"StoppingModel": ((204, LCID, 4, 0),()),
		"Straggling": ((4, LCID, 4, 0),()),
		"StragglingModel": ((17, LCID, 4, 0),()),
		"StragglingShape": ((202, LCID, 4, 0),()),
		"SubstrateRoughnessDimension": ((16, LCID, 4, 0),()),
		"ZBStopping": ((14, LCID, 4, 0),()),
		"dEin": ((1, LCID, 4, 0),()),
		"dEout": ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ICrossSec(DispatchBaseClass):
	CLSID = IID('{1C467EA5-494F-4FA4-A305-84183157CC48}')
	coclass_clsid = IID('{504EF515-68CF-495D-8D7C-C132E538D839}')

	# The method Choose is actually a property, but must be used as a method to correctly pass the arguments
	def Choose(self, Index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 2, (11, 0), ((3, 1),),Index
			)

	# The method EMax is actually a property, but must be used as a method to correctly pass the arguments
	def EMax(self, Index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(211, LCID, 2, (5, 0), ((3, 1),),Index
			)

	def ERDRutherford(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, Z2=defaultNamedNotOptArg, M2=defaultNamedNotOptArg
			, E=defaultNamedNotOptArg, Phi=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (5, 0), ((3, 1), (5, 1), (3, 1), (5, 1), (5, 1), (5, 1)),Z1
			, M1, Z2, M2, E, Phi
			)

	# The method Emin is actually a property, but must be used as a method to correctly pass the arguments
	def Emin(self, Index=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(210, LCID, 2, (5, 0), ((3, 1),),Index
			)

	# The method FileName is actually a property, but must be used as a method to correctly pass the arguments
	def FileName(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(207, LCID, 2, (8, 0), ((3, 1),),Index
			)

	# The method Info is actually a property, but must be used as a method to correctly pass the arguments
	def Info(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(209, LCID, 2, (8, 0), ((3, 1),),Index
			)

	def RBSRutherford(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, Z2=defaultNamedNotOptArg, M2=defaultNamedNotOptArg
			, E=defaultNamedNotOptArg, Theta=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (5, 0), ((3, 1), (5, 1), (3, 1), (5, 1), (5, 1), (5, 1)),Z1
			, M1, Z2, M2, E, Theta
			)

	def SelectReactions(self):
		return self._oleobj_.InvokeTypes(219, LCID, 1, (24, 0), (),)

	def SelectRutherford(self, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (24, 0), ((3, 1),),Z
			)

	def SelectRutherfordAll(self):
		return self._oleobj_.InvokeTypes(202, LCID, 1, (24, 0), (),)

	def SelectSigmaCalc(self, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (24, 0), ((3, 1),),Z
			)

	def SelectSigmaCalcAll(self):
		return self._oleobj_.InvokeTypes(213, LCID, 1, (24, 0), (),)

	# The method SetChoose is actually a property, but must be used as a method to correctly pass the arguments
	def SetChoose(self, Index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(208, LCID, 4, (24, 0), ((3, 1), (11, 1)),Index
			, arg1)

	# The method SetEMax is actually a property, but must be used as a method to correctly pass the arguments
	def SetEMax(self, Index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(211, LCID, 4, (24, 0), ((3, 1), (5, 1)),Index
			, arg1)

	# The method SetEmin is actually a property, but must be used as a method to correctly pass the arguments
	def SetEmin(self, Index=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(210, LCID, 4, (24, 0), ((3, 1), (5, 1)),Index
			, arg1)

	# The method Title is actually a property, but must be used as a method to correctly pass the arguments
	def Title(self, Index=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(206, LCID, 2, (8, 0), ((3, 1),),Index
			)

	def UniversalEMax(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, Z2=defaultNamedNotOptArg, M2=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (5, 0), ((3, 1), (5, 1), (3, 1), (5, 1)),Z1
			, M1, Z2, M2)

	def Unselect(self, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(216, LCID, 1, (24, 0), ((3, 1),),Z
			)

	def UnselectAll(self):
		return self._oleobj_.InvokeTypes(217, LCID, 1, (24, 0), (),)

	def UnselectRutherford(self, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(203, LCID, 1, (24, 0), ((3, 1),),Z
			)

	def UnselectRutherfordAll(self):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (24, 0), (),)

	def UnselectSigmaCalc(self, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (24, 0), ((3, 1),),Z
			)

	def UnselectSigmaCalcAll(self):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
		"Count": (205, 2, (3, 0), (), "Count", None),
		"ReactionsChoosen": (218, 2, (11, 0), (), "ReactionsChoosen", None),
	}
	_prop_map_put_ = {
		"ReactionsChoosen": ((218, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)
	#This class has Count() property - allow len(ob) to provide this
	def __len__(self):
		return self._ApplyTypes_(*(205, 2, (3, 0), (), "Count", None))
	#This class has a __len__ - this is needed so 'if object:' always returns TRUE.
	def __nonzero__(self):
		return True

class IFit(DispatchBaseClass):
	'Dispatch interface for Fit Object'
	CLSID = IID('{54207F20-9D23-11D5-B748-0040332FCEB4}')
	coclass_clsid = IID('{54207F22-9D23-11D5-B748-0040332FCEB4}')

	def Chi2(self):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (5, 0), (),)

	# The method RegionMaxChannel is actually a property, but must be used as a method to correctly pass the arguments
	def RegionMaxChannel(self, reg=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 2, (3, 0), ((3, 1),),reg
			)

	# The method RegionMinChannel is actually a property, but must be used as a method to correctly pass the arguments
	def RegionMinChannel(self, reg=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 2, (3, 0), ((3, 1),),reg
			)

	# The method SetRegionMaxChannel is actually a property, but must be used as a method to correctly pass the arguments
	def SetRegionMaxChannel(self, reg=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(9, LCID, 4, (24, 0), ((3, 1), (3, 1)),reg
			, arg1)

	# The method SetRegionMinChannel is actually a property, but must be used as a method to correctly pass the arguments
	def SetRegionMinChannel(self, reg=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(8, LCID, 4, (24, 0), ((3, 1), (3, 1)),reg
			, arg1)

	_prop_map_get_ = {
		"Accuracy": (11, 2, (5, 0), (), "Accuracy", None),
		"Chi2Evaluation": (13, 2, (3, 0), (), "Chi2Evaluation", None),
		"EnergyCalibration": (2, 2, (11, 0), (), "EnergyCalibration", None),
		"LayerComposition": (5, 2, (11, 0), (), "LayerComposition", None),
		"LayerNr": (6, 2, (3, 0), (), "LayerNr", None),
		"LayerRoughness": (12, 2, (11, 0), (), "LayerRoughness", None),
		"LayerThickness": (4, 2, (11, 0), (), "LayerThickness", None),
		"MaxIterations": (10, 2, (3, 0), (), "MaxIterations", None),
		"NumberOfRegions": (7, 2, (3, 0), (), "NumberOfRegions", None),
		"ParticlesSr": (3, 2, (11, 0), (), "ParticlesSr", None),
	}
	_prop_map_put_ = {
		"Accuracy": ((11, LCID, 4, 0),()),
		"Chi2Evaluation": ((13, LCID, 4, 0),()),
		"EnergyCalibration": ((2, LCID, 4, 0),()),
		"LayerComposition": ((5, LCID, 4, 0),()),
		"LayerNr": ((6, LCID, 4, 0),()),
		"LayerRoughness": ((12, LCID, 4, 0),()),
		"LayerThickness": ((4, LCID, 4, 0),()),
		"MaxIterations": ((10, LCID, 4, 0),()),
		"NumberOfRegions": ((7, LCID, 4, 0),()),
		"ParticlesSr": ((3, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IFoil(DispatchBaseClass):
	'Dispatch interface for Foil Object'
	CLSID = IID('{FF8D5AF3-63B8-42B5-B3EC-511F561E51F8}')
	coclass_clsid = IID('{F14C14DC-62BD-4C60-9710-A05CA0151546}')

	def AddElement(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (11, 0), ((3, 1),),lay
			)

	def AddLayer(self):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (11, 0), (),)

	def Copy(self, Foil1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(210, LCID, 1, (11, 0), ((13, 1),),Foil1
			)

	def DeleteAllLayer(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (11, 0), (),)

	def DeleteElement(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, el)

	def DeleteLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method ElementAmount is actually a property, but must be used as a method to correctly pass the arguments
	def ElementAmount(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(6, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementName is actually a property, but must be used as a method to correctly pass the arguments
	def ElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(12, LCID, 2, (8, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def ElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(207, LCID, 2, (3, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method HasLayerPorosity is actually a property, but must be used as a method to correctly pass the arguments
	def HasLayerPorosity(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 2, (11, 0), ((3, 1),),lay
			)

	# The method HasLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def HasLayerRoughness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 2, (11, 0), ((3, 1),),lay
			)

	def InsertLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(8, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method LayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerRoughness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method LayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerThickness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method NumberOfElements is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfElements(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 2, (3, 0), ((3, 1),),lay
			)

	def OpenMemory(self, WS=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), ((8, 1),),WS
			)

	# The method PoreDiameter is actually a property, but must be used as a method to correctly pass the arguments
	def PoreDiameter(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(203, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method PorosityFraction is actually a property, but must be used as a method to correctly pass the arguments
	def PorosityFraction(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(202, LCID, 2, (5, 0), ((3, 1),),lay
			)

	def ReadFoil(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def ReadLayer(self, FileName=defaultNamedNotOptArg, LayerNr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, LayerNr)

	def SaveFoilAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def SaveLayerAs(self, FileName=defaultNamedNotOptArg, LayerNr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, LayerNr)

	def SaveMemory(self, WS=pythoncom.Missing):
		return self._ApplyTypes_(209, 1, (11, 0), ((16392, 2),), 'SaveMemory', None,WS
			)

	# The method SetElementAmount is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementAmount(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(13, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(6, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementName is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(12, LCID, 4, (24, 0), ((3, 1), (3, 1), (8, 1)),lay
			, el, arg2)

	# The method SetElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(207, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, arg2)

	# The method SetHasLayerPorosity is actually a property, but must be used as a method to correctly pass the arguments
	def SetHasLayerPorosity(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(201, LCID, 4, (24, 0), ((3, 1), (11, 1)),lay
			, arg1)

	# The method SetHasLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def SetHasLayerRoughness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(4, LCID, 4, (24, 0), ((3, 1), (11, 1)),lay
			, arg1)

	# The method SetLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerRoughness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(3, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetLayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerThickness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(1, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetPoreDiameter is actually a property, but must be used as a method to correctly pass the arguments
	def SetPoreDiameter(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(203, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetPorosityFraction is actually a property, but must be used as a method to correctly pass the arguments
	def SetPorosityFraction(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(202, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetStoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def SetStoppingFactor(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(206, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, Z, arg2)

	# The method StoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def StoppingFactor(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(206, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, Z)

	_prop_map_get_ = {
		"NumberOfLayers": (2, 2, (3, 0), (), "NumberOfLayers", None),
		"Thickness": (204, 2, (5, 0), (), "Thickness", None),
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IForms(DispatchBaseClass):
	CLSID = IID('{A9E30D30-9792-4EF5-B5FE-81446FF50084}')
	coclass_clsid = IID('{E31D2D47-3E2E-418B-93E3-8A8C72A7E6C2}')

	def ShowReactions(self):
		return self._oleobj_.InvokeTypes(206, LCID, 1, (24, 0), (),)

	def ShowSetupCalculation(self):
		return self._oleobj_.InvokeTypes(202, LCID, 1, (24, 0), (),)

	def ShowSetupDetector(self):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (24, 0), (),)

	def ShowSetupExperiment(self):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (24, 0), (),)

	def ShowSetupGeometry(self):
		return self._oleobj_.InvokeTypes(203, LCID, 1, (24, 0), (),)

	def ShowSetupPileup(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (24, 0), (),)

	def ShowTargetFoil(self):
		return self._oleobj_.InvokeTypes(207, LCID, 1, (24, 0), (),)

	def ShowTargetTarget(self):
		return self._oleobj_.InvokeTypes(213, LCID, 1, (24, 0), (),)

	def ShowTargetWindow(self):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (24, 0), (),)

	def ShowToolsDataReader(self):
		return self._oleobj_.InvokeTypes(209, LCID, 1, (24, 0), (),)

	def ShowToolsIntegrateSpectrum(self):
		return self._oleobj_.InvokeTypes(210, LCID, 1, (24, 0), (),)

	def ShowToolsNearestElements(self):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (24, 0), (),)

	def ShowToolsSmoothed(self):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (24, 0), (),)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IPIGE(DispatchBaseClass):
	CLSID = IID('{A1F901AC-0EAB-485A-9945-A55DFC7E95D7}')
	coclass_clsid = IID('{AB1B23A1-601F-465B-B2DB-F4BC15421B62}')

	def Counts(self, n=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(203, LCID, 1, (5, 0), ((3, 1),),n
			)

	def E(self, n=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(202, LCID, 1, (5, 0), ((3, 1),),n
			)

	_prop_map_get_ = {
		"NumberOfGammas": (201, 2, (3, 0), (), "NumberOfGammas", None),
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IProjectile(DispatchBaseClass):
	CLSID = IID('{2486C206-2AE3-4D27-8B96-F3384714119A}')
	coclass_clsid = IID('{AB9D3C37-2FA9-434A-8959-8C84A8F50C97}')

	def Copy(self, P=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (11, 0), ((13, 1),),P
			)

	_prop_map_get_ = {
		"Charge": (5, 2, (3, 0), (), "Charge", None),
		"Mass": (6, 2, (5, 0), (), "Mass", None),
		"Name": (4, 2, (8, 0), (), "Name", None),
	}
	_prop_map_put_ = {
		"Charge": ((5, LCID, 4, 0),()),
		"Mass": ((6, LCID, 4, 0),()),
		"Name": ((4, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ISetup(DispatchBaseClass):
	'Dispatch interface for Setup Object'
	CLSID = IID('{C22A1430-9329-11D5-B743-0040332FCEB4}')
	coclass_clsid = IID('{C22A1432-9329-11D5-B743-0040332FCEB4}')

	def Copy(self, Setup1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(210, LCID, 1, (11, 0), ((13, 1),),Setup1
			)

	def Open(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(206, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def OpenAs(self, FileName=defaultNamedNotOptArg, FileType=-1):
		return self._oleobj_.InvokeTypes(207, LCID, 1, (11, 0), ((8, 1), (3, 33)),FileName
			, FileType)

	def OpenMemory(self, WS=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), ((8, 1),),WS
			)

	def ReadDetectorSensitivity(self, FileName=defaultNamedNotOptArg, Format=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 1, (11, 0), ((8, 1), (3, 1)),FileName
			, Format)

	def SaveAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def SaveAsDefault(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (11, 0), (),)

	def SaveMemory(self, WS=pythoncom.Missing):
		return self._ApplyTypes_(209, 1, (11, 0), ((16392, 2),), 'SaveMemory', None,WS
			)

	def SetBeta(self, Geometry=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (5, 0), ((3, 1),),Geometry
			)

	_prop_map_get_ = {
		"Alpha": (3, 2, (5, 0), (), "Alpha", None),
		"ApertureDistance": (218, 2, (5, 0), (), "ApertureDistance", None),
		"ApertureHeight": (217, 2, (5, 0), (), "ApertureHeight", None),
		"ApertureShape": (215, 2, (3, 0), (), "ApertureShape", None),
		"ApertureWidth": (216, 2, (5, 0), (), "ApertureWidth", None),
		"BeamHeight": (213, 2, (5, 0), (), "BeamHeight", None),
		"BeamShape": (211, 2, (3, 0), (), "BeamShape", None),
		"BeamWidth": (212, 2, (5, 0), (), "BeamWidth", None),
		"Beamspread": (10, 2, (5, 0), (), "Beamspread", None),
		"Beta": (4, 2, (5, 0), (), "Beta", None),
		"CalibrationLinear": (7, 2, (5, 0), (), "CalibrationLinear", None),
		"CalibrationOffset": (6, 2, (5, 0), (), "CalibrationOffset", None),
		"CalibrationQuadratic": (8, 2, (5, 0), (), "CalibrationQuadratic", None),
		"DetectorPosition": (214, 2, (3, 0), (), "DetectorPosition", None),
		"DetectorResolution": (9, 2, (5, 0), (), "DetectorResolution", None),
		"DetectorSensitivity": (202, 2, (3, 0), (), "DetectorSensitivity", None),
		"DetectorSensitivityFileName": (203, 2, (8, 0), (), "DetectorSensitivityFileName", None),
		"DetectorType": (19, 2, (3, 0), (), "DetectorType", None),
		"Energy": (1, 2, (5, 0), (), "Energy", None),
		"LTCorrection": (16, 2, (11, 0), (), "LTCorrection", None),
		"LifeTime": (12, 2, (5, 0), (), "LifeTime", None),
		"LiveTime": (18, 2, (5, 0), (), "LiveTime", None),
		"PUCalculation": (17, 2, (11, 0), (), "PUCalculation", None),
		"PUROn": (15, 2, (11, 0), (), "PUROn", None),
		"PURResolution": (14, 2, (5, 0), (), "PURResolution", None),
		"ParticlesSr": (5, 2, (5, 0), (), "ParticlesSr", None),
		"RealTime": (11, 2, (5, 0), (), "RealTime", None),
		"RiseTime": (13, 2, (5, 0), (), "RiseTime", None),
		"TOFLength": (20, 2, (5, 0), (), "TOFLength", None),
		"TOFTimeResolution": (21, 2, (5, 0), (), "TOFTimeResolution", None),
		"Theta": (2, 2, (5, 0), (), "Theta", None),
	}
	_prop_map_put_ = {
		"Alpha": ((3, LCID, 4, 0),()),
		"ApertureDistance": ((218, LCID, 4, 0),()),
		"ApertureHeight": ((217, LCID, 4, 0),()),
		"ApertureShape": ((215, LCID, 4, 0),()),
		"ApertureWidth": ((216, LCID, 4, 0),()),
		"BeamHeight": ((213, LCID, 4, 0),()),
		"BeamShape": ((211, LCID, 4, 0),()),
		"BeamWidth": ((212, LCID, 4, 0),()),
		"Beamspread": ((10, LCID, 4, 0),()),
		"Beta": ((4, LCID, 4, 0),()),
		"CalibrationLinear": ((7, LCID, 4, 0),()),
		"CalibrationOffset": ((6, LCID, 4, 0),()),
		"CalibrationQuadratic": ((8, LCID, 4, 0),()),
		"DetectorPosition": ((214, LCID, 4, 0),()),
		"DetectorResolution": ((9, LCID, 4, 0),()),
		"DetectorSensitivity": ((202, LCID, 4, 0),()),
		"DetectorType": ((19, LCID, 4, 0),()),
		"Energy": ((1, LCID, 4, 0),()),
		"LTCorrection": ((16, LCID, 4, 0),()),
		"LifeTime": ((12, LCID, 4, 0),()),
		"LiveTime": ((18, LCID, 4, 0),()),
		"PUCalculation": ((17, LCID, 4, 0),()),
		"PUROn": ((15, LCID, 4, 0),()),
		"PURResolution": ((14, LCID, 4, 0),()),
		"ParticlesSr": ((5, LCID, 4, 0),()),
		"RealTime": ((11, LCID, 4, 0),()),
		"RiseTime": ((13, LCID, 4, 0),()),
		"TOFLength": ((20, LCID, 4, 0),()),
		"TOFTimeResolution": ((21, LCID, 4, 0),()),
		"Theta": ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ISpectrum(DispatchBaseClass):
	CLSID = IID('{DF418CC1-A5C6-11D5-B749-0040332FCEB4}')
	coclass_clsid = IID('{DF418CC3-A5C6-11D5-B749-0040332FCEB4}')

	def AddSimulated(self, S=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(217, LCID, 1, (11, 0), ((13, 1),),S
			)

	def Copy(self, S=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (11, 0), ((13, 1),),S
			)

	def CopyExperimental(self, S=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(213, LCID, 1, (11, 0), ((13, 1),),S
			)

	def CopySimulated(self, S=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (11, 0), ((13, 1),),S
			)

	def Data(self, spID=defaultNamedNotOptArg, chan=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (5, 0), ((3, 1), (3, 1)),spID
			, chan)

	def DataArray(self, spID=defaultNamedNotOptArg):
		return self._ApplyTypes_(201, 1, (12, 0), ((3, 1),), 'DataArray', None,spID
			)

	def Delete(self, spID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(204, LCID, 1, (24, 0), ((3, 1),),spID
			)

	def GetDataArray(self, spID=defaultNamedNotOptArg):
		return self._ApplyTypes_(207, 1, (12, 0), ((3, 1),), 'GetDataArray', None,spID
			)

	def HighElementID(self):
		return self._oleobj_.InvokeTypes(210, LCID, 1, (3, 0), (),)

	def IDOfElement(self, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (3, 0), ((3, 1),),Z
			)

	def IDOfIsotope(self, Z=defaultNamedNotOptArg, M=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(206, LCID, 1, (3, 0), ((3, 1), (5, 1)),Z
			, M)

	def Integrate(self, spID=defaultNamedNotOptArg, lowChannel=defaultNamedNotOptArg, upChannel=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (5, 0), ((3, 1), (3, 1), (3, 1)),spID
			, lowChannel, upChannel)

	def LowElementID(self):
		return self._oleobj_.InvokeTypes(209, LCID, 1, (3, 0), (),)

	# The method M is actually a property, but must be used as a method to correctly pass the arguments
	def M(self, spID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(218, LCID, 2, (5, 0), ((3, 1),),spID
			)

	# The method NumberOfChannels is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfChannels(self, spID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 2, (3, 0), ((3, 1),),spID
			)

	def SetDataArray(self, spID=defaultNamedNotOptArg, V=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), ((3, 1), (16396, 1)),spID
			, V)

	# The method SetM is actually a property, but must be used as a method to correctly pass the arguments
	def SetM(self, spID=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(218, LCID, 4, (24, 0), ((3, 1), (5, 1)),spID
			, arg1)

	# The method SetTitle is actually a property, but must be used as a method to correctly pass the arguments
	def SetTitle(self, spID=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(216, LCID, 4, (24, 0), ((3, 1), (8, 1)),spID
			, arg1)

	# The method SetZ is actually a property, but must be used as a method to correctly pass the arguments
	def SetZ(self, spID=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(211, LCID, 4, (24, 0), ((3, 1), (3, 1)),spID
			, arg1)

	# The method Setiso is actually a property, but must be used as a method to correctly pass the arguments
	def Setiso(self, spID=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(212, LCID, 4, (24, 0), ((3, 1), (3, 1)),spID
			, arg1)

	# The method Title is actually a property, but must be used as a method to correctly pass the arguments
	def Title(self, spID=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(216, LCID, 2, (8, 0), ((3, 1),),spID
			)

	# The method Z is actually a property, but must be used as a method to correctly pass the arguments
	def Z(self, spID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(211, LCID, 2, (3, 0), ((3, 1),),spID
			)

	# The method iso is actually a property, but must be used as a method to correctly pass the arguments
	def iso(self, spID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(212, LCID, 2, (3, 0), ((3, 1),),spID
			)

	_prop_map_get_ = {
		"AutoScale": (4, 2, (11, 0), (), "AutoScale", None),
		"BottomAxisMax": (6, 2, (5, 0), (), "BottomAxisMax", None),
		"BottomAxisMin": (5, 2, (5, 0), (), "BottomAxisMin", None),
		"ElementsVisible": (221, 2, (11, 0), (), "ElementsVisible", None),
		"EndAcquisition": (203, 2, (7, 0), (), "EndAcquisition", None),
		"ExperimentalVisible": (219, 2, (11, 0), (), "ExperimentalVisible", None),
		"IsotopesVisible": (222, 2, (11, 0), (), "IsotopesVisible", None),
		"LeftAxisMax": (8, 2, (5, 0), (), "LeftAxisMax", None),
		"LeftAxisMin": (7, 2, (5, 0), (), "LeftAxisMin", None),
		"SimulatedVisible": (220, 2, (11, 0), (), "SimulatedVisible", None),
		"SmoothedVisible": (223, 2, (11, 0), (), "SmoothedVisible", None),
		"StartAcquisition": (202, 2, (7, 0), (), "StartAcquisition", None),
	}
	_prop_map_put_ = {
		"AutoScale": ((4, LCID, 4, 0),()),
		"BottomAxisMax": ((6, LCID, 4, 0),()),
		"BottomAxisMin": ((5, LCID, 4, 0),()),
		"ElementsVisible": ((221, LCID, 4, 0),()),
		"EndAcquisition": ((203, LCID, 4, 0),()),
		"ExperimentalVisible": ((219, LCID, 4, 0),()),
		"IsotopesVisible": ((222, LCID, 4, 0),()),
		"LeftAxisMax": ((8, LCID, 4, 0),()),
		"LeftAxisMin": ((7, LCID, 4, 0),()),
		"SimulatedVisible": ((220, LCID, 4, 0),()),
		"SmoothedVisible": ((223, LCID, 4, 0),()),
		"StartAcquisition": ((202, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IStopping(DispatchBaseClass):
	'Dispatch interface for Stopping Object'
	CLSID = IID('{0A40E4F1-D298-11D5-B752-0040332FCEB4}')
	coclass_clsid = IID('{0A40E4F3-D298-11D5-B752-0040332FCEB4}')

	def EnergylossInLayer(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, E=defaultNamedNotOptArg, id=defaultNamedNotOptArg
			, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (5, 0), ((3, 1), (5, 1), (5, 1), (3, 1), (3, 1)),Z1
			, M1, E, id, lay)

	def StoppingInElement(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, E=defaultNamedNotOptArg, Z2=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (5, 0), ((3, 1), (5, 1), (5, 1), (3, 1)),Z1
			, M1, E, Z2)

	def StoppingInLayer(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, E=defaultNamedNotOptArg, id=defaultNamedNotOptArg
			, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (5, 0), ((3, 1), (5, 1), (5, 1), (3, 1), (3, 1)),Z1
			, M1, E, id, lay)

	def StragglingInLayer(self, Z1=defaultNamedNotOptArg, M1=defaultNamedNotOptArg, E=defaultNamedNotOptArg, id=defaultNamedNotOptArg
			, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (5, 0), ((3, 1), (5, 1), (5, 1), (3, 1), (3, 1)),Z1
			, M1, E, id, lay)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ITarget(DispatchBaseClass):
	'Dispatch interface for Target Object'
	CLSID = IID('{5978B7E1-9706-11D5-B747-0040332FCEB4}')
	coclass_clsid = IID('{5978B7E3-9706-11D5-B747-0040332FCEB4}')

	def AddElement(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (11, 0), ((3, 1),),lay
			)

	def AddElementProperties(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg, c=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(218, LCID, 1, (11, 0), ((3, 1), (12, 1), (12, 1)),lay
			, Z, c)

	def AddElements(self, lay=defaultNamedNotOptArg, NumElements=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, NumElements)

	def AddIsotope(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, el)

	def AddLayer(self):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (11, 0), (),)

	def AddLayers(self, NumLayers=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (11, 0), ((3, 1),),NumLayers
			)

	def Copy(self, Target1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(221, LCID, 1, (11, 0), ((13, 1),),Target1
			)

	def DeleteAllLayer(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (11, 0), (),)

	def DeleteElement(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, el)

	def DeleteIsotope(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (11, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, iso)

	def DeleteLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method ElementAmount is actually a property, but must be used as a method to correctly pass the arguments
	def ElementAmount(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(9, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementConcentrationArray is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentrationArray(self, lay=defaultNamedNotOptArg):
		return self._ApplyTypes_(217, 2, (12, 0), ((3, 1),), 'ElementConcentrationArray', None,lay
			)

	# The method ElementName is actually a property, but must be used as a method to correctly pass the arguments
	def ElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(15, LCID, 2, (8, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def ElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(213, LCID, 2, (3, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementZArray is actually a property, but must be used as a method to correctly pass the arguments
	def ElementZArray(self, lay=defaultNamedNotOptArg):
		return self._ApplyTypes_(216, 2, (12, 0), ((3, 1),), 'ElementZArray', None,lay
			)

	# The method HasLayerPorosity is actually a property, but must be used as a method to correctly pass the arguments
	def HasLayerPorosity(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 2, (11, 0), ((3, 1),),lay
			)

	# The method HasLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def HasLayerRoughness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 2, (11, 0), ((3, 1),),lay
			)

	def InsertLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(11, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method IsotopeConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def IsotopeConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(209, LCID, 2, (5, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, iso)

	# The method IsotopeMass is actually a property, but must be used as a method to correctly pass the arguments
	def IsotopeMass(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(210, LCID, 2, (5, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, iso)

	# The method LayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerRoughness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method LayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerThickness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method NumberOfElements is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfElements(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 2, (3, 0), ((3, 1),),lay
			)

	# The method NumberOfIsotopes is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfIsotopes(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 2, (3, 0), ((3, 1), (3, 1)),lay
			, el)

	def OpenMemory(self, WS=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(219, LCID, 1, (11, 0), ((8, 1),),WS
			)

	# The method PoreDiameter is actually a property, but must be used as a method to correctly pass the arguments
	def PoreDiameter(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(203, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method PorosityFraction is actually a property, but must be used as a method to correctly pass the arguments
	def PorosityFraction(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(202, LCID, 2, (5, 0), ((3, 1),),lay
			)

	def ReadLayer(self, FileName=defaultNamedNotOptArg, LayerNr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, LayerNr)

	def ReadTarget(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def SaveLayerAs(self, FileName=defaultNamedNotOptArg, LayerNr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, LayerNr)

	def SaveMemory(self, WS=pythoncom.Missing):
		return self._ApplyTypes_(220, 1, (11, 0), ((16392, 2),), 'SaveMemory', None,WS
			)

	def SaveTargetAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	# The method SetElementAmount is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementAmount(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(16, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(9, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementConcentrationArray is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentrationArray(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(217, LCID, 4, (24, 0), ((3, 1), (12, 1)),lay
			, arg1)

	# The method SetElementName is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(15, LCID, 4, (24, 0), ((3, 1), (3, 1), (8, 1)),lay
			, el, arg2)

	# The method SetElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(213, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, arg2)

	# The method SetElementZArray is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementZArray(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(216, LCID, 4, (24, 0), ((3, 1), (12, 1)),lay
			, arg1)

	# The method SetHasLayerPorosity is actually a property, but must be used as a method to correctly pass the arguments
	def SetHasLayerPorosity(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(201, LCID, 4, (24, 0), ((3, 1), (11, 1)),lay
			, arg1)

	# The method SetHasLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def SetHasLayerRoughness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(4, LCID, 4, (24, 0), ((3, 1), (11, 1)),lay
			, arg1)

	# The method SetIsotopeConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetIsotopeConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg, arg3=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(209, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1), (5, 1)),lay
			, el, iso, arg3)

	# The method SetIsotopeMass is actually a property, but must be used as a method to correctly pass the arguments
	def SetIsotopeMass(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, iso=defaultNamedNotOptArg, arg3=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(210, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1), (5, 1)),lay
			, el, iso, arg3)

	# The method SetLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerRoughness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(3, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetLayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerThickness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(1, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetPoreDiameter is actually a property, but must be used as a method to correctly pass the arguments
	def SetPoreDiameter(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(203, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetPorosityFraction is actually a property, but must be used as a method to correctly pass the arguments
	def SetPorosityFraction(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(202, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetStoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def SetStoppingFactor(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(207, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, Z, arg2)

	# The method StoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def StoppingFactor(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(207, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, Z)

	_prop_map_get_ = {
		"AsArray": (222, 2, (12, 0), (), "AsArray", None),
		"HasSubstrateRoughness": (6, 2, (11, 0), (), "HasSubstrateRoughness", None),
		"NumberOfLayers": (2, 2, (3, 0), (), "NumberOfLayers", None),
		"SubstrateRoughness": (5, 2, (5, 0), (), "SubstrateRoughness", None),
		"SubstrateRoughnessDistribution": (8, 2, (3, 0), (), "SubstrateRoughnessDistribution", None),
		"Thickness": (206, 2, (5, 0), (), "Thickness", None),
		"TotalNumberOfElements": (204, 2, (3, 0), (), "TotalNumberOfElements", None),
	}
	_prop_map_put_ = {
		"AsArray": ((222, LCID, 4, 0),()),
		"HasSubstrateRoughness": ((6, LCID, 4, 0),()),
		"SubstrateRoughness": ((5, LCID, 4, 0),()),
		"SubstrateRoughnessDistribution": ((8, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class ITargetOut(DispatchBaseClass):
	CLSID = IID('{5DB47E27-5BA1-4FE3-8785-545F494FCBE2}')
	coclass_clsid = IID('{E45540BA-A7B0-4033-9E6F-B26230D41F69}')

	def AddElement(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), ((3, 1),),lay
			)

	def AddElementProperties(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg, c=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(221, LCID, 1, (11, 0), ((3, 1), (12, 1), (12, 1)),lay
			, Z, c)

	def AddElements(self, lay=defaultNamedNotOptArg, NumElements=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(218, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, NumElements)

	def AddLayer(self):
		return self._oleobj_.InvokeTypes(205, LCID, 1, (11, 0), (),)

	def AddLayers(self, NumLayers=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(217, LCID, 1, (11, 0), ((3, 1),),NumLayers
			)

	def CreateTargetOut(self):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (24, 0), (),)

	def DeleteAllLayer(self):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (11, 0), (),)

	def DeleteElement(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(209, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, el)

	def DeleteLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(207, LCID, 1, (11, 0), ((3, 1),),lay
			)

	def DestroyTargetOut(self):
		return self._oleobj_.InvokeTypes(212, LCID, 1, (24, 0), (),)

	# The method ElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(204, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementConcentrationArray is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentrationArray(self, lay=defaultNamedNotOptArg):
		return self._ApplyTypes_(220, 2, (12, 0), ((3, 1),), 'ElementConcentrationArray', None,lay
			)

	# The method ElementName is actually a property, but must be used as a method to correctly pass the arguments
	def ElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(210, LCID, 2, (8, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def ElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(216, LCID, 2, (3, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementZArray is actually a property, but must be used as a method to correctly pass the arguments
	def ElementZArray(self, lay=defaultNamedNotOptArg):
		return self._ApplyTypes_(219, 2, (12, 0), ((3, 1),), 'ElementZArray', None,lay
			)

	def InsertLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(206, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method LayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerThickness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method NumberOfElements is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfElements(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(203, LCID, 2, (3, 0), ((3, 1),),lay
			)

	# The method SetElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(204, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementConcentrationArray is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentrationArray(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(220, LCID, 4, (24, 0), ((3, 1), (12, 1)),lay
			, arg1)

	# The method SetElementName is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(210, LCID, 4, (24, 0), ((3, 1), (3, 1), (8, 1)),lay
			, el, arg2)

	# The method SetElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(216, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, arg2)

	# The method SetElementZArray is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementZArray(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(219, LCID, 4, (24, 0), ((3, 1), (12, 1)),lay
			, arg1)

	# The method SetLayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerThickness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(201, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	_prop_map_get_ = {
		"AsArray": (222, 2, (12, 0), (), "AsArray", None),
		"NumberOfLayers": (202, 2, (3, 0), (), "NumberOfLayers", None),
		"Shift": (213, 2, (5, 0), (), "Shift", None),
		"Thickness": (214, 2, (5, 0), (), "Thickness", None),
	}
	_prop_map_put_ = {
		"AsArray": ((222, LCID, 4, 0),()),
		"Shift": ((213, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IWindow(DispatchBaseClass):
	CLSID = IID('{2C926AE5-0CDA-45F2-BD6B-70031EFFB199}')
	coclass_clsid = IID('{58312EB5-30F5-47D1-8E60-04634C214FBD}')

	def AddElement(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(210, LCID, 1, (11, 0), ((3, 1),),lay
			)

	def AddLayer(self):
		return self._oleobj_.InvokeTypes(207, LCID, 1, (11, 0), (),)

	def Copy(self, Window1=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(227, LCID, 1, (11, 0), ((13, 1),),Window1
			)

	def DeleteAllLayer(self):
		return self._oleobj_.InvokeTypes(222, LCID, 1, (11, 0), (),)

	def DeleteElement(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(211, LCID, 1, (11, 0), ((3, 1), (3, 1)),lay
			, el)

	def DeleteLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(209, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method ElementAmount is actually a property, but must be used as a method to correctly pass the arguments
	def ElementAmount(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(213, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def ElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(206, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementName is actually a property, but must be used as a method to correctly pass the arguments
	def ElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(212, LCID, 2, (8, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method ElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def ElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(224, LCID, 2, (3, 0), ((3, 1), (3, 1)),lay
			, el)

	# The method HasLayerPorosity is actually a property, but must be used as a method to correctly pass the arguments
	def HasLayerPorosity(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(218, LCID, 2, (11, 0), ((3, 1),),lay
			)

	# The method HasLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def HasLayerRoughness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(204, LCID, 2, (11, 0), ((3, 1),),lay
			)

	def InsertLayer(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(208, LCID, 1, (11, 0), ((3, 1),),lay
			)

	# The method LayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerRoughness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(203, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method LayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def LayerThickness(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(201, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method NumberOfElements is actually a property, but must be used as a method to correctly pass the arguments
	def NumberOfElements(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(205, LCID, 2, (3, 0), ((3, 1),),lay
			)

	def OpenMemory(self, WS=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(225, LCID, 1, (11, 0), ((8, 1),),WS
			)

	# The method PoreDiameter is actually a property, but must be used as a method to correctly pass the arguments
	def PoreDiameter(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(220, LCID, 2, (5, 0), ((3, 1),),lay
			)

	# The method PorosityFraction is actually a property, but must be used as a method to correctly pass the arguments
	def PorosityFraction(self, lay=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(219, LCID, 2, (5, 0), ((3, 1),),lay
			)

	def ReadLayer(self, FileName=defaultNamedNotOptArg, LayerNr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(214, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, LayerNr)

	def ReadWindow(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(216, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	def SaveLayerAs(self, FileName=defaultNamedNotOptArg, LayerNr=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(215, LCID, 1, (24, 0), ((8, 1), (3, 1)),FileName
			, LayerNr)

	def SaveMemory(self, WS=pythoncom.Missing):
		return self._ApplyTypes_(226, 1, (11, 0), ((16392, 2),), 'SaveMemory', None,WS
			)

	def SaveWindowAs(self, FileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(217, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	# The method SetElementAmount is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementAmount(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(213, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementConcentration is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementConcentration(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(206, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, el, arg2)

	# The method SetElementName is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementName(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(212, LCID, 4, (24, 0), ((3, 1), (3, 1), (8, 1)),lay
			, el, arg2)

	# The method SetElementZ is actually a property, but must be used as a method to correctly pass the arguments
	def SetElementZ(self, lay=defaultNamedNotOptArg, el=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(224, LCID, 4, (24, 0), ((3, 1), (3, 1), (3, 1)),lay
			, el, arg2)

	# The method SetHasLayerPorosity is actually a property, but must be used as a method to correctly pass the arguments
	def SetHasLayerPorosity(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(218, LCID, 4, (24, 0), ((3, 1), (11, 1)),lay
			, arg1)

	# The method SetHasLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def SetHasLayerRoughness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(204, LCID, 4, (24, 0), ((3, 1), (11, 1)),lay
			, arg1)

	# The method SetLayerRoughness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerRoughness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(203, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetLayerThickness is actually a property, but must be used as a method to correctly pass the arguments
	def SetLayerThickness(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(201, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetPoreDiameter is actually a property, but must be used as a method to correctly pass the arguments
	def SetPoreDiameter(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(220, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetPorosityFraction is actually a property, but must be used as a method to correctly pass the arguments
	def SetPorosityFraction(self, lay=defaultNamedNotOptArg, arg1=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(219, LCID, 4, (24, 0), ((3, 1), (5, 1)),lay
			, arg1)

	# The method SetStoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def SetStoppingFactor(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg, arg2=defaultUnnamedArg):
		return self._oleobj_.InvokeTypes(223, LCID, 4, (24, 0), ((3, 1), (3, 1), (5, 1)),lay
			, Z, arg2)

	# The method StoppingFactor is actually a property, but must be used as a method to correctly pass the arguments
	def StoppingFactor(self, lay=defaultNamedNotOptArg, Z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(223, LCID, 2, (5, 0), ((3, 1), (3, 1)),lay
			, Z)

	_prop_map_get_ = {
		"NumberOfLayers": (202, 2, (3, 0), (), "NumberOfLayers", None),
		"Thickness": (221, 2, (5, 0), (), "Thickness", None),
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'Simnra.App'
class App(CoClassBaseClass): # A CoClass
	# App Object
	CLSID = IID('{9F51F4E3-754F-11D5-B742-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IApp,
	]
	default_interface = IApp

# This CoClass is known by the name 'Simnra.Calc'
class Calc(CoClassBaseClass): # A CoClass
	CLSID = IID('{9DD33B22-A8EC-11D5-B749-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICalc,
	]
	default_interface = ICalc

# This CoClass is known by the name 'Simnra.CrossSec'
class CrossSec(CoClassBaseClass): # A CoClass
	CLSID = IID('{504EF515-68CF-495D-8D7C-C132E538D839}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ICrossSec,
	]
	default_interface = ICrossSec

# This CoClass is known by the name 'Simnra.Fit'
class Fit(CoClassBaseClass): # A CoClass
	CLSID = IID('{54207F22-9D23-11D5-B748-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IFit,
	]
	default_interface = IFit

# This CoClass is known by the name 'Simnra.Foil'
class Foil(CoClassBaseClass): # A CoClass
	CLSID = IID('{F14C14DC-62BD-4C60-9710-A05CA0151546}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IFoil,
	]
	default_interface = IFoil

# This CoClass is known by the name 'Simnra.Forms'
class Forms(CoClassBaseClass): # A CoClass
	CLSID = IID('{E31D2D47-3E2E-418B-93E3-8A8C72A7E6C2}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IForms,
	]
	default_interface = IForms

# This CoClass is known by the name 'Simnra.PIGE'
class PIGE(CoClassBaseClass): # A CoClass
	CLSID = IID('{AB1B23A1-601F-465B-B2DB-F4BC15421B62}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IPIGE,
	]
	default_interface = IPIGE

# This CoClass is known by the name 'Simnra.Projectile'
class Projectile(CoClassBaseClass): # A CoClass
	CLSID = IID('{AB9D3C37-2FA9-434A-8959-8C84A8F50C97}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IProjectile,
	]
	default_interface = IProjectile

# This CoClass is known by the name 'Simnra.Setup'
class Setup(CoClassBaseClass): # A CoClass
	# Setup Object
	CLSID = IID('{C22A1432-9329-11D5-B743-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ISetup,
	]
	default_interface = ISetup

# This CoClass is known by the name 'Simnra.Spectrum'
class Spectrum(CoClassBaseClass): # A CoClass
	CLSID = IID('{DF418CC3-A5C6-11D5-B749-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ISpectrum,
	]
	default_interface = ISpectrum

# This CoClass is known by the name 'Simnra.Stopping'
class Stopping(CoClassBaseClass): # A CoClass
	CLSID = IID('{0A40E4F3-D298-11D5-B752-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IStopping,
	]
	default_interface = IStopping

# This CoClass is known by the name 'Simnra.Target'
class Target(CoClassBaseClass): # A CoClass
	# Target Object
	CLSID = IID('{5978B7E3-9706-11D5-B747-0040332FCEB4}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ITarget,
	]
	default_interface = ITarget

# This CoClass is known by the name 'Simnra.TargetOut'
class TargetOut(CoClassBaseClass): # A CoClass
	CLSID = IID('{E45540BA-A7B0-4033-9E6F-B26230D41F69}')
	coclass_sources = [
	]
	coclass_interfaces = [
		ITargetOut,
	]
	default_interface = ITargetOut

# This CoClass is known by the name 'Simnra.Window'
class Window(CoClassBaseClass): # A CoClass
	CLSID = IID('{58312EB5-30F5-47D1-8E60-04634C214FBD}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IWindow,
	]
	default_interface = IWindow

IApp_vtables_dispatch_ = 1
IApp_vtables_ = [
	(( 'Open' , 'FileName' , 'FileType' , 'Value' , ), 1, (1, (), [ 
			 (8, 1, None, None) , (3, 33, '-1', None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'CalculateSpectrum' , 'Value' , ), 2, (2, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , 'FileType' , 'Value' , ), 3, (3, (), [ 
			 (8, 1, None, None) , (3, 49, '2', None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'ReadSpectrumData' , 'FileName' , 'Format' , 'Value' , ), 4, (4, (), [ 
			 (8, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Minimize' , ), 5, (5, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Restore' , ), 6, (6, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'BringToFront' , ), 7, (7, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'WriteSpectrumData' , 'FileName' , 'Param2' , ), 8, (8, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'CopySpectrumData' , ), 9, (9, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Active' , 'Value' , ), 10, (10, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Hide' , ), 11, (11, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Show' , ), 12, (12, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'FitSpectrum' , 'Value' , ), 13, (13, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'DeleteSpectrumOnCalculate' , 'Value' , ), 14, (14, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'DeleteSpectrumOnCalculate' , 'Value' , ), 14, (14, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'ShowMessages' , 'Value' , ), 15, (15, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'ShowMessages' , 'Value' , ), 15, (15, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'LastMessage' , 'Value' , ), 16, (16, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Maximize' , ), 17, (17, (), [ ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'CalculateSpectrumFast' , 'Value' , ), 18, (18, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'CalculatingSpectrum' , 'Value' , ), 19, (19, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'SpectrumChanged' , 'Value' , ), 20, (20, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'SpectrumChanged' , 'Value' , ), 20, (20, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'FileName' , 'Value' , ), 21, (21, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'CalculateSpectrumToDepth' , 'Depth' , 'Value' , ), 22, (22, (), [ (5, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'Left' , 'Value' , ), 23, (23, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'Left' , 'Value' , ), 23, (23, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'Width' , 'Value' , ), 24, (24, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'Width' , 'Value' , ), 24, (24, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'Top' , 'Value' , ), 25, (25, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'Top' , 'Value' , ), 25, (25, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'Height' , 'Value' , ), 26, (26, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'Height' , 'Value' , ), 26, (26, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'Version' , 'Value' , ), 27, (27, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'CreateListOfCrSecs' , ), 28, (28, (), [ ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'SaveThumbnailAs' , 'FileName' , 'Width' , ), 201, (201, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'Standalone' , 'Value' , ), 204, (204, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'BringToRear' , ), 205, (205, (), [ ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'OpenAs' , 'FileName' , 'FileType' , 'Value' , ), 202, (202, (), [ 
			 (8, 1, None, None) , (3, 49, '-1', None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'LegendVisible' , 'Value' , ), 203, (203, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'LegendVisible' , 'Value' , ), 203, (203, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'LegendOutsideOfChart' , 'Value' , ), 206, (206, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'LegendOutsideOfChart' , 'Value' , ), 206, (206, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'TopAxisCaption' , 'Value' , ), 207, (207, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'TopAxisCaption' , 'Value' , ), 207, (207, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'OpenStream' , 'Stream' , 'FileType' , 'Value' , ), 208, (208, (), [ 
			 (13, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'IncidentIonEnergyIsZero' , 'Value' , ), 209, (209, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'IncidentIonEnergyIsZero' , 'Value' , ), 209, (209, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'Visible' , 'Value' , ), 210, (210, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'Reset' , ), 211, (211, (), [ ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'ToolbarVisible' , 'Value' , ), 212, (212, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'ToolbarVisible' , 'Value' , ), 212, (212, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'MenuVisible' , 'Value' , ), 213, (213, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'MenuVisible' , 'Value' , ), 213, (213, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'StatusbarVisible' , 'Value' , ), 214, (214, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'StatusbarVisible' , 'Value' , ), 214, (214, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'ControlsVisible' , ), 215, (215, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'ResizeSpectrum' , 'NumChannels' , 'ResizeCalibration' , ), 216, (216, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'BorderStyle' , 'Value' , ), 217, (217, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'BorderStyle' , 'Value' , ), 217, (217, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'OLEUser' , 'Value' , ), 218, (218, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
	(( 'OLEUser' , 'Value' , ), 218, (218, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'SRIMDirectory' , 'Value' , ), 219, (219, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'SRIMDirectory' , 'Value' , ), 219, (219, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'CalculatePileup' , 'Value' , ), 220, (220, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'CalculateDualScatteringBackground' , 'AddToSpectrum' , 'Value' , ), 221, (221, (), [ (11, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'CloseButtonEnabled' , ), 222, (222, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'TargetOutItemVisible' , 'Value' , ), 223, (223, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
	(( 'TargetOutItemVisible' , 'Value' , ), 223, (223, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'OpenMemory' , 'S' , 'FileType' , 'Value' , ), 224, (224, (), [ 
			 (8, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
	(( 'SaveMemory' , 'WS' , 'Value' , ), 225, (225, (), [ (16392, 2, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 616 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'App1' , 'Value' , ), 226, (226, (), [ (13, 1, None, "IID('{9F51F4E3-754F-11D5-B742-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 624 , (3, 0, None, None) , 0 , )),
	(( 'Priority' , 'Value' , ), 227, (227, (), [ (16403, 10, None, None) , ], 1 , 2 , 4 , 0 , 632 , (3, 0, None, None) , 0 , )),
	(( 'Priority' , 'Value' , ), 227, (227, (), [ (19, 1, None, None) , ], 1 , 4 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'CalculateSpectrumFromTargets' , 'V' , 'Value' , ), 228, (228, (), [ (12, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'CalculateSpectrumFromTargetsFast' , 'V' , 'Value' , ), 229, (229, (), [ (12, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 656 , (3, 0, None, None) , 0 , )),
	(( 'SimulationMode' , 'Value' , ), 230, (230, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 664 , (3, 0, None, None) , 0 , )),
	(( 'SimulationMode' , 'Value' , ), 230, (230, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 672 , (3, 0, None, None) , 0 , )),
	(( 'GetThumbnailAsVariant' , 'Width' , 'V' , ), 231, (231, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 680 , (3, 0, None, None) , 0 , )),
]

ICalc_vtables_dispatch_ = 1
ICalc_vtables_ = [
	(( 'dEin' , 'Value' , ), 1, (1, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'dEin' , 'Value' , ), 1, (1, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'dEout' , 'Value' , ), 2, (2, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'dEout' , 'Value' , ), 2, (2, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Emin' , 'Value' , ), 3, (3, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Emin' , 'Value' , ), 3, (3, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Straggling' , 'Value' , ), 4, (4, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Straggling' , 'Value' , ), 4, (4, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Isotopes' , 'Value' , ), 5, (5, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Isotopes' , 'Value' , ), 5, (5, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'DualScattering' , 'Value' , ), 6, (6, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'DualScattering' , 'Value' , ), 6, (6, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'MultipleScattering' , 'Value' , ), 7, (7, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'MultipleScattering' , 'Value' , ), 7, (7, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'AutoStepwidthIn' , 'Value' , ), 8, (8, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'AutoStepwidthIn' , 'Value' , ), 8, (8, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'AutoStepwidthOut' , 'Value' , ), 9, (9, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'AutoStepwidthOut' , 'Value' , ), 9, (9, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfDVariations' , 'Value' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfDVariations' , 'Value' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfAngleVariations' , 'Value' , ), 11, (11, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfAngleVariations' , 'Value' , ), 11, (11, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'ElementSpectra' , 'Value' , ), 12, (12, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'ElementSpectra' , 'Value' , ), 12, (12, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeSpectra' , 'Value' , ), 13, (13, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeSpectra' , 'Value' , ), 13, (13, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'ZBStopping' , 'Value' , ), 14, (14, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'ZBStopping' , 'Value' , ), 14, (14, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'HighEnergyStopping' , 'Value' , ), 15, (15, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'HighEnergyStopping' , 'Value' , ), 15, (15, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'SubstrateRoughnessDimension' , 'Value' , ), 16, (16, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'SubstrateRoughnessDimension' , 'Value' , ), 16, (16, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'StragglingModel' , 'Value' , ), 17, (17, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'StragglingModel' , 'Value' , ), 17, (17, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'ScreeningModel' , 'Value' , ), 18, (18, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'ScreeningModel' , 'Value' , ), 18, (18, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'PUModel' , 'Value' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'PUModel' , 'Value' , ), 19, (19, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'LogFile' , 'Value' , ), 20, (20, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'LogFile' , 'Value' , ), 20, (20, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'CreateSpectrum' , 'Value' , ), 21, (21, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'CreateSpectrum' , 'Value' , ), 21, (21, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'CrossSecStraggling' , 'Value' , ), 201, (201, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'CrossSecStraggling' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'StragglingShape' , 'Value' , ), 202, (202, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'StragglingShape' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'DualScatteringRoughness' , 'Value' , ), 203, (203, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'DualScatteringRoughness' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'StoppingModel' , 'Value' , ), 204, (204, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'StoppingModel' , 'Value' , ), 204, (204, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'NuclearStoppingModel' , 'Value' , ), 205, (205, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'NuclearStoppingModel' , 'Value' , ), 205, (205, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'CreateSpectrumFromLayerNr' , 'Value' , ), 206, (206, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'CreateSpectrumFromLayerNr' , 'Value' , ), 206, (206, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'Accuracy' , 'Value' , ), 207, (207, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'CalculateToEMin' , 'Value' , ), 208, (208, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'CalculateToEMin' , 'Value' , ), 208, (208, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'OpenMemory' , 'WS' , 'Value' , ), 209, (209, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'SaveMemory' , 'WS' , 'Value' , ), 210, (210, (), [ (16392, 2, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'Calc1' , 'Value' , ), 211, (211, (), [ (13, 1, None, "IID('{9DD33B22-A8EC-11D5-B749-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , 'Value' , ), 212, (212, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsDefault' , 'Value' , ), 213, (213, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'Open' , 'FileName' , 'Value' , ), 214, (214, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'OpenAs' , 'FileName' , 'FileType' , 'Value' , ), 215, (215, (), [ 
			 (8, 1, None, None) , (3, 49, '-1', None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'GeometricalStraggling' , 'Value' , ), 216, (216, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'GeometricalStraggling' , 'Value' , ), 216, (216, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'MultipleScatteringModel' , 'Value' , ), 217, (217, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'MultipleScatteringModel' , 'Value' , ), 217, (217, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
]

ICrossSec_vtables_dispatch_ = 1
ICrossSec_vtables_ = [
	(( 'RBSRutherford' , 'Z1' , 'M1' , 'Z2' , 'M2' , 
			 'E' , 'Theta' , 'Value' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'UniversalEMax' , 'Z1' , 'M1' , 'Z2' , 'M2' , 
			 'Value' , ), 2, (2, (), [ (3, 1, None, None) , (5, 1, None, None) , (3, 1, None, None) , 
			 (5, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ERDRutherford' , 'Z1' , 'M1' , 'Z2' , 'M2' , 
			 'E' , 'Phi' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SelectRutherford' , 'Z' , ), 201, (201, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SelectRutherfordAll' , ), 202, (202, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'UnselectRutherford' , 'Z' , ), 203, (203, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'UnselectRutherfordAll' , ), 204, (204, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Count' , 'Value' , ), 205, (205, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'Index' , 'Value' , ), 206, (206, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'FileName' , 'Index' , 'Value' , ), 207, (207, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Choose' , 'Index' , 'Value' , ), 208, (208, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Choose' , 'Index' , 'Value' , ), 208, (208, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'Info' , 'Index' , 'Value' , ), 209, (209, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'Emin' , 'Index' , 'Value' , ), 210, (210, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Emin' , 'Index' , 'Value' , ), 210, (210, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'EMax' , 'Index' , 'Value' , ), 211, (211, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'EMax' , 'Index' , 'Value' , ), 211, (211, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SelectSigmaCalc' , 'Z' , ), 212, (212, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SelectSigmaCalcAll' , ), 213, (213, (), [ ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'UnselectSigmaCalc' , 'Z' , ), 214, (214, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'UnselectSigmaCalcAll' , ), 215, (215, (), [ ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'Unselect' , 'Z' , ), 216, (216, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'UnselectAll' , ), 217, (217, (), [ ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'ReactionsChoosen' , 'Value' , ), 218, (218, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'ReactionsChoosen' , 'Value' , ), 218, (218, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'SelectReactions' , ), 219, (219, (), [ ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
]

IFit_vtables_dispatch_ = 1
IFit_vtables_ = [
	(( 'EnergyCalibration' , 'Value' , ), 2, (2, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'EnergyCalibration' , 'Value' , ), 2, (2, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ParticlesSr' , 'Value' , ), 3, (3, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'ParticlesSr' , 'Value' , ), 3, (3, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'LayerThickness' , 'Value' , ), 4, (4, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'LayerThickness' , 'Value' , ), 4, (4, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'LayerComposition' , 'Value' , ), 5, (5, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'LayerComposition' , 'Value' , ), 5, (5, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'LayerNr' , 'Value' , ), 6, (6, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'LayerNr' , 'Value' , ), 6, (6, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfRegions' , 'Value' , ), 7, (7, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfRegions' , 'Value' , ), 7, (7, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'RegionMinChannel' , 'reg' , 'Value' , ), 8, (8, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'RegionMinChannel' , 'reg' , 'Value' , ), 8, (8, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'RegionMaxChannel' , 'reg' , 'Value' , ), 9, (9, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'RegionMaxChannel' , 'reg' , 'Value' , ), 9, (9, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'MaxIterations' , 'Value' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'MaxIterations' , 'Value' , ), 10, (10, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Accuracy' , 'Value' , ), 11, (11, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'Accuracy' , 'Value' , ), 11, (11, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'Chi2' , 'Value' , ), 1, (1, (), [ (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'Value' , ), 12, (12, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'Value' , ), 12, (12, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'Chi2Evaluation' , 'Value' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'Chi2Evaluation' , 'Value' , ), 13, (13, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
]

IFoil_vtables_dispatch_ = 1
IFoil_vtables_ = [
	(( 'LayerThickness' , 'lay' , 'Value' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'LayerThickness' , 'lay' , 'Value' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfLayers' , 'Value' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'lay' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'lay' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerRoughness' , 'lay' , 'Value' , ), 4, (4, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerRoughness' , 'lay' , 'Value' , ), 4, (4, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfElements' , 'lay' , 'Value' , ), 5, (5, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 6, (6, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 6, (6, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'AddLayer' , 'Value' , ), 7, (7, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'InsertLayer' , 'lay' , 'Value' , ), 8, (8, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'DeleteLayer' , 'lay' , 'Value' , ), 9, (9, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'AddElement' , 'lay' , 'Value' , ), 10, (10, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'DeleteElement' , 'lay' , 'el' , 'Value' , ), 11, (11, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 12, (12, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 12, (12, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'ElementAmount' , 'lay' , 'el' , 'Value' , ), 13, (13, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'ElementAmount' , 'lay' , 'el' , 'Value' , ), 13, (13, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'ReadLayer' , 'FileName' , 'LayerNr' , ), 14, (14, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'SaveLayerAs' , 'FileName' , 'LayerNr' , ), 15, (15, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'ReadFoil' , 'FileName' , ), 16, (16, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'SaveFoilAs' , 'FileName' , ), 17, (17, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerPorosity' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerPorosity' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'PorosityFraction' , 'lay' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'PorosityFraction' , 'lay' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'PoreDiameter' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'PoreDiameter' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'Thickness' , 'Value' , ), 204, (204, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'DeleteAllLayer' , 'Value' , ), 205, (205, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'lay' , 'Z' , 'Value' , ), 206, (206, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'lay' , 'Z' , 'Value' , ), 206, (206, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 207, (207, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 207, (207, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'OpenMemory' , 'WS' , 'Value' , ), 208, (208, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'SaveMemory' , 'WS' , 'Value' , ), 209, (209, (), [ (16392, 2, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'Foil1' , 'Value' , ), 210, (210, (), [ (13, 1, None, "IID('{F14C14DC-62BD-4C60-9710-A05CA0151546}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
]

IForms_vtables_dispatch_ = 1
IForms_vtables_ = [
	(( 'ShowSetupExperiment' , ), 201, (201, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'ShowSetupCalculation' , ), 202, (202, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ShowSetupGeometry' , ), 203, (203, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'ShowSetupDetector' , ), 204, (204, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ShowSetupPileup' , ), 205, (205, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ShowReactions' , ), 206, (206, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ShowTargetFoil' , ), 207, (207, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'ShowTargetWindow' , ), 208, (208, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ShowToolsDataReader' , ), 209, (209, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ShowToolsIntegrateSpectrum' , ), 210, (210, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ShowToolsNearestElements' , ), 211, (211, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'ShowToolsSmoothed' , ), 212, (212, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'ShowTargetTarget' , ), 213, (213, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
]

IPIGE_vtables_dispatch_ = 1
IPIGE_vtables_ = [
	(( 'NumberOfGammas' , 'Value' , ), 201, (201, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'E' , 'n' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Counts' , 'n' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
]

IProjectile_vtables_dispatch_ = 1
IProjectile_vtables_ = [
	(( 'Name' , 'Value' , ), 4, (4, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Name' , 'Value' , ), 4, (4, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Charge' , 'Value' , ), 5, (5, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Charge' , 'Value' , ), 5, (5, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Mass' , 'Value' , ), 6, (6, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Mass' , 'Value' , ), 6, (6, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'P' , 'Value' , ), 201, (201, (), [ (13, 1, None, "IID('{AB9D3C37-2FA9-434A-8959-8C84A8F50C97}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
]

ISetup_vtables_dispatch_ = 1
ISetup_vtables_ = [
	(( 'Energy' , 'Value' , ), 1, (1, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Energy' , 'Value' , ), 1, (1, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Theta' , 'Value' , ), 2, (2, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Theta' , 'Value' , ), 2, (2, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Alpha' , 'Value' , ), 3, (3, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Alpha' , 'Value' , ), 3, (3, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Beta' , 'Value' , ), 4, (4, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Beta' , 'Value' , ), 4, (4, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ParticlesSr' , 'Value' , ), 5, (5, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ParticlesSr' , 'Value' , ), 5, (5, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'CalibrationOffset' , 'Value' , ), 6, (6, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'CalibrationOffset' , 'Value' , ), 6, (6, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'CalibrationLinear' , 'Value' , ), 7, (7, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'CalibrationLinear' , 'Value' , ), 7, (7, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'CalibrationQuadratic' , 'Value' , ), 8, (8, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'CalibrationQuadratic' , 'Value' , ), 8, (8, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'DetectorResolution' , 'Value' , ), 9, (9, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'DetectorResolution' , 'Value' , ), 9, (9, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'Beamspread' , 'Value' , ), 10, (10, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'Beamspread' , 'Value' , ), 10, (10, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'RealTime' , 'Value' , ), 11, (11, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'RealTime' , 'Value' , ), 11, (11, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'LifeTime' , 'Value' , ), 12, (12, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'LifeTime' , 'Value' , ), 12, (12, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'RiseTime' , 'Value' , ), 13, (13, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'RiseTime' , 'Value' , ), 13, (13, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'PURResolution' , 'Value' , ), 14, (14, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'PURResolution' , 'Value' , ), 14, (14, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'PUROn' , 'Value' , ), 15, (15, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'PUROn' , 'Value' , ), 15, (15, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'LTCorrection' , 'Value' , ), 16, (16, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'LTCorrection' , 'Value' , ), 16, (16, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'PUCalculation' , 'Value' , ), 17, (17, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'PUCalculation' , 'Value' , ), 17, (17, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'LiveTime' , 'Value' , ), 18, (18, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'LiveTime' , 'Value' , ), 18, (18, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'DetectorType' , 'Value' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'DetectorType' , 'Value' , ), 19, (19, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'TOFLength' , 'Value' , ), 20, (20, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'TOFLength' , 'Value' , ), 20, (20, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'TOFTimeResolution' , 'Value' , ), 21, (21, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'TOFTimeResolution' , 'Value' , ), 21, (21, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'SetBeta' , 'Geometry' , 'Value' , ), 22, (22, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'ReadDetectorSensitivity' , 'FileName' , 'Format' , 'Value' , ), 201, (201, (), [ 
			 (8, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'DetectorSensitivity' , 'Value' , ), 202, (202, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'DetectorSensitivity' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'DetectorSensitivityFileName' , 'Value' , ), 203, (203, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , 'Value' , ), 204, (204, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsDefault' , 'Value' , ), 205, (205, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'Open' , 'FileName' , 'Value' , ), 206, (206, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'OpenAs' , 'FileName' , 'FileType' , 'Value' , ), 207, (207, (), [ 
			 (8, 1, None, None) , (3, 33, '-1', None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'OpenMemory' , 'WS' , 'Value' , ), 208, (208, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'SaveMemory' , 'WS' , 'Value' , ), 209, (209, (), [ (16392, 2, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'Setup1' , 'Value' , ), 210, (210, (), [ (13, 1, None, "IID('{C22A1432-9329-11D5-B743-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'BeamShape' , 'Value' , ), 211, (211, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'BeamShape' , 'Value' , ), 211, (211, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'BeamWidth' , 'Value' , ), 212, (212, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'BeamWidth' , 'Value' , ), 212, (212, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'BeamHeight' , 'Value' , ), 213, (213, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'BeamHeight' , 'Value' , ), 213, (213, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'DetectorPosition' , 'Value' , ), 214, (214, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
	(( 'DetectorPosition' , 'Value' , ), 214, (214, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'ApertureShape' , 'Value' , ), 215, (215, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'ApertureShape' , 'Value' , ), 215, (215, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'ApertureWidth' , 'Value' , ), 216, (216, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 568 , (3, 0, None, None) , 0 , )),
	(( 'ApertureWidth' , 'Value' , ), 216, (216, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'ApertureHeight' , 'Value' , ), 217, (217, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'ApertureHeight' , 'Value' , ), 217, (217, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
	(( 'ApertureDistance' , 'Value' , ), 218, (218, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'ApertureDistance' , 'Value' , ), 218, (218, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 608 , (3, 0, None, None) , 0 , )),
]

ISpectrum_vtables_dispatch_ = 1
ISpectrum_vtables_ = [
	(( 'Integrate' , 'spID' , 'lowChannel' , 'upChannel' , 'Value' , 
			 ), 1, (1, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Data' , 'spID' , 'chan' , 'Value' , ), 2, (2, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfChannels' , 'spID' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'AutoScale' , 'Value' , ), 4, (4, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'AutoScale' , 'Value' , ), 4, (4, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'BottomAxisMin' , 'Value' , ), 5, (5, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'BottomAxisMin' , 'Value' , ), 5, (5, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'BottomAxisMax' , 'Value' , ), 6, (6, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'BottomAxisMax' , 'Value' , ), 6, (6, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'LeftAxisMin' , 'Value' , ), 7, (7, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'LeftAxisMin' , 'Value' , ), 7, (7, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'LeftAxisMax' , 'Value' , ), 8, (8, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'LeftAxisMax' , 'Value' , ), 8, (8, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'DataArray' , 'spID' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Delete' , 'spID' , ), 204, (204, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'IDOfElement' , 'Z' , 'Value' , ), 205, (205, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'IDOfIsotope' , 'Z' , 'M' , 'Value' , ), 206, (206, (), [ 
			 (3, 1, None, None) , (5, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'GetDataArray' , 'spID' , 'Value' , ), 207, (207, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SetDataArray' , 'spID' , 'V' , 'Value' , ), 208, (208, (), [ 
			 (3, 1, None, None) , (16396, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'LowElementID' , 'Value' , ), 209, (209, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'HighElementID' , 'Value' , ), 210, (210, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'Z' , 'spID' , 'Value' , ), 211, (211, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'Z' , 'spID' , 'Value' , ), 211, (211, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'iso' , 'spID' , 'Value' , ), 212, (212, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'iso' , 'spID' , 'Value' , ), 212, (212, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'StartAcquisition' , 'Value' , ), 202, (202, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'StartAcquisition' , 'Value' , ), 202, (202, (), [ (7, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'EndAcquisition' , 'Value' , ), 203, (203, (), [ (16391, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'EndAcquisition' , 'Value' , ), 203, (203, (), [ (7, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'CopyExperimental' , 'S' , 'Value' , ), 213, (213, (), [ (13, 1, None, "IID('{DF418CC3-A5C6-11D5-B749-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'CopySimulated' , 'S' , 'Value' , ), 214, (214, (), [ (13, 1, None, "IID('{DF418CC3-A5C6-11D5-B749-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'S' , 'Valu' , ), 215, (215, (), [ (13, 1, None, "IID('{DF418CC3-A5C6-11D5-B749-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'spID' , 'Value' , ), 216, (216, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'Title' , 'spID' , 'Value' , ), 216, (216, (), [ (3, 1, None, None) , 
			 (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'AddSimulated' , 'S' , 'Value' , ), 217, (217, (), [ (13, 1, None, "IID('{DF418CC3-A5C6-11D5-B749-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'M' , 'spID' , 'Value' , ), 218, (218, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'M' , 'spID' , 'Value' , ), 218, (218, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'ExperimentalVisible' , 'Value' , ), 219, (219, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'ExperimentalVisible' , 'Value' , ), 219, (219, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'SimulatedVisible' , 'Value' , ), 220, (220, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'SimulatedVisible' , 'Value' , ), 220, (220, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'ElementsVisible' , 'Value' , ), 221, (221, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'ElementsVisible' , 'Value' , ), 221, (221, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'IsotopesVisible' , 'Value' , ), 222, (222, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'IsotopesVisible' , 'Value' , ), 222, (222, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'SmoothedVisible' , 'Value' , ), 223, (223, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'SmoothedVisible' , 'Value' , ), 223, (223, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
]

IStopping_vtables_dispatch_ = 1
IStopping_vtables_ = [
	(( 'StoppingInElement' , 'Z1' , 'M1' , 'E' , 'Z2' , 
			 'Value' , ), 1, (1, (), [ (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'StoppingInLayer' , 'Z1' , 'M1' , 'E' , 'id' , 
			 'lay' , 'Value' , ), 2, (2, (), [ (3, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'StragglingInLayer' , 'Z1' , 'M1' , 'E' , 'id' , 
			 'lay' , 'Value' , ), 4, (4, (), [ (3, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'EnergylossInLayer' , 'Z1' , 'M1' , 'E' , 'id' , 
			 'lay' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
]

ITarget_vtables_dispatch_ = 1
ITarget_vtables_ = [
	(( 'LayerThickness' , 'lay' , 'Value' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'LayerThickness' , 'lay' , 'Value' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfLayers' , 'Value' , ), 2, (2, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'lay' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'lay' , 'Value' , ), 3, (3, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerRoughness' , 'lay' , 'Value' , ), 4, (4, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerRoughness' , 'lay' , 'Value' , ), 4, (4, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SubstrateRoughness' , 'Value' , ), 5, (5, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SubstrateRoughness' , 'Value' , ), 5, (5, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'HasSubstrateRoughness' , 'Value' , ), 6, (6, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'HasSubstrateRoughness' , 'Value' , ), 6, (6, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfElements' , 'lay' , 'Value' , ), 7, (7, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 9, (9, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 9, (9, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'AddLayer' , 'Value' , ), 10, (10, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'InsertLayer' , 'lay' , 'Value' , ), 11, (11, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'DeleteLayer' , 'lay' , 'Value' , ), 12, (12, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'AddElement' , 'lay' , 'Value' , ), 13, (13, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'DeleteElement' , 'lay' , 'el' , 'Value' , ), 14, (14, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 15, (15, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 15, (15, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'SubstrateRoughnessDistribution' , 'Value' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'SubstrateRoughnessDistribution' , 'Value' , ), 8, (8, (), [ (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'ElementAmount' , 'lay' , 'el' , 'Value' , ), 16, (16, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'ElementAmount' , 'lay' , 'el' , 'Value' , ), 16, (16, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'ReadLayer' , 'FileName' , 'LayerNr' , ), 17, (17, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'SaveLayerAs' , 'FileName' , 'LayerNr' , ), 18, (18, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'ReadTarget' , 'FileName' , ), 19, (19, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'SaveTargetAs' , 'FileName' , ), 20, (20, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerPorosity' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerPorosity' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'PorosityFraction' , 'lay' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'PorosityFraction' , 'lay' , 'Value' , ), 202, (202, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'PoreDiameter' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'PoreDiameter' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'TotalNumberOfElements' , 'Value' , ), 204, (204, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'DeleteAllLayer' , 'Value' , ), 205, (205, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'Thickness' , 'Value' , ), 206, (206, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'lay' , 'Z' , 'Value' , ), 207, (207, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'lay' , 'Z' , 'Value' , ), 207, (207, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfIsotopes' , 'lay' , 'el' , 'Value' , ), 208, (208, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeConcentration' , 'lay' , 'el' , 'iso' , 'Value' , 
			 ), 209, (209, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeConcentration' , 'lay' , 'el' , 'iso' , 'Value' , 
			 ), 209, (209, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeMass' , 'lay' , 'el' , 'iso' , 'Value' , 
			 ), 210, (210, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'IsotopeMass' , 'lay' , 'el' , 'iso' , 'Value' , 
			 ), 210, (210, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 408 , (3, 0, None, None) , 0 , )),
	(( 'AddIsotope' , 'lay' , 'el' , 'Value' , ), 211, (211, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'DeleteIsotope' , 'lay' , 'el' , 'iso' , 'Value' , 
			 ), 212, (212, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 213, (213, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 213, (213, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'AddLayers' , 'NumLayers' , 'Value' , ), 214, (214, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'AddElements' , 'lay' , 'NumElements' , 'Value' , ), 215, (215, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'ElementZArray' , 'lay' , 'V' , ), 216, (216, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'ElementZArray' , 'lay' , 'V' , ), 216, (216, (), [ (3, 1, None, None) , 
			 (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentrationArray' , 'lay' , 'V' , ), 217, (217, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentrationArray' , 'lay' , 'V' , ), 217, (217, (), [ (3, 1, None, None) , 
			 (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'AddElementProperties' , 'lay' , 'Z' , 'c' , 'Value' , 
			 ), 218, (218, (), [ (3, 1, None, None) , (12, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'OpenMemory' , 'WS' , 'Value' , ), 219, (219, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'SaveMemory' , 'WS' , 'Value' , ), 220, (220, (), [ (16392, 2, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'Target1' , 'Value' , ), 221, (221, (), [ (13, 1, None, "IID('{5978B7E3-9706-11D5-B747-0040332FCEB4}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'AsArray' , 'Value' , ), 222, (222, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'AsArray' , 'Value' , ), 222, (222, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
]

ITargetOut_vtables_dispatch_ = 1
ITargetOut_vtables_ = [
	(( 'LayerThickness' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'LayerThickness' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfLayers' , 'Value' , ), 202, (202, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfElements' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 204, (204, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 204, (204, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddLayer' , 'Value' , ), 205, (205, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'InsertLayer' , 'lay' , 'Value' , ), 206, (206, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DeleteLayer' , 'lay' , 'Value' , ), 207, (207, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'AddElement' , 'lay' , 'Value' , ), 208, (208, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'DeleteElement' , 'lay' , 'el' , 'Value' , ), 209, (209, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 210, (210, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 210, (210, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'CreateTargetOut' , ), 211, (211, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'DestroyTargetOut' , ), 212, (212, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'Shift' , 'Value' , ), 213, (213, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Shift' , 'Value' , ), 213, (213, (), [ (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'Thickness' , 'Value' , ), 214, (214, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'DeleteAllLayer' , 'Value' , ), 215, (215, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 216, (216, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 216, (216, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'AddLayers' , 'NumLayers' , 'Value' , ), 217, (217, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'AddElements' , 'lay' , 'NumElements' , 'Value' , ), 218, (218, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'ElementZArray' , 'lay' , 'V' , ), 219, (219, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'ElementZArray' , 'lay' , 'V' , ), 219, (219, (), [ (3, 1, None, None) , 
			 (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentrationArray' , 'lay' , 'V' , ), 220, (220, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentrationArray' , 'lay' , 'V' , ), 220, (220, (), [ (3, 1, None, None) , 
			 (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'AddElementProperties' , 'lay' , 'Z' , 'c' , 'Value' , 
			 ), 221, (221, (), [ (3, 1, None, None) , (12, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'AsArray' , 'Value' , ), 222, (222, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'AsArray' , 'Value' , ), 222, (222, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
]

IWindow_vtables_dispatch_ = 1
IWindow_vtables_ = [
	(( 'LayerThickness' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'LayerThickness' , 'lay' , 'Value' , ), 201, (201, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfLayers' , 'Value' , ), 202, (202, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'LayerRoughness' , 'lay' , 'Value' , ), 203, (203, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerRoughness' , 'lay' , 'Value' , ), 204, (204, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerRoughness' , 'lay' , 'Value' , ), 204, (204, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'NumberOfElements' , 'lay' , 'Value' , ), 205, (205, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 206, (206, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ElementConcentration' , 'lay' , 'el' , 'Value' , ), 206, (206, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'AddLayer' , 'Value' , ), 207, (207, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'InsertLayer' , 'lay' , 'Value' , ), 208, (208, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'DeleteLayer' , 'lay' , 'Value' , ), 209, (209, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'AddElement' , 'lay' , 'Value' , ), 210, (210, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'DeleteElement' , 'lay' , 'el' , 'Value' , ), 211, (211, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 212, (212, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'ElementName' , 'lay' , 'el' , 'Value' , ), 212, (212, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'ElementAmount' , 'lay' , 'el' , 'Value' , ), 213, (213, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'ElementAmount' , 'lay' , 'el' , 'Value' , ), 213, (213, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'ReadLayer' , 'FileName' , 'LayerNr' , ), 214, (214, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'SaveLayerAs' , 'FileName' , 'LayerNr' , ), 215, (215, (), [ (8, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'ReadWindow' , 'FileName' , ), 216, (216, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'SaveWindowAs' , 'FileName' , ), 217, (217, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerPorosity' , 'lay' , 'Value' , ), 218, (218, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'HasLayerPorosity' , 'lay' , 'Value' , ), 218, (218, (), [ (3, 1, None, None) , 
			 (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'PorosityFraction' , 'lay' , 'Value' , ), 219, (219, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'PorosityFraction' , 'lay' , 'Value' , ), 219, (219, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'PoreDiameter' , 'lay' , 'Value' , ), 220, (220, (), [ (3, 1, None, None) , 
			 (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'PoreDiameter' , 'lay' , 'Value' , ), 220, (220, (), [ (3, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'Thickness' , 'Value' , ), 221, (221, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'DeleteAllLayer' , 'Valu' , ), 222, (222, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'lay' , 'Z' , 'Value' , ), 223, (223, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'StoppingFactor' , 'lay' , 'Z' , 'Value' , ), 223, (223, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 4 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 224, (224, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'ElementZ' , 'lay' , 'el' , 'Value' , ), 224, (224, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , ], 1 , 4 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'OpenMemory' , 'WS' , 'Value' , ), 225, (225, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'SaveMemory' , 'WS' , 'Value' , ), 226, (226, (), [ (16392, 2, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'Copy' , 'Window1' , 'Value' , ), 227, (227, (), [ (13, 1, None, "IID('{58312EB5-30F5-47D1-8E60-04634C214FBD}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{9F51F4E1-754F-11D5-B742-0040332FCEB4}' : IApp,
	'{9F51F4E3-754F-11D5-B742-0040332FCEB4}' : App,
	'{C22A1430-9329-11D5-B743-0040332FCEB4}' : ISetup,
	'{C22A1432-9329-11D5-B743-0040332FCEB4}' : Setup,
	'{5978B7E1-9706-11D5-B747-0040332FCEB4}' : ITarget,
	'{5978B7E3-9706-11D5-B747-0040332FCEB4}' : Target,
	'{54207F20-9D23-11D5-B748-0040332FCEB4}' : IFit,
	'{54207F22-9D23-11D5-B748-0040332FCEB4}' : Fit,
	'{DF418CC1-A5C6-11D5-B749-0040332FCEB4}' : ISpectrum,
	'{DF418CC3-A5C6-11D5-B749-0040332FCEB4}' : Spectrum,
	'{9DD33B20-A8EC-11D5-B749-0040332FCEB4}' : ICalc,
	'{9DD33B22-A8EC-11D5-B749-0040332FCEB4}' : Calc,
	'{0A40E4F1-D298-11D5-B752-0040332FCEB4}' : IStopping,
	'{0A40E4F3-D298-11D5-B752-0040332FCEB4}' : Stopping,
	'{2486C206-2AE3-4D27-8B96-F3384714119A}' : IProjectile,
	'{AB9D3C37-2FA9-434A-8959-8C84A8F50C97}' : Projectile,
	'{1C467EA5-494F-4FA4-A305-84183157CC48}' : ICrossSec,
	'{504EF515-68CF-495D-8D7C-C132E538D839}' : CrossSec,
	'{FF8D5AF3-63B8-42B5-B3EC-511F561E51F8}' : IFoil,
	'{F14C14DC-62BD-4C60-9710-A05CA0151546}' : Foil,
	'{2C926AE5-0CDA-45F2-BD6B-70031EFFB199}' : IWindow,
	'{58312EB5-30F5-47D1-8E60-04634C214FBD}' : Window,
	'{5DB47E27-5BA1-4FE3-8785-545F494FCBE2}' : ITargetOut,
	'{E45540BA-A7B0-4033-9E6F-B26230D41F69}' : TargetOut,
	'{A9E30D30-9792-4EF5-B5FE-81446FF50084}' : IForms,
	'{E31D2D47-3E2E-418B-93E3-8A8C72A7E6C2}' : Forms,
	'{A1F901AC-0EAB-485A-9945-A55DFC7E95D7}' : IPIGE,
	'{AB1B23A1-601F-465B-B2DB-F4BC15421B62}' : PIGE,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{9F51F4E1-754F-11D5-B742-0040332FCEB4}' : 'IApp',
	'{C22A1430-9329-11D5-B743-0040332FCEB4}' : 'ISetup',
	'{5978B7E1-9706-11D5-B747-0040332FCEB4}' : 'ITarget',
	'{54207F20-9D23-11D5-B748-0040332FCEB4}' : 'IFit',
	'{DF418CC1-A5C6-11D5-B749-0040332FCEB4}' : 'ISpectrum',
	'{9DD33B20-A8EC-11D5-B749-0040332FCEB4}' : 'ICalc',
	'{0A40E4F1-D298-11D5-B752-0040332FCEB4}' : 'IStopping',
	'{2486C206-2AE3-4D27-8B96-F3384714119A}' : 'IProjectile',
	'{1C467EA5-494F-4FA4-A305-84183157CC48}' : 'ICrossSec',
	'{FF8D5AF3-63B8-42B5-B3EC-511F561E51F8}' : 'IFoil',
	'{2C926AE5-0CDA-45F2-BD6B-70031EFFB199}' : 'IWindow',
	'{5DB47E27-5BA1-4FE3-8785-545F494FCBE2}' : 'ITargetOut',
	'{A9E30D30-9792-4EF5-B5FE-81446FF50084}' : 'IForms',
	'{A1F901AC-0EAB-485A-9945-A55DFC7E95D7}' : 'IPIGE',
}


NamesToIIDMap = {
	'IApp' : '{9F51F4E1-754F-11D5-B742-0040332FCEB4}',
	'ISetup' : '{C22A1430-9329-11D5-B743-0040332FCEB4}',
	'ITarget' : '{5978B7E1-9706-11D5-B747-0040332FCEB4}',
	'IFit' : '{54207F20-9D23-11D5-B748-0040332FCEB4}',
	'ISpectrum' : '{DF418CC1-A5C6-11D5-B749-0040332FCEB4}',
	'ICalc' : '{9DD33B20-A8EC-11D5-B749-0040332FCEB4}',
	'IStopping' : '{0A40E4F1-D298-11D5-B752-0040332FCEB4}',
	'IProjectile' : '{2486C206-2AE3-4D27-8B96-F3384714119A}',
	'ICrossSec' : '{1C467EA5-494F-4FA4-A305-84183157CC48}',
	'IFoil' : '{FF8D5AF3-63B8-42B5-B3EC-511F561E51F8}',
	'IWindow' : '{2C926AE5-0CDA-45F2-BD6B-70031EFFB199}',
	'ITargetOut' : '{5DB47E27-5BA1-4FE3-8785-545F494FCBE2}',
	'IForms' : '{A9E30D30-9792-4EF5-B5FE-81446FF50084}',
	'IPIGE' : '{A1F901AC-0EAB-485A-9945-A55DFC7E95D7}',
}


