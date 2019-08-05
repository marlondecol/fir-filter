import numpy as np
# Importa os pacotes do projeto.
from Core.Plotter import Plotter
from Core.Signal import Signal
from Core.Utils import clear, lprint, luprint, lubprint, numerize, pressenterto

# Importa as exceções do projeto.
from Core.Error import (ColorNotDefinedError, LoadingCanceledError, NotDefinedSignalsError,
	SavingCanceledError, SignalDataNotDefinedError, SignalFileNotFoundError,
	SignalNotExistError, SignalFileNotSavedError, TooManyNamesPassedError)

# Imprime o título. A margem é em caracteres.
def printtitle(margin=2):
	# Não aceita margem negativa.
	margin = abs(margin) - margin % 2

	# Margens verticais são a metade da margem lateral.
	vmargin = margin / 2

	# Tipografia gerada em: http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=FIR%20Filter
	# Houve um alongamento de uma linha nas letras maiúsculas, apenas.
	lubprint("{:{margin}}".format("\n", margin=margin + 1).join([
		"███████╗██╗██████╗     ███████╗",
		"██╔════╝██║██╔══██╗    ██╔════╝██╗██╗  ████████╗███████╗██████╗",
		"█████╗  ██║██████╔╝    █████╗  ╚═╝██║  ╚══██╔══╝██╔════╝██╔══██╗",
		"██╔══╝  ██║██╔══██╗    ██╔══╝  ██╗██║     ██║   █████╗  ██████╔╝",
		"██║     ██║██║  ██║    ██║     ██║██║     ██║   ██╔══╝  ██╔══██╗",
		"██║     ██║██║  ██║    ██║     ██║███████╗██║   ███████╗██║  ██║",
		"╚═╝     ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝"
	]), margin, vmargin, vmargin)

# Carrega o sinal ruidoso a partir de um arquivo.
def loadfromfile(plotter):
	try:
		message = "Selecione o sinal ruidoso x[n]"

		luprint(message + "...", end="")

		noisy = Signal("Sinal ruidoso x[n]", "red")
		noisy.load(message)

		samplefreq = float(input("\n\n  Frequência de amostragem: "))
		
		# Caso a frequência seja inválida.
		if samplefreq < 0:
			raise ValueError()
		
		noisy.samplefreq = samplefreq

		noisyfft = Signal("Série de Fourier do sinal ruidoso x[n]", "red")
		noisyfft.fftbysignal(noisy)

		# Define os atributos do sinal.
		noisy.xlabel = "Tempo"
		noisy.ylabel = "Amplitude"

		# Define o eixo das abscissas da FFT.
		noisyfft.xlabel = "Frequência"

		# Adiciona o sinal ao plotter e plota-o.
		# Se já existe, o sinal é substituído pelo novo.
		replaced = plotter.add(noisy)
		plotter.add(noisyfft)
		plotter.plot(noisy.name, noisyfft.name)

		clear()

		luprint("Sinal carregado com sucesso!")

		if replaced:
			luprint("O sinal adicionado anteriormente foi substituído por este.")
	# Cor não definida.
	except ColorNotDefinedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não tem uma cor definida.".format(e.signal.name))
	# Carregamento cancelado.
	except LoadingCanceledError as e:
		clear()
		luprint("Carregamento cancelado!")
	# Nenhum sinal adicionado.
	except NotDefinedSignalsError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Nenhum sinal foi adicionado ao plotter.")
	# Arquivo não encontrado.
	except SignalFileNotFoundError as e:
		clear()
		luprint("Erro ao carregar o arquivo!")
		lprint("O arquivo \"{}\" não foi encontrado.".format(e.file))
	# Sinal não adicionado.
	except SignalNotExistError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não foi adicionado ao plotter.".format(e.name))
	# Muitos sinais informados.
	except TooManyNamesPassedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Deveriam ser plotados {:d} sinais, mas {} apenas {:d}.".format(e.nameslen, "existem" if e.signalslen > 1 else "existe", e.signalslen))
	# Frequência de amostragem inválida.
	except ValueError:
		clear()
		luprint("O valor informado é inválido!")
	
	pressenterto("voltar ao menu")

	plotter.close()

# Gera um filtro passa-baixas.
def genlowpass(plotter):
	try:
		lubprint("Defina os parâmetros do filtro h[n]:")

		samplefreq = float(input("  Frequência de amostragem: "))

		# Caso a frequência seja inválida.
		if samplefreq < 0:
			raise ValueError()
		
		cutfreq = float(input("  Frequência de corte:      "))

		# Caso a frequência seja inválida.
		if cutfreq < 0 or cutfreq >= samplefreq / 2.0:
			raise ValueError()
		
		order = int(input("  Comprimento do sinal:     "))

		# Caso a ordem seja inválida.
		if order < 0:
			raise ValueError()
		
		clear()

		message = "Selecione um arquivo para salvar o sinal de filtro h[n]"

		luprint(message + "...", end="")
		
		fir = Signal("Sinal de filtro h[n]", "blue")
		fir.genfir(samplefreq, cutfreq, order, "lowpass", "blackmanharris", message)

		firfft = Signal("Série de Fourier do sinal de filtro h[n]", "blue")
		firfft.fftbysignal(fir)

		# Define os atributos do sinal.
		fir.xlabel = "Tempo"
		fir.ylabel = "Amplitude"

		# Define o eixo das abscissas da FFT.
		firfft.xlabel = "Frequência"

		# Adiciona o sinal ao plotter e plota-o.
		# Se já existe, o sinal é substituído pelo novo.
		replaced = plotter.add(fir)
		plotter.add(firfft)
		plotter.plot(fir.name, firfft.name)

		clear()

		luprint("Sinal gerado com sucesso!")

		if replaced:
			luprint("O sinal gerado anteriormente foi substituído por este.")
	# Cor não definida.
	except ColorNotDefinedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não tem uma cor definida.".format(e.signal.name))
	# Nenhum sinal adicionado.
	except NotDefinedSignalsError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Nenhum sinal foi adicionado ao plotter.")
	# Salvamento cancelado.
	except SavingCanceledError as e:
		clear()
		luprint("Salvamento cancelado!")
	# Arquivo não foi salvo.
	except SignalFileNotSavedError as e:
		clear()
		luprint("Erro ao gerar o filtro!")
		lprint("O arquivo do sinal de filtro não pôde ser salvo.")
	# Sinal não adicionado.
	except SignalNotExistError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não foi adicionado ao plotter.".format(e.name))
	# Muitos sinais informados.
	except TooManyNamesPassedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Deveriam ser plotados {:d} sinais, mas {} apenas {:d}.".format(e.nameslen, "existem" if e.signalslen > 1 else "existe", e.signalslen))
	except ValueError:
		clear()
		luprint("O valor informado é inválido!")
	
	pressenterto("voltar ao menu")

	plotter.close()

# Gera um filtro passa-banda.
def genbandpass(plotter):
	try:
		lubprint("Defina os parâmetros do filtro h[n]:")

		samplefreq = float(input("  Frequência de amostragem:     "))

		# Caso a frequência seja inválida.
		if samplefreq < 0:
			raise ValueError()
		
		cutfreq1 = float(input("  Frequência de corte inferior: "))

		# Caso a frequência inferior seja inválida.
		if cutfreq1 < 0 or cutfreq1 >= samplefreq / 2.0:
			raise ValueError()
		
		cutfreq2 = float(input("  Frequência de corte superior: "))

		# Caso a frequência superior seja inválida.
		if cutfreq2 < 0 or cutfreq2 <= cutfreq1 or cutfreq2 >= samplefreq / 2.0:
			raise ValueError()
		
		order = int(input("  Comprimento do sinal:         "))

		# Caso a ordem seja inválida.
		if order < 0:
			raise ValueError()
		
		clear()

		message = "Selecione um arquivo para salvar o sinal de filtro h[n]"

		luprint(message + "...", end="")
		
		fir = Signal("Sinal de filtro h[n]", "blue")
		fir.genfir(samplefreq, [cutfreq1, cutfreq2], order, "bandpass", "blackmanharris", message)

		firfft = Signal("Série de Fourier do sinal de filtro h[n]", "blue")
		firfft.fftbysignal(fir)

		# Define os atributos do sinal.
		fir.xlabel = "Tempo"
		fir.ylabel = "Amplitude"

		# Define o eixo das abscissas da FFT.
		firfft.xlabel = "Frequência"

		# Adiciona o sinal ao plotter e plota-o.
		# Se já existe, o sinal é substituído pelo novo.
		replaced = plotter.add(fir)
		plotter.add(firfft)
		plotter.plot(fir.name, firfft.name)

		clear()

		luprint("Sinal gerado com sucesso!")

		if replaced:
			luprint("O sinal gerado anteriormente foi substituído por este.")
	# Cor não definida.
	except ColorNotDefinedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não tem uma cor definida.".format(e.signal.name))
	# Nenhum sinal adicionado.
	except NotDefinedSignalsError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Nenhum sinal foi adicionado ao plotter.")
	# Salvamento cancelado.
	except SavingCanceledError as e:
		clear()
		luprint("Salvamento cancelado!")
	# Arquivo não foi salvo.
	except SignalFileNotSavedError as e:
		clear()
		luprint("Erro ao gerar o filtro!")
		lprint("O arquivo do sinal de filtro não pôde ser salvo.")
	# Sinal não adicionado.
	except SignalNotExistError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não foi adicionado ao plotter.".format(e.name))
	# Muitos sinais informados.
	except TooManyNamesPassedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Deveriam ser plotados {:d} sinais, mas {} apenas {:d}.".format(e.nameslen, "existem" if e.signalslen > 1 else "existe", e.signalslen))
	except ValueError:
		clear()
		luprint("O valor informado é inválido!")
	
	pressenterto("voltar ao menu")

	plotter.close()

# Filtra o sinal ruidoso convoluindo-o com o sinal de filtro.
def filtersignal(plotter):
	try:
		# Verifica se os dois sinais foram definidos.
		a = plotter.getbyname("Sinal ruidoso x[n]")
		v = plotter.getbyname("Sinal de filtro h[n]")

		message = "Selecione um arquivo para salvar o sinal convoluído y[n]"

		luprint(message + "...", end="")

		clean = Signal("Sinal convoluído y[n]", "green")
		clean.convolve(a, v, message)

		cleanfft = Signal("Série de Fourier do sinal convoluído y[n]", "green")
		cleanfft.fftbysignal(clean)

		# Define os atributos do sinal.
		clean.xlabel = "Tempo"
		clean.ylabel = "Amplitude"

		# Define o eixo das abscissas da FFT.
		cleanfft.xlabel = "Frequência"

		# Adiciona o sinal ao plotter e plota-o.
		plotter.add(clean)
		plotter.add(cleanfft)
		plotter.plot(clean.name, cleanfft.name)

		clear()
		
		luprint("Sinais convoluídos com sucesso!")
		luprint("O arquivo foi salvo em: {}".format(clean.file))
	# Cor não definida.
	except ColorNotDefinedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("O sinal de nome \"{}\" não tem uma cor definida.".format(e.signal.name))
	# Nenhum sinal adicionado.
	except NotDefinedSignalsError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Nenhum sinal foi adicionado ao plotter.")
	# Salvamento cancelado.
	except SavingCanceledError as e:
		clear()
		luprint("Salvamento cancelado!")
	# Atributo data do sinal não definido.
	except SignalDataNotDefinedError as e:
		clear()
		luprint("Erro ao convoluir os sinais!")
		lprint("O sinal de nome \"{}\" não teve seus dados definidos.".format(e.signal.name))
	# Arquivo não foi salvo.
	except SignalFileNotSavedError as e:
		clear()
		luprint("Erro ao convoluir os sinais!")
		lprint("O arquivo do sinal convoluído não pôde ser salvo.")
	# Sinal não adicionado ao plotter.
	except SignalNotExistError as e:
		clear()
		luprint("Erro ao carregar um sinal!")
		lprint("O sinal de nome \"{}\" não foi adicionado ao plotter.".format(e.name))
	# Muitos sinais informados.
	except TooManyNamesPassedError as e:
		clear()
		luprint("Erro ao plotar o sinal!")
		lprint("Deveriam ser plotados {:d} sinais, mas {} apenas {:d}.".format(e.nameslen, "existem" if e.signalslen > 1 else "existe", e.signalslen))
	
	pressenterto("voltar ao menu")

	plotter.close()

# Plota todos os sinais.
def plotallsignals(plotter):
	# Verifica se há pelo menos um sinal para plotar.
	if not plotter.signals:
		luprint("Nenhum sinal foi adicionado ao plotter!")
		pressenterto("voltar ao menu")
		return
	
	# Sinais que devem ser plotados, em sua devida ordem.
	signals = [
		"Sinal ruidoso x[n]",
		"Sinal de filtro h[n]",
		"Sinal convoluído y[n]"
	]
	
	fftsignals = [
		"Série de Fourier do sinal ruidoso x[n]",
		"Série de Fourier do sinal de filtro h[n]",
		"Série de Fourier do sinal convoluído y[n]"
	]
	
	# Verifica quais dos sinais ainda não foi adicionado para que seja excluído.
	signals = [i for i in signals if plotter.exists(i)]
	fftsignals = [i for i in fftsignals if plotter.exists(i)]

	try:
		luprint("Sinais plotados:")

		# Printa uma lista dos sinais plotados.
		luprint("\n  ".join(numerize(signals)))

		# Plota os sinais.
		plotter.plot(signals, fftsignals)

		luprint("Operação realizada com sucesso!")
	# Cor não definida.
	except ColorNotDefinedError as e:
		clear()
		luprint("Erro ao plotar os sinais!")
		lprint("O sinal de nome \"{}\" não tem uma cor definida.".format(e.signal.name))
	# Nenhum sinal adicionado.
	except NotDefinedSignalsError as e:
		clear()
		luprint("Erro ao plotar os sinais!")
		lprint("Nenhum sinal foi adicionado ao plotter.")
	# Sinal não adicionado ao plotter.
	except SignalNotExistError as e:
		clear()
		luprint("Erro ao carregar um sinal!")
		lprint("O sinal de nome \"{}\" não foi adicionado ao plotter.".format(e.name))
	# Muitos sinais informados.
	except TooManyNamesPassedError as e:
		clear()
		luprint("Erro ao plotar os sinais!")
		lprint("Deveriam ser plotados {:d} sinais, mas {} apenas {:d}.".format(e.nameslen, "existem" if e.signalslen > 1 else "existe", e.signalslen))

	pressenterto("voltar ao menu")

	plotter.close()

# Instancia o plotter.
plotter = Plotter("FIR Filter")

# Menu principal do programa.
while True:
	clear()
	printtitle()

	lprint("Bem-vindo ao FIR Filter!")

	# Menu principal.
	options = [
		["Carregar sinal ruidoso de um arquivo", "loadfromfile"],
		["Gerar um filtro passa-baixas", "genlowpass"],
		["Gerar um filtro passa-banda", "genbandpass"],
		["Convoluir os sinais", "filtersignal"],
		["Plotar todos os sinais", "plotallsignals"]
	]

	luprint("O que deseja fazer?\n")
	
	# Lista as opções.
	for i, opt in enumerate(options):
		lprint("[{:d}] {}".format(i + 1, opt[0]))
	
	lprint("[0] Sair")

	# Lê a opção escolhida pelo usuário.
	try:
		opt = int(input("\n  Sua opção: "))
		
		# Verifica se a opção existe.
		if opt not in range(0, len(options) + 1):
			raise ValueError()
	except ValueError:
		luprint("Opção inválida!")
		pressenterto("tentar novamente")
		continue
	
	clear()
	
	# Se a opção for 0, sai do programa.
	if not opt:
		break

	# Senão, executa a opção correspondente.
	locals()[options[opt - 1][1]](plotter)

printtitle()

# Agradecimentos e encerramento do programa.
lprint("Muito obrigado por utilizar o FIR Filter!")

luprint("Desenvolvido por:")

luprint("Lucas Giaretta Medeiros")
lprint("Marlon Luís de Col")
lprint("Matheus Welter Groth")
lprint("Mauricio Nathan Centenaro")

luprint("Engenharia de Computação")
lprint("2019 - Unoesc Chapecó")

pressenterto("finalizar")

print()

clear()