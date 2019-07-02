# Classe pai.
class FIRError(Exception):
	pass



# Classes filhas.
class FIRPlotError(FIRError):
	pass

class FIRSignalError(FIRError):
	pass



# Classes herdadas de FIRPlotError.
class ColorNotDefinedError(FIRPlotError):
	def __init__(self, signal):
		self.signal = signal

class NotDefinedSignalsError(FIRPlotError):
	pass

class SignalNotExistError(FIRPlotError):
	def __init__(self, name):
		self.name = name

class TooManyNamesPassedError(FIRPlotError):
	def __init__(self, nameslen, signalslen):
		self.nameslen = nameslen
		self.signalslen = signalslen



# Classes herdadas de FIRSignalError.
class LoadingCanceledError(FIRSignalError):
	pass

class SavingCanceledError(FIRSignalError):
	pass

class SignalDataNotDefinedError(FIRSignalError):
	def __init__(self, signal):
		self.signal = signal

class SignalFileNotFoundError(FIRSignalError):
	def __init__(self, file):
		self.file = file

class SignalFileNotSavedError(FIRSignalError):
	pass