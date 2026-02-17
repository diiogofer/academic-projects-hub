#Representação do Território e das Interseções

def eh_territorio(arg):
    """eh_territorio: Universal ---> Booleano

    Verifica se arg é um território (True) ou se não é (False).
    Um território é uma estrutura formada por caminhos verticais 
    e horizontais. É um tuplo de tuplos onde cada subtuplo é um 
    caminho vertical (max 26 ccaminhos) e cada elemento de um 
    subtuplo é uma interseção (max 99) com valor 1 (interseção 
    montanhosa) ou 0 (interseção vazia). Todos os subtuplos têm 
    o mesmo tamanho.

    Não levanta erros.
   
    """

    #Verifica se o território é um tuplo com no máximo 26 caminhos verticais (letras do alfabeto)
    if type(arg)!=tuple or len(arg) > 26 or len(arg)==0:
        return False
    
    else:       
        #percorre os tuplos verificando o seu comprimento e os valores (válidos para representar uma interseção)
        for Nv in arg:
            if type(Nv)!=tuple or len(Nv) > 99 or len(Nv) == 0: #tuplos numerados de 1 até 99 (no máximo)
                return False
            #obtém comprimento do primeiro tuplo para termo de comparação (referência)
            comprimento_territorio = len(arg[0])
            if len(Nv)!= comprimento_territorio:
                return False
            #percorre cada elemento dos tuplos verificando os seus valores
            for Nh in Nv:
                if Nh != 0 and Nh != 1:
                    return False
                if type(Nh)!=int:
                    return False
    return True



def obtem_ultima_intersecao(t):
    """obtem_ultima__intersecao: Território ---> Interseção
    
    Devolve a última interseção (extremo superior direito) de um território (t).
    Retorna Falso se t não é um território.

    Não levanta erros.

    """
    #Verifica se é Território
    if not eh_territorio(t):
        return False
    
    else:
        #obtém a última letra com base na tabela de ASCII
        ultima_letra = chr(ord('A') + len(t) - 1)
        #obtém a último número com base no tamanho do primeiro tuplo do território
        ultimo_numero = len(t[0])
        ultima_intersecao = ultima_letra,ultimo_numero
        return ultima_intersecao
    

def eh_intersecao(arg):
    """eh_intersecao: Universal ---> Booleano

    Verifica se arg é uma interseção (True) ou não (False).
    Uma interseção é um tuplo de dois elementos, cujo primeiro 
    elemento é uma letra maiúscula e o segundo elemento é um
    número inteiro de 1 a 99.
    
    Não levanta erros. 

    """
    #Verifica se é um tuplo de tamanho 2 contendo uma string e um inteiro
    if type(arg)==tuple and len(arg)==2:
        if type(arg[0])==str and len(arg[0])==1 and type(arg[1])==int:
            #Verifica se a string é válida 
            if not(ord('A') <= ord(arg[0]) <= ord('Z')):
                return False
            #Verifica se o número é válido
            if not 1 <= arg[1] <= 99:
                return False
            return True
        
    return False

def eh_intersecao_valida(t, i):
    """eh_intersecao_valida: Território x Interseção ---> Booleano
    
    Verifica se i é uma interseção pertencente ao território t, 
    devolvendo True se o for ou False se não o for.

    Não levanta erros.

    """
    #Verifica se é um território e se é uma interseção
    if eh_territorio(t) and eh_intersecao(i):
        numero_colunas = len(t)
        numero_linhas = len(t[0])
        letra_máxima_ascii = (ord('A') + numero_colunas - 1 )
        #Verifica se a interseção é válida para o território
        if not(ord("A") <= ord(i[0]) <= letra_máxima_ascii and 1 <= i[1]<= numero_linhas):
            return False
        return True
    return False
    
def eh_intersecao_livre(t, i):
    """eh_intersecao_livre: Território x Interseção ---> Booleano
    
    Verifica se a interseção i do território t é uma interseção 
    livre/sem montanhas (True) ou se não o é (False).
    True caso o segundo elemento do tuplo seja 0 e False caso 
    seja 1.

    Não levanta erros. 

    """
    if not(eh_territorio(t) and eh_intersecao_valida(t, i)):
        return False

    letra, numero = i #Por questões de legibilidade
    caminho_vertical = ord(letra)-ord("A") #Ver tabela ASCII
    caminho_horizontal = numero - 1 # O índice do 1º elemento é 0

    if t[caminho_vertical][caminho_horizontal] == 0:
        return True
    return False


#Função adicional
def cria_dicionario_intersecoes(t):
    """cria_dicionario_intersecoes: Território ---> Dicionário
    
    Cria um dicionário com as interseções do território t, 
    como chave, e com 0 ou 1, como valor, consoante não têm 
    ou têm montanha.

    Não levanta erros.

    """
    if not eh_territorio(t):
       return False

    dicionario_intersecoes = {}
    numero_colunas = len(t)
    numero_linhas = len(t[0])

    for coluna in range(numero_colunas):
        letra = chr(ord('A') + coluna)
        for linha in range(numero_linhas):
            numero = linha + 1
            intersecao = (letra, numero) #chave do dicionário
            valor_intersecao = t[coluna][linha] #valor
            dicionario_intersecoes[intersecao] = valor_intersecao 
    return dicionario_intersecoes
   

def obtem_intersecoes_adjacentes(t, i):
    """obtem_intersecoes_adjacentes: Território x Interseção ---> Tuplo
    
    Recebe uma interseção i de um território t e devolve as 
    interseções adjacentes a i, pela ordem de leitura estabelecida
    (esquerda para a direita, baixo para cima).

    Não levanta erros.

    """
    if not(eh_territorio(t) and eh_intersecao_valida):
       return False
    else:
        intersecoes_reais = [] #armazena interseções adjacentes reais
        letra = i[0]
        numero_linha = i[1]
        simbolo_seguinte_ASCII = chr(ord(letra)+1)
        simbolo_anterior_ASCII = chr(ord(letra)-1)
    
        dicionario_intersecoes_validas = cria_dicionario_intersecoes(t) #dicionário com todas as interseções de t
        #4 possíveis adjacentes à interseção:
        possiveis_adjacentes = [(simbolo_seguinte_ASCII, numero_linha),\
                            (simbolo_anterior_ASCII, numero_linha), \
                            (letra, numero_linha + 1), \
                            (letra, numero_linha - 1)]
    #se a interseção possível adjacente estiver no dicionário, então é uma interseção real
    for intersecao_possivel in possiveis_adjacentes:
        if intersecao_possivel in dicionario_intersecoes_validas:
            intersecoes_reais.append(intersecao_possivel)
    
    intersecoes_reais.sort(key = lambda intersecao:  (intersecao[1], intersecao[0])) #ordenação
    return tuple(intersecoes_reais)



def ordena_intersecoes(tup):
    """ ordena_interseções: Tuplo ---> Tuplo
    
    Recebe um conjunto de interseções (em tuplo) e ordena-as em modo de
    leitura de um território (esquerda para a direita e baixo para cima).

    Não levanta erros.

    """
    if type(tup)!=tuple:
        return False
    
    if tup == ():
        return ()
    
    for intersecoes in tup:
        if eh_intersecao(intersecoes):
            intersecoes_ordenadas = tuple(sorted(tup, key=lambda intersecao:  (intersecao[1], intersecao[0]))) #sem o tuple devolveria uma lista
            return intersecoes_ordenadas   
        return False #caso seja uma interseção inválida

def territorio_para_str(t):
    """territorio_para_str: Território ---> Cadeia de Caracteres
    
    Recebe um território e converte-o na sua representação externa 
    (representação "para os nossos olhos") em cadeia de carateres.

    Levanta erro se o argumento é inválido.

    """
    if not eh_territorio(t):
        raise ValueError('territorio_para_str: argumento invalido')

    numero_linhas = len(t[0])
    numero_colunas = len(t)
    territorio_str = [] #lista para armazenar cada linha gerada
    #Parte de cima (= Parte de baixo)
    letras = "   " + " ".join(chr(ord('A') + coluna) for coluna in range(numero_colunas))
    territorio_str.append(letras)
    #Parte Intermédia
    for linha in range(numero_linhas - 1, -1, -1):
        linha_str = "".join(f"{str(linha + 1)}" if (linha + 1)>=10 else f" {str(linha + 1)}") #Adiciona números à esquerda, respeitando os espaçamentos aceites
        linha_str += "".join(" X" if t[coluna][linha] == 1 else " ." for coluna in range(numero_colunas)) #Adicona pontos ou cruzes, respeitando os espaçamentos aceites
        linha_str += "".join(f" {str(linha + 1)}" if (linha + 1)>=10 else f"  {str(linha + 1)}")  # Adiciona os números à direita, respeitando os espaçamentos aceites
        territorio_str.append(linha_str)
    #Parte de baixo
    territorio_str.append(letras)  # Adiciona as letras de baixo
    return "\n".join(territorio_str) #return como string com quebras de linha


#Funcões das cadeias de montanhas e dos vales


def obtem_cadeia(t,i):
    """obtem_cadeia: ---> Território x Interseção ---> Tuplo
    
    Recebe uma interseçao i (livre ou não) de um território t e devolve
    todas as interseções que estão conectadas a i, ou seja, que em 
    conjunto com esta formam uma cadeia de montanhas ou uma cadeia 
    de interseções livres

    Levanta erro se os argumentos são inválidos.

    """
    if not eh_intersecao_valida(t, i):
        raise ValueError('obtem_cadeia: argumentos invalidos')
    else:
        cadeia = [(i),] #lista com interseção inicial
        resultado = [] #para armazenar interseções da cadeia
        
        while len(cadeia) != 0:
            resultado.append(cadeia[0])
            cadeia.remove(cadeia[0])
            adjacentes = obtem_intersecoes_adjacentes(t, resultado[-1]) #interseções adjacentes da última interseção da lista resutado

            for percorrer in adjacentes: 
                if eh_intersecao_livre(t, percorrer) == eh_intersecao_livre(t, i): #verifica se a interseção tem o mesmo valor que a inicial (se é livre ou não)
                    if percorrer not in resultado and percorrer not in cadeia:
                        cadeia.append(percorrer) #adiciona interseção à cadeia

        return ordena_intersecoes(tuple(resultado))
        
    
def obtem_vale(t, i):
    """obtem_vale: Território x Interseção ---> Tuplo

    Recebe uma interseção i de um território t e devolve as interseções que fazem
    parte do vale da cadeia de montanhas formada por i.
    Vale: conjunto de interseções livres adjacentes a uma montanha/cadeia de montanhas.

    Levanta erro se os argumentos são inválidos, ou seja, se t não é um território,
    i não é uma interseção pertencente a t, se i não é uma interseção e se i é 
    uma interseção livre.
    
    """
    if not eh_intersecao_valida(t, i):
        raise ValueError('obtem_vale: argumentos invalidos')
    if eh_intersecao_livre(t,i):
        raise ValueError('obtem_vale: argumentos invalidos')
    cadeia_montanhosa = obtem_cadeia(t,i) #obtem cadeia de montanhas
    adjacentes = []
    vales = []
    #obtem adjacentes para cada motanha da cadeia montanhosa:
    for interseções in cadeia_montanhosa:
        adjacentes.extend(obtem_intersecoes_adjacentes(t,interseções))
    #se interseção não está na cadeia_motntanhosa e ainda não está nem na lista vales, então é um vale válido
    for interseções in adjacentes: 
        if interseções not in cadeia_montanhosa and interseções not in vales:
            vales.append(interseções)
    return ordena_intersecoes(tuple(vales))
    


#Funções Informação de um Território


def verifica_conexao(t,i1,i2):
    """verifica_conexao: Território x Interseção x Interseção ---> Booleano
    
    Verifica se duas interseções (i1 e i2) de um território 
    t estão conectadas (True) ou não (False).
    Interseções (ocupadas ou livres) conectadas: é possível 
    traçar um percurso entre uma e outra passando apenas por 
    interseções adjacentes (ocupadas ou livres).

    Levanta erro se os argumentos são inválidos, ou seja, se 
    t não é um território, se as interseções não são válidas 
    para esse território e se não são interseções.

    """
    if not (eh_intersecao_valida(t, i1) and eh_intersecao_valida(t, i2)):
        raise ValueError('verifica_conexao: argumentos invalidos')
    else:
        cadeia = obtem_cadeia(t,i1)
        if i2 not in cadeia: #se i2 não está na cadeia de i1 então não estão conectados
            return False
        return True

def calcula_numero_montanhas(t):
    """calcula_numero_montanhas: Território ---> Inteiro

    Calcula o número de interseções ocupadas (montanhas) de um territóro t.
    Estas interseções têm valor 1.

    Levanta erro caso o argumento seja inválido.

    """
    if not eh_territorio(t):
        raise ValueError('calcula_numero_montanhas: argumento invalido')
    total_montanhas = 0
    for Nv in t: #percorre caminhos verticais
        for Nh in Nv: #percorre caminhos horizontais
            if Nh == 1: # valor 1 = interseção montanhosa
                total_montanhas = total_montanhas + 1

    return total_montanhas

def calcula_numero_cadeias_montanhas(t):
    """calcula_numero_cadeias_montanhas: Território ---> Inteiro

    Calcula o número de cadeias de montanhas de um território t.
    Cadeia de montanhas: conjunto de uma ou mais interseções ocupadas 
    conectadas entre si sem estarem conectadas a nenhuma outra montanha.

    Levanta erro se o argumento for inválido.

    """

    if not eh_territorio(t):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')
    else:
        
        dicionario_interseções = cria_dicionario_intersecoes(t)
        lista_montanhas = []
        #criação da lista com interseções montanhosas a partir do dicionário de interseções
        for interseções in dicionario_interseções:
            if dicionario_interseções[interseções] == 1: #só importam montanhas
                lista_montanhas.append(interseções)
        #Para cada interseção montanhosa obtem-se a sua cadeia montanhosa (geram-se repetições):
        lista_cadeias = []
        for interseções in lista_montanhas:
            lista_cadeias.append(obtem_cadeia(t, interseções))
        #Remoção das repetições:
        lista_cadeias_final = []
        for cadeias in lista_cadeias:
            if cadeias not in lista_cadeias_final:
                lista_cadeias_final.append(cadeias)

    return len(lista_cadeias_final)
    

def calcula_tamanho_vales(t):
    """calcula_tamanho_vales: Território ---> Inteiro
    
    Calcula o número total de interseções diferentes que 
    formam os vales das cadeias de montanhas do território t.

    Levanta erro se o argumento é inválido.

    """
    if not eh_territorio(t):
        raise ValueError('calcula_tamanho_vales: argumento invalido')
    else:
        todas_montanhas = []
        todas_interseções = cria_dicionario_intersecoes(t) #dicionário das interseções de t
        for interseções in todas_interseções:
            if todas_interseções[interseções] == 1:
               todas_montanhas = todas_montanhas + [interseções] #lista só com montanhas

        todos_os_vales = []
        for interseções in todas_montanhas:
            vale = obtem_vale(t, interseções) #obtém o vale de todas as interseções montanhosas
            for elementos in vale:
                if elementos not in todos_os_vales: #evita que se repita a adição de um vale já adicionado
                    todos_os_vales.append(elementos)
    return len(todos_os_vales)