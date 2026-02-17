"""
TAD interseção (Assinatura)
Representação interna da interseção -> Tuplo

Construtor:

---> cria_intesecao: str x int -> tuple (intersecao)
cria_intersecao(col,lin) cria uma interseção (tuplo) constituida 
por uma letra (A a S) e um inteiro (1 a 19) para tabuleiros de Go.


Seletores:

---> obtem_col: intersecao -> str (coluna)
obtem_col(i) recebe uma interseção e devolve a respetiva coluna (letra de A a S).

---> obtem_lin: intersecao -> int (linha)
obtem_lin(i) recebe uma interseção e devolve a respetiva linha (inteiro de 1 a 19).


Reconhecedor:

---> eh_intersecao: universal -> {True, False}
eh_intersecao(arg) tem valor True se arg é um TAD intersecao e False caso contrário.


Teste:

---> intersecoes_iguais: interseção x interseção -> {True, False}
intersecoes_iguais(i1, i2) tem valor True se as duas interseções são iguais e False caso contrário.


Transformadores:

--->intersecao_para_str(i): intersecao -> str
intersecao_para_str(i) transforma uma interseção (tuplo) numa string que a representa, "letra"+"inteiro".

--->str_para_intersecao(s): str -> interseção
str_para_intersecao(s): transforma uma string, "letra"+"inteiro", numa interseção (tuplo).


Alto Nível:

--->obtem_intersecoes_adjacentes: intersecao x intersecao -> tuple
obtem_intersecoes_adjacentes(i, l) recebem uma interseção qualquer do tabuleiro e a interseção superior direita 
e devolve o tuplo com as interseções adjacentes à primeira, por ordem de leitura.

--->ordena_intersecoes: tuple -> tuple
ordena_intersecoes(t) recebe um tuplo de interseções e devolve o tuplo com as interseções ordenadas
da esquerda para a direita e de baixo para cima (ordem de leitura de um tabuleiro de Go).

"""
#TAD interseção

#Consctrutor
def cria_intersecao(col,lin):
    """ Cria uma interseção válida para um tabuleiro de GO, com uma letra e um inteiro.
    Args:
        col (str): A letra da coluna (A a S).
        lin (int): O número da linha (1 a 19).
    Returns:
        tuple --> intersecao (col, lin)
    Raises: 
        ValueError: argumentos inválidos.
    """

    i = (col,lin) # ---> Interseção
    #Verificações:
    if eh_intersecao(i)==False: 
        raise ValueError('cria_intersecao: argumentos invalidos')
    return i

#Seletores
def obtem_col(i):
    """ Devolve a coluna da interseção i.
    Args:
        i (intersecao): (col,lin) --> tuplo com letra (A a S) e número (1 a 19).
    Returns:
        str --> letra da coluna da interseção.
    Raises: 
        Não tem.
    """
    #Primeiro elemento do tuplo (Letra)
    return i[0]

def obtem_lin(i):
    """ Devolve a linha da interseção i.
    Args:
        i (intersecao): (col,lin) --> tuplo com letra (A a S) e número (1 a 19).
    Returns:
        int --> número da linha da interseção.
    Raises:
        Não tem. 
    """
    #Segundo elemento do tuplo (Inteiro)
    return i[1]

#Reconhecedor

def eh_intersecao(arg):
    """ Verifica se arg é uma interseção de um tabuleiro GO.
    Args:
        intersecao: (col,lin) --> tuplo com letra (A a S) e número (1 a 19).
    Returns:
        bool --> True se arg é TAD intersecao e False caso contrário.
    Raises: 
        Não tem.
    """
    #Tuplo, tamanho dois, letra maiúscula de A a S e número inteiro de 1 a 19
    if not(type(arg)==tuple and len(arg)==2 \
        and type(arg[0]) == str and len(arg[0])==1 and arg[0] in "ABCDEFGHIJKLMNOPQRS" \
        and type(arg[1])==int and 1<=arg[1]<=19):
        return False
    return True

#Teste

def intersecoes_iguais(i1, i2):
    """ Verifica se as interseções i1 e i2 são iguais.
    Args:
        i1,i2: intersecao1 x intersecao2 --> (lin1,col1) x (lin2,col2).
    Returns:
        bool: True se i1 e i2 são interseções iguais, False caso contrário.
    Raises: 
        Não tem.
    """
    #Obtenção de colunas e linhas das interseções
    col1 = obtem_col(i1)
    lin1 = obtem_lin(i1)
    col2 = obtem_col(i2)
    lin2 = obtem_lin(i2)
    #Comparação das colunas e linhas
    if col1 != col2 or lin1!=lin2:
        return False
    return True

#Transformador

def intersecao_para_str(i):
    """ Transforma uma interseção numa string que a representa.
    Args:
        intersecao: (col,lin) --> tuplo com letra (A a S) e número (1 a 19).
    Returns:
        str: string com letra correspondente à coluna de i e número correspondente à linha da mesma.
    Raises: 
        Não tem.
    """
    #f string para facilitar a representação de uma interseção em string:
    return f"{obtem_col(i)}"+f"{obtem_lin(i)}"
    
def str_para_intersecao(s):
    """ Transforma uma string numa interseção.
    Args:
        str: String com letra correspondente à coluna de i e número correspondente à linha da mesma.
    Returns:
        intersecao: (col,lin) --> tuplo com letra (A a S) e número (1 a 19).
    Raises: 
        Não tem.
    """
    #Verifica se é uma string
    if type(s)==str: 
        #Se tem tamanho dois então é uma letra e um número de 1 a 9
        if len(s)==2 and "A"<=s[0]<="S" and s[1] in "123456789":
            return cria_intersecao(s[0], int(s[1]))
        #Se tem tamanho três é uma letra, o número um e um número de 0 a 9
        if len(s)==3 and "A"<=s[0]<="S" and s[1]=="1" and s[2] in "0123456789":
            return cria_intersecao(s[0], int(s[1])*10+int(s[2]))
            
#Alto Nível

def obtem_intersecoes_adjacentes(i, l):
    """ Obtém as interseções adjacentes (esquerda, direita, baixo, cima - caso existam) a uma dada interseção.
    Args:
        i (intersecao): Interseção à qual se querem obter as interseções adjacentes.
        l (intersecao): A última interseção do tabuleiro (canto superior direito), usada para determinar os limites.
    Returns:
        tuple: Um tuplo com as interseções válidas pela ordem de leitura estabelecida.
    Raises: 
        Não tem.
    """    
    #Obtenção de colunas e linhas 
    col_i, lin_i = obtem_col(i), obtem_lin(i)
    col_l, lin_l = obtem_col(l), obtem_lin(l)
    adjacentes = [] #Lista para armazenar adjacentes

    if "A" <= col_i <= col_l and 1 <= lin_i <= lin_l: #Está dentro dos limites do tabuleiro

        if col_i > "A": #Não está no lado esquerdo, logo tem interseção da esquerda:
            adjacentes.append(cria_intersecao(chr(ord(col_i) - 1), lin_i))

        if col_i < col_l: #Não está no lado direito, logo tem interseção da direita:
            adjacentes.append(cria_intersecao(chr(ord(col_i) + 1), lin_i))

        if lin_i > 1: #Não está na parte de baixo, logo tem interseção de baixo:
            adjacentes.append(cria_intersecao(col_i, lin_i - 1))

        if lin_i < lin_l: #Não está na parte de cima, logo tem interseção de cima:
            adjacentes.append(cria_intersecao(col_i, lin_i + 1))

    #Conversão da lista num tuplo com as interseções ordenadas
    return ordena_intersecoes(tuple(adjacentes))

def ordena_intersecoes(t):
    """ Ordena um tuplo de interseções de acordo com a ordem de leitura estabelecida (esquerda para a direita, baixo para cima).
    Args:
        t (tuple): tuplo de interseções que se quer ordenar.
    Returns:
        tuple: Um tuplo com as interseções pela ordem de leitura estabelecida.
    Raises: 
        Não tem.
    """
    #Ordena as interseções: primeiro por linha e, em caso de empate, por coluna.
    intersecoes_ordenadas = sorted(t, key=lambda intersecao: (obtem_lin(intersecao), obtem_col(intersecao)))

    #Conversão da lista ordenada num tuplo
    return tuple(intersecoes_ordenadas)

"""
TAD pedra (Assinatura)
Representação interna das pedras -> strings

Construtor:

---> cria_pedra_branca: {} -> str (pedra)
cria_pedra_branca() devolve uma pedra que pertence ao jogador branco, "O".

---> cria_pedra_preta: {} -> str (pedra)
cria_pedra_preta() devolve uma pedra que pertence ao jogador preto, "X".

---> cria_pedra_neutra: {} -> str (pedra)
cria_pedra_neutra() devolve uma pedra neutra, ".".


Reconhecedores:

---> eh_pedra: universal -> {True, False}
eh_pedra(arg) devolve True se arg é um TAD pedra e False caso contrário.

---> eh_pedra_branca: str (pedra) -> {True, False}
eh_pedra_branca(p) devolve True caso p seja uma pedra branca e False caso contrário.

---> eh_pedra_preta: str (pedra) -> {True, False}
eh_pedra_preta(p) devolve True caso p seja uma pedra preta e False caso contrário.


Teste:

---> pedras_iguais str (pedra) x str (pedra) -> {True, False}
pedras_iguais(p1, p2) devolve True caso p1 e p2 sejam pedras iguais e False caso contrário.


Transformador:

---> pedra_para_str: str (pedra) -> str (pedra)
pedra_para_str(p) transforma uma pedra em string numa pedra em string.


Alto Nível:

---> eh_pedra_jogador: pedra -> {True, False}
eh_pedra_jogador(p) devolve True se p é uma pedra de um jogador e False caso contrário.

"""

#TAD pedra

#Construtores
def cria_pedra_branca():
    """ Cria uma pedra de cor branca.
    Args:
        Não tem.
    Returns:
        str: "O" --> representação da pedra branca em string.
    Raises:
        Não tem.
    """
    return "O"

def cria_pedra_preta():
    """ Cria uma pedra de cor preta.
    Args:
        Não tem.
    Returns:
        str: "X" --> representação da pedra preta em string.
    Raises:
        Não tem.
    """
    return "X"

def cria_pedra_neutra():
    """ Cria uma pedra neutra.
    Args:
        Não tem.
    Returns:
        str: "." --> representação da pedra neutra em string.
    Raises:
        Não tem.
    """
    return "." 

#Reconhecededores

def eh_pedra(arg):
    """ Verifica se arg corresponde a um TAD pedra.
    Args:
        arg: argumento que se quer verificar (universal).
    Returns:
        bool: True se arg é um TAD pedra e False caso contrário.
    Raises: 
        Não tem.
    """
    #Verificações num só return
    return arg == cria_pedra_branca() or arg == cria_pedra_preta() or arg == cria_pedra_neutra()

def eh_pedra_branca(p): 
    """ Verifica se p corresponde a uma pedra de cor branca.
    Args:
        p (pedra) --> pedra que se deseja verificar.
    Returns:
        bool: True se p é uma pedra de cor branca e False caso contrário.
    Raises: 
        Não tem.
    """
    #Verificação num só return      
    return p == cria_pedra_branca()

def eh_pedra_preta(p):
    """ Verifica se p corresponde a uma pedra de cor preta.
    Args:
        p: pedra (str) --> pedra que se deseja verificar.
    Returns:
        bool: True se p é uma pedra de cor preta e False caso contrário.
    Raises: 
        Não tem.
    """       
    #Verificação num só return 
    return p == cria_pedra_preta()

#Testes

def pedras_iguais(p1, p2):
    """ Verifica se p1 e p2 são duas pedras do mesmo tipo (branco, preto, neutro).
    Args:
        p1: pedra (str) --> pedra que se deseja comparar.
        p2: pedra (str) --> pedra que se deseja comparar.
    Returns:
        bool: True se p1 e p2 são igais e False caso contrário.
    Raises: 
        Não tem.
    """
    #Verificações num só return
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2

#Transformador
def pedra_para_str(p):
    """ Converte uma pedra numa string que a representa.
    Args:
        p: pedra (str) --> pedra que se deseja transformar. 
    Returns:
        str: "O" para pedras brancas, "X" para pedras pretas e "." para pedras neutras.
    Raises:
        Não tem.

    """    
    if eh_pedra_branca(p):
        return cria_pedra_branca() #Representação de pedra branca em string
    
    elif eh_pedra_preta(p):
        return cria_pedra_preta() #Representação de pedra preta em string
    
    return cria_pedra_neutra() #Representação de pedra vazia em string
    
#Alto Nível

def eh_pedra_jogador(p):
    """ Verifica se p é uma pedra de um jogador branco ou preto.
    Args:
        p: pedra (str) --> pedra que se deseja verificar.
    Returns:
        bool: True se p é de um jogador branco ou preto, False caso contrário.
    Raises: 
        Não tem.
    """
    #Verifica se a pedra é preta ou branca (pertence a um jogador)
    return eh_pedra_branca(p) or eh_pedra_preta(p)
    
"""
TAD goban (Assinatura)
Representação interna do goban -> lista de listas

Construtores:

---> cria_goban_vazio: int -> goban (list)
cria_goban_vazio(n) recebe 9, 13 ou 19 e devolve uma tabuleiro de Go vazio (Lista de listas com pedras neutras). 

---> cria_goban: int x tuple x tuple -> goban (list)
cria_goban(n, ib, ip) recebe 9, 13 ou 19 e dois tuplos com interseções dos jogadores branco e preto (ib e ip) 
e devolve o goban com as interseções dos tuplos preenchidas por pedras brancas e pretas, respetivamente.

---> cria_copia_goban: goban (list) -> goban (list)
cria_copia_goban(t) recebe um goban e devolve a sua cópia profunda.


Seletores:

---> obtem_ultima_intersecao: goban (list) -> intersecao 
obtem_ultima_intersecao(g) recebe um goban e devolve a sua interseção superior direita.

---> obtem_pedra: goban (list) x intersecao -> pedra
obtem_pedra(g, i) recebe um goban e uma interseção e devolve a pedra dessa interseção.

---> obtem_cadeia: goban (list) x intersecao -> tuple
obtem_cadeia(g, i) recebe um goban e uma interseção e devolve a cadeia na qual a pedra dessa interseção está incluída.


Modificadores:

---> coloca_pedra: goban (list) x intersecao x pedra -> goban (list)
coloca_pedra(g, i, p) recebe um goban, uma interseção e uma pedra e devolve o mesmo goban com a pedra na interseção recebida.

---> remove_pedra: goban (list) x intersecao -> goban (list)
remove_pedra(g, i) remove a pedra (de jogador) da interseção recebida, devolvendo o goban sem essa pedra.

---> remove_cadeia: goban (list) x tuple -> goban (list)
remove_cadeia(g, t) remove do goban as pedras das interseções recebidas no tuplo.


Reconhecedores:

---> eh_goban: universal -> {True, False}
eh_goban(arg) devolve True se arg é um TAD goban e False caso contrário.

---> eh_intersecao_valida: goban (list) x interseção -> {True, False}
eh_intersecao_valida(g, i) devolve True se a interseção é válida para o goban recebido e False caso contrário.


Testes:

---> gobans_iguais: goban (list) x goban (list) -> {True, False}
gobans_iguais(g1, g2) devolve True caso os gobans recebidos sejam iguais e False caso contrário.

---> goban_para_str: goban (list) -> str
goban_para_str(g) devolve o goban na sua representação em string.


Alto Nível

---> obtem_territorios: goban -> tuple
obtem_territorios(g) devolve o tuplo formado pelos tuplos com as interseções de cada território do goban.

---> obtem_adjacentes_diferentes: goban x tuple -> tuple
obtem_adjacentes_diferentes(g, t) devolve as liberdades de uma cadeia de pedras ou a fronteira de um território,
consoante o tuplo contém interseções correspondentes a pedras de jogador ou a pedras neutras.

---> jogada: goban x intersecao x pedra -> goban
jogada(g, i, p) realiza uma jogada (colocação de uma pedra e, se for possível, remoção de pedras do adversário),
devolvendo o goban após a jogada ser concluída.

---> obtem_pedras_jogadores: goban -> tuple
obtem_pedras_jogadores(g) devolve um tuplo com o nº de pedras do jogador branco e nº de pedras do jogador preto.

"""
#TAD goban

#Construtores

def cria_goban_vazio(n):
    """ Cria o goban vazio com o tamanho n (9,13,19).
    Args:
        n: int --> n in (9,13,19).
    Returns:
        goban: list --> lista que representa o goban vazio.
    Raises: 
        ValueError: argumento inválido.
    """
    #Verificação do argumento (levanta erro)
    if type(n) != int or n not in (9,13,19): # ---> 9,13,19 são os possíveis tamanhos de um tabuleiro
        raise ValueError('cria_goban_vazio: argumento invalido')
    
    #Linha com pedras neutras:
    linha_vazia = [cria_pedra_neutra()] * n
    #Goban representado por uma lista de linhas com pedras neutras:
    goban = [list(linha_vazia) for coluna in range(n)]

    return goban

def cria_goban(n, ib, ip):
    """ Cria o goban com o tamanho n e com as interseções em ib preenchidas \
        com pedras brancas e as interseções em ip com pedras pretas.
    Args:
        n: int --> n in (9,13,19).
        ib: tuple --> tuplo de interseções com pedras brancas.
        ip: tuple --> tuplo de interseções com pedras pretas. 
    Returns:
        goban: list --> lista que representa o goban com as interseções em ib\
        preenchidas com pedras brancas e as interseções de ip com pedras pretas.
    Raises: 
        ValueError: argumentos inválidos.
    """
    #Verificação de n:
    try:
        cria_goban_vazio(n)
    except ValueError:
        raise ValueError('cria_goban: argumentos invalidos')
    
    #Verificação de ib e ip como tuplos:
    if type(ib)!= tuple:
        raise ValueError('cria_goban: argumentos invalidos')
    if type(ip)!=tuple:
        raise ValueError('cria_goban: argumentos invalidos')
    
    #Criação de um goban vazio:
    goban = cria_goban_vazio(n)
    
    #Verificação da validade das interseções de ib e ip:
    for intersecao in ib:
        if not eh_intersecao_valida(goban, intersecao):
            raise ValueError('cria_goban: argumentos invalidos')
        if intersecao in ip:
            raise ValueError('cria_goban: argumentos invalidos')
        
    if len(set(ib)) != len(ib):
        raise ValueError('cria_goban: argumentos invalidos')
    
    for intersecao in ip:
        if not eh_intersecao_valida(goban, intersecao):
            raise ValueError('cria_goban: argumentos invalidos')
        if intersecao in ib:
            raise ValueError('cria_goban: argumentos invalidos')
        
    if len(set(ip)) != len(ip):
        raise ValueError('cria_goban: argumentos invalidos')
        
    #Colocação das pedras brancas nas respetivas interseções
    for intersecao in ib:
        coluna, linha = ord(obtem_col(intersecao)) - ord("A"), obtem_lin(intersecao) - 1
        goban[coluna][linha] = cria_pedra_branca()

    #Colocação das pedras pretas nas respetivas interseções
    for intersecao in ip:
        coluna, linha = ord(obtem_col(intersecao)) - ord("A"), obtem_lin(intersecao) - 1
        goban[coluna][linha] = cria_pedra_preta()

    return goban

def cria_copia_goban(t): 
    """ Cria uma cópia profunda de um goban.
    Args:
        t: goban (list) --> goban que se deseja copiar.
    Returns:
        goban (list) --> cópia profunda do goban t.
    Raises: 
        Não tem.
    """
    
    #Obtém tamanho do goban original
    n = len(t)

    #Cria novo goban vazio
    copia_goban = cria_goban_vazio(n) 

    #Copia as interseções do goban original para a cópia
    for coluna in range(n):
        for linha in range(n):
            copia_goban[coluna][linha] = t[coluna][linha]

    return copia_goban

#Seletores

def obtem_ultima_intersecao(g):
    """ Obtém a interseção do canto superior direito do goban g.
    Args:
        g: goban (list) --> goban ao qual se deseja obter a última interseção.
    Returns:
        tuple: interseção (col,lin) --> última interseção do goban g.
    Raises: 
        Não tem.
    """
    tamanho = len(g) # ---> igual à linha
    return cria_intersecao(chr(tamanho + ord("A") - 1) , tamanho) # ---> interseção com letra e inteiro

def obtem_pedra(g, i):
    """ Obtém a pedra na interseção i do goban g.
    Args:
        g: goban (list) --> goban escolhido.
        i: interseção (col,lin) --> interseção à qual se deseja obter a pedra.
    Returns:
        str: "O" para pedras brancas, "X" para pedras pretas e "." para pedras neutras.
    Raises: 
        Não tem.
    """
    #Obtenção da coluna e da linha no goban correspondentes à interseção 
    coluna,linha = ord(obtem_col(i)) - ord("A"), obtem_lin(i) - 1

    #Caso seja pedra branca
    if eh_pedra_branca(g[coluna][linha]):
        return cria_pedra_branca()  
        
    #Caso seja pedra preta
    if eh_pedra_preta(g[coluna][linha]):
        return cria_pedra_preta()   
        
    #Caso seja pedra neutra
    if not eh_pedra_jogador(g[coluna][linha]):
        return cria_pedra_neutra()   

def obtem_cadeia(g, i):
    """ Obtém a cadeia que contém a interseção i. Cadeia é o conjunto de uma ou mais interseções 
        ocupadas por pedras do mesmo tipo que estão todas conetadas entre si e que não estão conetadas 
        a nenhuma outra pedra do mesmo tipo.
    Args:
        g: goban (list) --> goban escolhido.
        i: interseção (col,lin) --> interseção pertencente à cadeia que se deseja obter.
    Returns:
        tuple: um tuplo com as intersções que formam a cadeia com a inteseção i.
        Só pode conter interseções de um tipo (brancas, pretas, neutras).
    Raises: 
        Não tem.
    """
    
    #Obtenção da cor da pedra (e, consequentemente, da cadeia):
    cor_cadeia = obtem_pedra(g, i)
    #Inicialização da lista cadeia:
    cadeia = [i]
    #Inicialização da lista de visitados:
    visitados = [i]

    while cadeia: # ---> Enquanto a lista "cadeia" não estiver vazia

        #Remoção da primeira interseção da lista cadeia:
        intersecao_atual = cadeia.pop(0)

        #Obtenção das adjacentes à interseção atual:
        adjacentes = obtem_intersecoes_adjacentes(intersecao_atual, obtem_ultima_intersecao(g))

        for adjacente in adjacentes: # ---> Percorre as interseções adjacentes

            #Verifica se a interseção adjacente não foi visitada, se é válida e da mesma cor que a cadeia:
            if adjacente not in visitados and eh_intersecao_valida(g, adjacente) and pedras_iguais(obtem_pedra(g, adjacente),cor_cadeia):
                
                #Adiciona a adjacente à lista "cadeia" e à lista "visitados"
                cadeia.append(adjacente)
                visitados.append(adjacente)
            
    #Return com tuplo das interseções da cadeia ordenadas
    return ordena_intersecoes(tuple(visitados))


#Modificadores

def coloca_pedra(g, i, p):
    """ Coloca uma pedra p, de um jogador, numa interseção i de um goban g.
    Args:
        g: goban (list) --> goban escolhido.
        i: intersecao (col,lin) --> interseção à qual se quer adicionar a pedra.
        p: pedra (str) --> "O" peara pedra branca e "X" para pedra preta.
    Returns:
        goban: goban modificado com a pedra p na interseção i.
    Raises:
        Não tem. 
    """
    
    #Obtenção da coluna e da linha no goban correspondentes à interseção:
    coluna, linha = ord(obtem_col(i)) - ord("A"), obtem_lin(i) - 1

    #Colocação da pedra branca na respetiva interseção do tabuleiro:
    if eh_pedra_branca(p):
        g[coluna][linha] = cria_pedra_branca()

    #Colocação da pedra preta na respetiva interseção do tabuleiro:
    else:
        g[coluna][linha] = cria_pedra_preta()

    return g

def remove_pedra(g, i):
    """ Remove a pedra da interseção i do goban g, substituindo-a por uma pedra neutra.
    Args:
        g: goban (list) --> goban escolhido.
        i: intersecao (col,lin) --> interseção que se deseja remover.
    Returns:
        goban: goban sem a pedra que anteriormente estava em i.
    Raises: 
        Não tem.
    """
    
    #Obtenção da coluna e da linha no goban correspondentes à interseção:
    coluna, linha = ord(obtem_col(i)) - ord("A"), obtem_lin(i) - 1

    #Colocação da pedra neutra na respetiva interseção do tabuleiro:
    g[coluna][linha] = cria_pedra_neutra() # ---> Corresponde a remover uma pedra com cor

    return g

def remove_cadeia(g, t):
    """ Remove as pedras das interseções pertenentes ao tuplo t.
    Args:
        g: goban (list) --> goban escolhido.
        t: tuplo (tuple) --> tuplo de interseções.
    Returns:
        goban: goban sem as pedras das interseções que estavam em t.
    Raises: 
        Não tem.
    """
    for intersecao in t: # ---> Percorre as interseções de t

        #Obtenção da coluna e da linha no goban correspondentes à interseção:
        coluna, linha = ord(obtem_col(intersecao)) - ord("A"), obtem_lin(intersecao) - 1

        #Remoção da interseção (corresponde à sua substituição por uma pedra neutra)
        g[coluna][linha] = cria_pedra_neutra()

    return g

#Reconhecedores

def eh_goban(arg):
    """ Verifica se arg é um TAD goban ou não.
    Args:
        arg: argumento que se quer verificar.
    Returns:
        bool: True se arg é um goban e False caso contrário.
    Raises: 
        Não tem.
    """
    #Verifica se é uma lista
    if type(arg)!= list:
        return False
    
    #Verificação do tamanho do goban
    if len(arg) not in (9,13,19):
        return False
    
    #Obtenção do tamanho de uma coluna (para comparação)
    tamanho_coluna = len(arg)
    #Tabuleiro é quadrado!!
    if tamanho_coluna not in (9,13,19):
        return False
    for coluna in arg:
        if type(coluna) != list: #Verifica se cada linha é uma lista
            return False
        if len(coluna)!= tamanho_coluna:
            return False
        for intersecao in coluna: # ---> Verifica se as interseções são válidas (pedras de todos os tipos)
            if not eh_pedra(intersecao):
                return False
            
    #Se é goban válido devolve True
    return True    

def eh_intersecao_valida(g, i):
    """ Verifica se i é uma interseção válida para o goban g.
    Args:
        g: goban (list) --> goban escolhido.
        i: intersecao (col,lin) --> interseção que se deseja verificar.
    Returns:
        bool: True se i pertene ao goban g e False caso contrário.
    Raises: 
        Não tem.
    """
    #Verificação ---> é goban:
    if not eh_goban(g):
        return False
    
    #Verificação ---> é interseção:
    if not eh_intersecao(i):
        return False
    
    #Verificação ---> interseção dentro dos limites do tabuleiro:
    tamanho = len(g)
    coluna, linha = ord(obtem_col(i)) - ord("A"), obtem_lin(i) - 1
    if 0 <= linha < tamanho and 0 <= coluna < tamanho:
        return True

    return False

#Teste
def gobans_iguais(g1, g2):
    """ Compara dois gobans.
    Args:
        g1: goban (list) --> goban que se quer comparar.
        g2: goban (list) --> goban que se quer comparar.
    Returns:
        bool: True se g1 é igual a g2 e False caso contrário.
    Raises: 
        Não tem.
    """
    #Verificação ---> são gobans?
    if not(eh_goban(g1) and eh_goban(g2)):
        return False
    
    #Verificação ---> Têm tamanhos diferentes?  
    if len(g1) != len(g2) or len(g1[0]) != len(g2[0]):
        return False
    
    #Verificação ---> As interseções são todas iguais?
    for coluna in range(len(g1)):
        for linha in range(len(g1)):
            if g1[coluna][linha] != g2[coluna][linha]:
                return False 
               
    return True

def goban_para_str(g):
    """ Transforma um goban g na sua representação em string. 
    Args:
        g: goban (list) --> goban que se quer transformar.
    Returns:
        str: string que representa o goban.    
    Raises: 
        ValueError: argumento inválido.
    """
    #Verificação:
    if not eh_goban(g):
        raise ValueError('goban_para_str: argumento invalido')
    
    #Obtenção de tamanhos:
    numero_linhas = len(g)
    numero_colunas = numero_linhas

    #Inicialização de uma lista para armazenar cada linha gerada
    goban_str = []

    # Parte de cima (= Parte de baixo) ---> Letras
    letras = "   " + " ".join(chr(ord('A') + coluna) for coluna in range(numero_colunas))
    goban_str.append(letras)

    # Parte Intermédia
    for linha in range(numero_linhas - 1, -1, -1):
        #Números da esquerda:
        linha_str = "".join(f"{str(linha + 1)}" if (linha + 1) >= 10 else f" {str(linha + 1)}")
        #Interseções:
        linha_str += "".join(" X" if g[coluna][linha] == 'X' else " O" if g[coluna][linha] == 'O' else " ." for coluna in range(numero_colunas))
        #Números da direita
        linha_str += "".join(f" {str(linha + 1)}" if (linha + 1) >= 10 else f"  {str(linha + 1)}")
        goban_str.append(linha_str)

    # Parte de baixo ---> Letras
    goban_str.append(letras)

    #Return como string única (une linhas com quebra de linhas):
    return "\n".join(goban_str)


#Alto Nível
    
def obtem_territorios(g):
    """ Obtém todos os territórios do goban g. Um território é o conjunto maximal
        de uma ou mais interseções livres que estão todas conetadas entre si e que
        não estão conetadas a nenhuma outra interseção livre.
    Args:
        g: goban --> goban escolhido.
    Returns:
        tuple: Um tuplo de territórios, onde cada território é um tuplo de interseções.
    Raises: 
        Não tem.
    """
    #Inicialização de uma lista para armazenar as cadeias vazias:
    cadeias_vazios = []
    tamanho = obtem_lin(obtem_ultima_intersecao(g)) #Em vez de usar len(g) ---> Abstração

    #Iteração sobre cada interseção:
    for coluna in range(tamanho):
        for linha in range(tamanho):

            #Interseção atual:
            intersecao = cria_intersecao(chr(coluna + ord('A')), linha + 1)

            #Se interseção atual é vazia e se não faz parte de cadeias já identificadas:
            if not eh_pedra_jogador(obtem_pedra(g, intersecao)) and not any(intersecao in cadeia for cadeia in cadeias_vazios):

                #Adiciona cadeia da interseção atual à lista cadeia_vazios:
                cadeia_v = tuple(obtem_cadeia(g, intersecao))
                cadeias_vazios.append(cadeia_v)

    #Ordena os territórios de acordo com a primeira interseção:       
    cadeias_vazios.sort(key=lambda cadeia: (obtem_lin(cadeia[0]), obtem_col(cadeia[0]))) 

    #Return de tuplo com cada subtuplo a corresponder a um território:    
    return tuple(cadeia for cadeia in cadeias_vazios)
    
def obtem_adjacentes_diferentes(g, t):
    """ Obtém as liberdades de uma cadeia de pedras, se t tiver interseções com pedras de jogador ou
        a fronteira de um território, se t tiver interseções livres.

    Args:
        g: goban --> goban escolhido.
        t: tuple --> tuplo com interseções válidas para g.
    Returns:
        tuple: tuplo ordenado formado por liberdades de uma cadeia de pedras ou pela fronteira de um território

    Raises: 
        Não tem.
    """
    adjacentes_diferentes = []

    for intersecao in t:
        #Parte da fronteira ---> t tem pedras neutras

        if not eh_pedra_jogador(obtem_pedra(g, intersecao)):

            #Obtem adjacentes à pedra neutra atual:
            intersecoes_adjacentes = obtem_intersecoes_adjacentes(intersecao, obtem_ultima_intersecao(g))
            
            for adjacente in intersecoes_adjacentes: # ---> Percorre adjacentes

                #Verifica se a adjacente é pedra de um jogador e se não está na lista "adjacentes_diferentes":
                if eh_pedra_jogador(obtem_pedra(g, adjacente)) and adjacente not in adjacentes_diferentes:
                    adjacentes_diferentes.append(adjacente) # ---> Adiciona à lista
        
        #Parte das liberdades ---> t tem pedras não neutras
        
        if eh_pedra_jogador(obtem_pedra(g, intersecao)):
            
            #Obtém adjacentes à pedra atual:
            intersecoes_adjacentes = obtem_intersecoes_adjacentes(intersecao, obtem_ultima_intersecao(g))
            
            for adjacente in intersecoes_adjacentes: # ---> Percorre adjacentes
                
                #Verifica se a adjacente é pedra neutra e se não está na lista "adjacentes_diferentes":
                if not eh_pedra_jogador(obtem_pedra(g,adjacente)) and adjacente not in adjacentes_diferentes:
                    adjacentes_diferentes.append(adjacente) # ---> Adiciona à lista

    #Transforma a lista num tuplo e ordena as interseções da lista:
    adjacentes_diferentes = ordena_intersecoes(tuple(adjacentes_diferentes))
    return adjacentes_diferentes

def jogada(g, i, p):
    """ Realiza uma jogada num goban g: 
        1) colocação da pedra p na interseção i; 
        2) remoção das pedras do oponente sem liberdades.
    Args:
        g: goban --> goban escolhido.
        i: intersecao --> interseção na qual se deseja colocar a pedra p.
        p: pedra --> a pedra a ser colocada.
    Returns:
        goban: goban alterado, com a pedra p na interseção i e sem as interseções adversárias sem liberdades.
    Raises: 
        Não tem.
    """
    #Coloca a pedra p na interseção i:
    coloca_pedra(g, i, p)
    #Obtem adjacentes a i:
    adjacentes = obtem_intersecoes_adjacentes(i, obtem_ultima_intersecao(g))
    
    for adjacente in adjacentes: # ---> Percorre adjacentes
        
        #Se adjacente é pedra diferente de p:
        if not pedras_iguais(obtem_pedra(g, adjacente), p): 
            
            #Obtém cadeia da adjacente:
            cadeia = obtem_cadeia(g, adjacente)
            
            #Obtém liberdade da adjacente:
            liberdades = obtem_adjacentes_diferentes(g, cadeia)
            
            #Se não tem liberdades, remove a cadeia
            if not liberdades:
                remove_cadeia(g, cadeia)

    return g

def obtem_pedras_jogadores(g):
    """ Obtém o número de pedras de cada jogador no goban g.
    Args:
        g: goban --> goban escolhido.
    Returns:
        tuple: tuplo com número de pedras brancas e número de pedras pretas.
    Raises: 
        Não tem.
    """
    #Inicialização dos contadores:
    pedras_brancas = 0
    pedras_pretas = 0

    #Obtenção do tamanho da tabuleiro:
    tamanho = obtem_lin(obtem_ultima_intersecao(g))
    
    #Percorre todas as interseções do tabuleiro:
    for coluna in range(tamanho): 
        for linha in range(tamanho):

            #Obter a pedra da interseção atual
            intersecao = cria_intersecao(chr(coluna + ord('A')), linha + 1)
            pedra = obtem_pedra(g, intersecao)

            #Se a pedra é branca:
            if eh_pedra_branca(pedra):
                pedras_brancas += 1

            #Se a pedra é preta
            elif eh_pedra_preta(pedra):
                pedras_pretas += 1

    #Return de tuplo ---> (Nº de pedras brancas, Nº de pedras pretas)
    return pedras_brancas, pedras_pretas

"""
Funções Adicionais (Assinatura)

---> calcula_pontos: goban -> tuple
calcula_pontos(g) recebe um goban e devolve o tuplo com o nº de pontos do jogador preto e do jogador branco.
Nota -> Pontuação = Nº Pedras + Nº interseções de territórios (de cada jogador).

---> eh_jogada_legal: goban x intersecao x pedra x goban -> {True, False}
eh_jogada_legal(g, i, p, l) devolve True se uma jogada é legal e False caso contrário
Nota -> Jogadas ilegais: ko, suicídio, sobreposição de peças, interseções inválidas.

---> turno_jogador: goban x pedra x goban -> {True, False}
turno_jogador(g, p, l) devolve False se o jogador passar e True caso contrário.

---> go: inteiro x tuplo x tuplo -> {True, False}
go(n, tb, tp) recebe um inteiro (9, 13 ou 19) e dois tuplos com as interseções em string dos jogadores branco e preto,
potencialmente vazios. Permite a realização de um jogo de Go e devolve True se o jogador branco ganhar ou se empatar,
e False caso contrário.

"""

#Funções Adicionais

def calcula_pontos(g):
    """ Calcula a pontuação de cada jogador num goban. A pontuação de um jogador é dada 
        pela soma do número de pedras que lhe correspondem com o número de interseções 
        dos seus territórios.
    Args:
        g: goban (list) --> goban escolhido.
    Returns:
        tuple: tuplo com os pontos dos dois jogadores de Go.
    Raises: 
        Não tem.
    """
    #Nota: Pontuação = Nº Pedras + Nº interseções de territórios

    #Nº de pedras:
    pedras = obtem_pedras_jogadores(g)
    pontos_brancos, pontos_pretos = pedras
    
    #Começo do jogo:
    if pontos_brancos == 0 and pontos_pretos == 0:
        return 0, 0
    

    #Identificação do dono do território:


    todos_territorios = obtem_territorios(g) # ---> Interseções vazias

    #Inicialização da lista que armazena territórios:
    territorios = []

    for cadeia in todos_territorios: # ---> Percorre cadeias vazias da lista "todos_territorios"

        #Verificação da conectividade entre as interseções da cadeia:

        #Suposição: Território não conectado a pedras pretas nem brancas:
        conectado_a_branca = False
        conectado_a_preta = False

        for intersecao in cadeia: # ---> Percorre interseções da cadeia atual

           #Obtenção das adjacentes à interseção atual 
            adjacentes = obtem_intersecoes_adjacentes(intersecao, obtem_ultima_intersecao(g))

            for adjacente in adjacentes: # ---> Percorre adjacentes
                #Se adjacente é pedra branca
                if eh_pedra_branca(obtem_pedra(g, adjacente)):
                    conectado_a_branca = True
                #Se adjacente é pedra preta
                elif eh_pedra_preta(obtem_pedra(g, adjacente)):
                    conectado_a_preta = True
        
        #Verifica se o potencial território não está conectado a ambos os jogadores:
        if not (conectado_a_branca and conectado_a_preta):
            territorios.append(cadeia)
    
    #Ordena os territórios de acordo com a primeira interseção:       
    territorios.sort(key=lambda territorio: (obtem_lin(territorio[0]), obtem_col(territorio[0]))) 
    #Tuplo com cada subtuplo a corresponder a um território:    
    territorios = tuple(tuple(territorio) for territorio in territorios)
    
    for territorio in territorios:  #Itera nos subtuplos de interseções vazias correspondentes a um território
        
        #Obtém fronteira de um território (Para ver a que jogador este pertence)
        fronteiras = obtem_adjacentes_diferentes(g, territorio)
        
        #Se todas as pedras da fronteira forem pretas: 
        if all(eh_pedra_preta(obtem_pedra(g, fronteira)) for fronteira in fronteiras):
            pontos_pretos += len(territorio) # ---> Adição do nº de interseções do território preto
        #Caso contrário (são brancas)
        else:
            pontos_brancos += len(territorio) # ---> Adição do nº de interseções do território branco

    #Return de tuplo ---> (Pontos do jogador branco, Pontos do jogador preto) 
    return pontos_brancos, pontos_pretos

def eh_jogada_legal(g, i, p, l):
    """ Verifica se uma jogada é legal, ou seja, não se comete suícido, ko, sobreposição de peças
    e a interseção é válida.
    Args:
        g: goban (list) --> goban escolhido.
        i: intersecao (col,lin) --> interseção à qual se quer adicionar a pedra p.
        p: pedra (str) --> "O" se for pedra branca e "X" se for pedra preta.
        l: goban (list) --> goban correspondente ao estado que não se pode obter.
    Returns:
        bool: True se a jogada é legal e False caso contrário.
    Raises: 
        Não tem.
    """
    
    #Estado que não se pode obter (ko):   
    estado_inicial = [l]
    #Cópia de g, para não o alterar:
    copia_g = cria_copia_goban(g)

    #Validade da interseção
    if not eh_intersecao_valida(g,i):
        return False
    
    #Evitar sobreposição de peças:
    if eh_pedra_jogador(obtem_pedra(copia_g, i)):
        return False
    
    #Realização da jogada na cópia do goban
    jogada(copia_g, i, p) # ---> return da cópia do goban alterada 

    #Verificação (ko):
    if copia_g in estado_inicial:
        return False  
    
    #Verificação (Suicídio):
    if not obtem_adjacentes_diferentes(copia_g, obtem_cadeia(copia_g, i)):
        return False  
    
    #Return True se a jogada foi legal
    return True
        
def turno_jogador(g, p, l):
    """ Realiza o turno e um jogador.
    Args:
        g: goban (list) --> o Goban no qual a jogada será feita.
        p: pedra (str) --> a pedra do jogador ('O' para branco ou 'X' para preto).
        l: goban (list): --> estado do tabuleiro que não pode ser obtido.
    Returns:
        bool: False se o jogador passar, True caso contrário.
    Raises:
        Não tem. 
    """    
    while True: #Loop até jogador passar ou a jogada for válida

        #Input:
        entrada = input(f"Escreva uma intersecao ou 'P' para passar [{p}]:")
        
        #Se Passar, retorna False:
        if entrada == 'P':
            return False
        
        #Converte entrada em interseção:
        intersecao = str_para_intersecao(entrada)

        #Se a interseção é válida e a jogada é legal, a jogada é realizada:
        if eh_jogada_legal(g, intersecao, p, l):
            jogada(g, intersecao, p)
            return True # ---> Turno de p concluído com sucesso
                 
def go(n, tb, tp):
    """
    Realiza um jogo de Go num goban de tamanho n com pedras brancas em interseções tb e pedras pretas em interseções tp.
    O jogo é executado alternando entre jogadores brancos e pretos até que ambos os jogadores passem consecutivamente.
    Args:
        n (int): O tamanho do Goban, que deve ser 9, 13 ou 19.
        tb (tuple): Um tuplo de interseções (representação externa) onde as pedras brancas são colocadas.
        tp (tuple): Um tuplo de interseções (representação externa) onde as pedras pretas são colocadas.
    Returns:
        bool: True se o jogador branco vencer ou for empate, False se o jogador preto vencer.
    Raises:
        ValueError: argumentos inválidos.
    """
    #Verificação superficial dos argumentos:
    if type(n) != int or type(tb) != tuple or type(tp)!= tuple:
        raise ValueError('go: argumentos invalidos')
    
    #Conversão da representação externa para interna:
    tb_intersecoes = tuple(str_para_intersecao(intersecao) for intersecao in tb)
    tp_intersecoes = tuple(str_para_intersecao(intersecao) for intersecao in tp)

    #Verifica se as interseções são válidas:        
    try:
        cria_goban(n, tb_intersecoes, tp_intersecoes)
    except ValueError:
        raise ValueError('go: argumentos invalidos')

    #Momento do Jogo:

    #Criação do goban já com as interseções desejadas (vazio ou não)
    g = cria_goban(n, tb_intersecoes, tp_intersecoes)

    #Representar pedras:
    p_branca = cria_pedra_branca() 
    p_preta = cria_pedra_preta()

    jogador_branco = False # ---> jogador preto começa
    consecutivo_passos = 0 # ---> "controla" o nº de passos consecutivos
    estados_antigos = [cria_copia_goban(g)] # ---> Para verificar a jogada inválida do estilo ko


    while consecutivo_passos < 2: # ---> loop até os dois jogadores darem Pass ("P")
        
        #Se for o jogador branco, jogador tem valor de p_branca
        #Se for jogador preto, jogador tem valor de p_preta
        jogador = p_branca if jogador_branco else p_preta
        pontos = calcula_pontos(g)
        
        #Print da pontuação e do goban em string    
        print(f"Branco (O) tem {pontos[0]} pontos\nPreto (X) tem {pontos[1]} pontos")
        print(goban_para_str(g))
        
        
        if turno_jogador(g, jogador, estados_antigos[0]): #Se o turno for concluido (True -> Não deram pass)
            consecutivo_passos = 0 # ---> Volta a "zerar" caso existam passos anteriores     
        else: # ---> Se deram pass
            consecutivo_passos += 1 # ---> incrementa um passo

        #Para manter a cópia go tabuleiro atualizada:
        estados_antigos.append(cria_copia_goban(g)) 
        if len(estados_antigos) > 2:
            estados_antigos.pop(0)     

        jogador_branco = not jogador_branco # ---> Muda de jogador

    #Pontuação (Em caso de empate ganha o branco):   
    pontos = calcula_pontos(g)        
    print(f"Branco (O) tem {pontos[0]} pontos\nPreto (X) tem {pontos[1]} pontos")
    print(goban_para_str(g))

    return  pontos[0] >= pontos[1]
