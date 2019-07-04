from matplotlib import pyplot as plt
from scipy.fftpack import fftfreq
import numpy as np, os

# Importa as exceções da classe.
from Core.Error import ColorNotDefinedError, NotDefinedSignalsError, SignalNotExistError, TooManyNamesPassedError

# Classe responsável por plotar os sinais.
class Plotter:
	def __init__(self, windowtitle):
		# Armazena os sinais que devem ser plotados.
		self.signals = []

		# Título da janela.
		self.windowtitle = windowtitle

		# Cofigura o plotter.
		plt.switch_backend('TkAgg')
		
		# Insere o título na janela.
		mng = plt.get_current_fig_manager()
		mng.window.title(self.windowtitle)
	
	# Adiciona um sinal. Retorna True se foi substituído e False caso contrário.
	def add(self, signal):
		alreadyadded = signal.name in self.listnames()

		# Se o sinal já foi adicionado, remove-o.
		if alreadyadded:
			for i, el in enumerate(self.signals):
				if el.name == signal.name:
					del self.signals[i]

		self.signals.append(signal)
		return alreadyadded
	
	# Fecha a janela.
	def close(self):
		plt.close()
	
	# Verifica se um sinal já foi adicionado.
	def exists(self, name):
		return name in self.listnames()
	
	# Retorna um sinal pelo seu nome.
	def getbyname(self, name):
		# Verifica se o sinal foi definido.
		if not self.exists(name):
			raise SignalNotExistError(name)
		
		# Procura o objeto do sinal pelo seu nome para retorná-lo.
		for signal in self.signals:
			if signal.name == name:
				return signal
	
	# Retorna o nome de todos os sinais adicionados, em ordem crescente.
	def listnames(self):
		return sorted([i.name for i in self.signals])
	
	# Plota os gráficos.
	def plot(self, names, fftnames, hspace=0.6):
		# Verifica se há algo para plotar.
		if not self.signals:
			raise NotDefinedSignalsError()
		
		# Transforma os nomes em lista.
		if type(names) is not list:
			names = [names]
		
		if type(fftnames) is not list:
			fftnames = [fftnames]
		
		# Verifica se a quantidade de sinais informados é existente.
		if len(names) + len(fftnames) > len(self.signals):
			raise TooManyNamesPassedError(len(names) + len(fftnames), len(self.signals))
		
		signals = []
		
		for name, fftname in zip(names, fftnames):
			# Verifica se os sinais informados existem.
			if name not in self.listnames():
				raise SignalNotExistError(name)
			
			if fftname not in self.listnames():
				raise SignalNotExistError(fftname)
			
			signal = self.getbyname(name)
			fftsignal = self.getbyname(fftname)
			
			# Verifica se a cor do sinal foi definida.
			if not signal.color:
				raise ColorNotDefinedError(signal)

			if not fftsignal.color:
				raise ColorNotDefinedError(fftsignal)
			
			# Adiciona o objeto de cada sinal encontrado a partir do nome.
			signals.append([signal, fftsignal])
		
		# Ajusta o espaçamento entre os gráficos.
		plt.subplots_adjust(hspace=hspace)
		
		# Plota os sinais.
		for i, signal in enumerate(signals):
			# Plota o sinal no domínio do tempo.
			plt.subplot(len(signals), 2, (i*2)+1)
			plt.plot(signal[0].data, color=signal[0].color, linewidth=signal[0].linewidth)

			# O título no gráfico é o nome do sinal.
			plt.title(signal[0].name)

			# Verifica se foi definido um rótulo para o eixo horizontal.
			if signal[0].xlabel and i + 1 == len(signals):
				plt.xlabel(signal[0].xlabel)
			
			# Verifica se foi definido um rótulo para o eixo vertical.
			if signal[0].ylabel:
				plt.ylabel(signal[0].ylabel)
			
			N = signal[1].order
			T = 1.0 / signal[1].samplefreq

			x = np.linspace(0.0, 1.0/(2.0*T), N//2)
			y = 2.0/N * np.abs(signal[1].data[0:N//2])
			
			# Plota o sinal no domínio da frequência.
			plt.subplot(len(signals), 2, (i*2)+2)
			plt.plot(x, y, color=signal[1].color, linewidth=signal[1].linewidth)

			# O título no gráfico é o nome do sinal.
			plt.title(signal[1].name)

			# Verifica se foi definido um rótulo para o eixo horizontal.
			if signal[1].xlabel and i + 1 == len(signals):
				plt.xlabel(signal[1].xlabel)
			
			# Verifica se foi definido um rótulo para o eixo vertical.
			if signal[1].ylabel:
				plt.ylabel(signal[1].ylabel)
		
		# Não bloqueia o processo.
		plt.ion()
		
		# Finalmente, exibe a janela de plotagem.
		plt.show()