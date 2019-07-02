from os import name, system

# Limpa a tela executando o comando específico do sistema operacional.
def clear():
	system("cls" if name == "nt" else "clear")

# Faz um print com uma margem de N caracteres à esquerda, apenas.
def lprint(text, left=2, end="\n"):
	luprint(text, left, 0, end)

# Faz um print com uma margem de N caracteres à esquerda e N linhas acima e abaixo.
def lubprint(text, left=2, top=1, bottom=1, end="\n"):
	print("{top}{:>{left}}{bottom}".format(str(text), left=abs(int(left)) + len(str(text)), top="\n" * abs(int(top)), bottom="\n" * abs(int(bottom))), end=end)

# Faz um print com uma margem de N caracteres à esquerda e N linhas acima.
def luprint(text, left=2, top=1, end="\n"):
	lubprint(text, left, top, 0, end)

# Gera uma lista enumerada. A margem é em caracteres.
def numerize(entries):
	return ["{:>{width}}. {}".format(i, opt, width=len(str(len(entries)))) for i, opt in enumerate(entries)]

# Mostra a mensagem "Pressione [ENTER] para [tomessage]...".
def pressenterto(tomessage, key="ENTER"):
	input("\n  Pressione [{}] para {}...".format(key.upper(), tomessage.lower()))