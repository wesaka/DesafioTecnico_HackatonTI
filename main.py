import re

expressao = input()
expressao = re.sub(r"\s+", "", expressao).upper()

# Procurar caracteres proibidos apos tirar o whitespace
if re.search(r"[^A-Z]", expressao) is not None:
    raise Exception('Caracteres invalidos foram encontrados', 'Apenas serao aceitas letras de \"A\" ate \"Z\" e espacos')

comp = len(expressao)

# Abrir o arquivo de palavras e guardar as palavras com tamanho correto numa lista
tc = []
with open('palavras.txt', 'r') as p:
    for linha in p:
        # deixar apenas as letras na palavra (tirar /n)
        l_strp = re.sub(r"\s+", "", linha).upper()

        # reduzir apenas para as palavras com a mesma quantidade de letras
        if len(l_strp) == comp:
            tc.append(l_strp)

# a partir de agora trabalhamos apenas com as palavas na lista tc (tamanho correto)
for palavra in tc:
    # transformo cada string em uma lista para ser ordenado
    palavra_list = list(palavra)
    expressao_list = list(expressao)

    palavra_list.sort()
    expressao_list.sort()

    if palavra_list == expressao_list:
        print(palavra)
