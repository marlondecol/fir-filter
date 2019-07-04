from os import path, sep
from scipy.fftpack import fft
from scipy.signal import firwin
from tkinter import Tk, filedialog as fd
import numpy as np

# Importa as exceções da classe.
from Core.Error import LoadingCanceledError, SavingCanceledError, SignalDataNotDefinedError, SignalFileNotFoundError, SignalFileNotSavedError

# Classe de um sinal.
class Signal:
	def __init__(self, name, color, fileformat=".txt", initialdir=None):
		# Nome do sinal.
		self.name = name

		# Configurações de plotagem.
		self.color = color
		self.xlabel = None
		self.ylabel = None
		self.linewidth = 0.75

		# Atributos específicos.
		self.data = None
		self.file = None
		self.order = None
		self.samplefreq = None

		# Diretório inicial para os diálogos.
		self.initialdir = self.signalsdir(initialdir)

		# Extensão de um arquivo de sinal.
		self.fileformat = fileformat

		# Configura as janelas de diálogo.
		root = Tk()
		root.withdraw()
	
	# Faz a convolução entre dois sinais, salva em um arquivo e retorna o sinal convoluído.
	def convolve(self, a, v, asktitle, asktype="Arquivo de texto"):
		# Verifica se os sinais já foram definidos.
		if a.data is None:
			raise SignalDataNotDefinedError(a)
		
		if v.data is None:
			raise SignalDataNotDefinedError(v)
		
		# Faz a convolução dos sinais.
		self.data = np.convolve(a.data, v.data)

		self.order = a.order
		self.samplefreq = a.samplefreq
		
		# Abre uma janela de diálogo para escolher onde salvar o arquivo do sinal resultante.
		outfile = fd.asksaveasfilename(initialdir=self.initialdir, title=asktitle, filetypes=[[asktype, self.fileformat]])

		# Se o usuário cancelou o salvamento.
		if not outfile:
			raise SavingCanceledError()
		
		# Salva o arquivo do sinal resultante.
		np.savetxt(outfile, self.data)

		# Verifica se o arquivo foi realmente salvo.
		if not path.isfile(outfile):
			raise SignalFileNotSavedError()
		
		self.file = outfile

		return self.data
	
	# Aplica a série de Fourier ao sinal.
	def fftbysignal(self, signal):
		self.data = fft(signal.data)

		self.order = signal.order
		self.samplefreq = signal.samplefreq
	
	# Gera um filtro FIR parametrizados.
	def genfir(self, samplefreq, cutfreq, order, filtertype, window):
		self.data = firwin(order, cutfreq, fs=samplefreq, window=window, pass_zero=filtertype)

		self.order = order
		self.samplefreq = samplefreq
	
	# Abre uma janela de diálogo para carregar o sinal de um arquivo e retorna seus dados.
	def load(self, asktitle, asktype="Arquivos de texto", askallfiles=True, dtype=float, delimiter="\n"):
		filetypes = [[asktype, self.fileformat]]

		# Verifica se deve ser mostrada a opção "Todos os arquivos".
		if askallfiles:
			filetypes.append(["Todos os arquivos", ".*"])
		
		infile = fd.askopenfilename(initialdir=self.initialdir, title=asktitle, filetypes=filetypes)

		# Se o usuário cancelou o carregamento.
		if not infile:
			raise LoadingCanceledError()

		# Verifica se o arquivo realmente existe.
		if not path.isfile(infile):
			raise SignalFileNotFoundError(infile)
		
		# Carrega os dados do arquivo.
		self.data = np.loadtxt(infile, dtype=dtype, delimiter=delimiter)
		self.order = len(self.data)

		self.file = infile

		return self.data
	
	# Retorna um diretório inicial conveniente para os diálogos.
	def signalsdir(self, trialpath=None):
		# Se o caminho do parâmetro existe, usa ele.
		if trialpath is not None and path.exists(trialpath):
			return trialpath
		
		# Possíveis diretórios iniciais para os diálogos, em ordem de prioridade.
		initialdirs = [
			"Sinais",
			"Signals",
			".." + sep + "Sinais",
			".." + sep + "Signals",
			# Caso nenhum exista, usa o diretório atual.
			"."
		]
		
		# Verifica qual dos possíveis diretórios existe.
		for i in initialdirs:
			if path.exists(i):
				# Se encontrou, finaliza a busca e retorna-o.
				return i