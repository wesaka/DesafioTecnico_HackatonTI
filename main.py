import re
import itertools


# Retorna a lista de palavras
def lista_palavras():
    lista = []
    with open('palavras.txt', 'r') as p:
        for linha in p:
            # deixar apenas as letras na palavra (tirar /n)
            l_strp = re.sub(r"\s+", "", linha).upper()

            # Guardar todas as palavras numa lista
            lista.append(l_strp)
    return lista


# Dá Exception se o string não for válido
def validar(string):
    # Procurar caracteres proibidos apos tirar o whitespace
    if re.search(r"[^A-Z]", string) is not None:
        raise Exception('Caracteres invalidos foram encontrados',
                        'Apenas serao aceitas letras de \"A\" ate \"Z\" e espacos')


# Retorna uma lista com todos os sub-anagramas possiveis para determinada palavra
def achar_todos_anagramas(list_string, string):
    la = []
    chars_string = list(string)

    for s in list_string:
        sub = list(s)

        if set(sub).issubset(chars_string):
            la.append(s)

    return la


# Retorna uma lista com todos os comprimentos de sub-anagramas existentes
def lista_comprimentos(list_string):
    lc = []
    for s in list_string:
        if len(s) not in lc:
            lc.append(len(s))

    return lc


# Retorna um mapa organizado com a chave sendo o comprimento do sub-anagrama e o valor uma lista com todos eles
def organizar_mapa_comprimentos(list_string):
    moc = {}
    for s in list_string:
        if len(s) not in moc.keys():
            moc[len(s)] = [s]
        else:
            moc[len(s)].append(s)

    return moc


# Retorna uma lista com várias listas contendo todas as combinacoes possiveis de comprimentos de sub-anagramas que
# resultem no comprimento da expressao inicial
# Autor dessa função: https://stackoverflow.com/users/1903116/thefourtheye
# Minha solução incial era extremamente ineficience - Esta é mais rapida e compreensiva que achei
def todas_combinacoes_possiveis(lst, target, with_replacement=False):
    def _todas_combinacoes_possiveis(idx, l, r, t, w):
        if t == sum(l):
            r.append(l)
        elif t < sum(l):
            return
        for u in range(idx, len(lst)):
            _todas_combinacoes_possiveis(u if w else (u + 1), l + [lst[u]], r, t, w)
        return r

    return _todas_combinacoes_possiveis(0, [], [], target, with_replacement)


# Checar se existem sub-anagramas repetidos via comparacao do tamanho do tuple e do set(tuple)
def checar_repeticao(list_checagem):
    return not len(set(list_checagem)) == len(list_checagem)


# Faz a classificacao final e retorna uma lista com todos os anagramas possiveis
# Esse é o coração do programa e aqui que é gasto a maior quantidade de tempo
def classificacao_final(string, list_comb, mapa_comb):
    lista_possibilidades = []

    for combinacao in list_comb:
        # Organizar as combinacoes numa lista iterable - tirar do mapa com comprimentos
        lista_temp = []
        for item in combinacao:
            lista_temp.append(mapa_comb[item])

        possibilidade = list(itertools.product(*lista_temp))

        # Remover palavras repetidas
        possibilidade[:] = itertools.filterfalse(checar_repeticao, possibilidade)

        # Checar se isso é um anagrama válido
        for p in possibilidade:
            # transformo cada string em uma lista para ser ordenado
            caracteres_possibilidade = list(''.join(p))
            caracteres_string = list(string)

            # Realizar a checagem de anagrama
            caracteres_possibilidade.sort()
            caracteres_string.sort()

            # Organizar cada conjunto de anagramas por ordem alfabetica
            list_p = sorted(list(p))

            if caracteres_possibilidade == caracteres_string and list_p not in lista_possibilidades:
                lista_possibilidades.append(list_p)

    return lista_possibilidades


expressao = input()
expressao = re.sub(r"\s+", "", expressao).upper()

# Validar a expressao inicial
validar(expressao)

# Carregar as palavras do arquivo numa lista
lista = lista_palavras()

# Achar todos os anagramas possíveis
todos = achar_todos_anagramas(lista, expressao)

# Achar a combinação de palavras que forme o total de caracteres na expressao original
lista_comp = lista_comprimentos(todos)

# Organizar as possibilidades num mapa
mapa_organizado = organizar_mapa_comprimentos(todos)

# Achar todas as combinacoes de comprimentos que possam ser a solucao
combinacoes = todas_combinacoes_possiveis(lista_comp, len(expressao), True)

# Agora achar quais são as palavras que podem se encaixar nas combinacoes
lista_possibilidades_final = classificacao_final(expressao, combinacoes, mapa_organizado)

# Classificar por ordem alfabetica cada item na lista que será apresentada
lista_possibilidades_final = sorted(lista_possibilidades_final, key=lambda x: x[0])
for possib in lista_possibilidades_final:
    print(*possib)
