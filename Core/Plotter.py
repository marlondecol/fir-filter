from matplotlib import pyplot as plt
import os

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
	def plot(self, names, hspace=0.6):
		# Verifica se há algo para plotar.
		if not self.signals:
			raise NotDefinedSignalsError()
		
		# Transforma os nomes em lista.
		if type(names) is not list:
			names = [names]
		
		# Verifica se a quantidade de sinais informados é existente.
		if len(names) > len(self.signals):
			raise TooManyNamesPassedError(len(names), len(self.signals))
		
		signals = []
		
		for name in names:
			# Verifica se o sinal informado existe.
			if name not in self.listnames():
				raise SignalNotExistError(name)
			
			signal = self.getbyname(name)
			
			# Verifica se a cor do sinal foi definida.
			if not signal.color:
				raise ColorNotDefinedError(signal)
			
			# Adiciona o objeto de cada sinal encontrado a partir do nome.
			signals.append(signal)
		
		# Ajusta o espaçamento entre os gráficos.
		plt.subplots_adjust(hspace=hspace)
		
		# Plota os sinais.
		for i, signal in enumerate(signals):
			# Divide a janela de plotagem.
			plt.subplot(len(signals), 1, i + 1)

			plt.plot(signal.data, color=signal.color, linewidth=signal.linewidth)

			# O título no gráfico é o nome do sinal.
			plt.title = signal.name

			# Verifica se foi definido um rótulo para o eixo horizontal.
			if signal.xlabel and i + 1 == len(signals):
				plt.xlabel = signal.xlabel
			
			# Verifica se foi definido um rótulo para o eixo vertical.
			if signal.ylabel:
				plt.ylabel = signal.ylabel
		
		# Não bloqueia o processo.
		plt.ion()
		
		# Finalmente, exibe a janela de plotagem.
		plt.show()