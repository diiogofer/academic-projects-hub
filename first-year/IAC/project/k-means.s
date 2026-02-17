# IAC 2023/2024 k-means
# 
# Grupo: 9
#
# Autores:
# 1111129, Bernardo Lopes
# 63484, Michael Maycock
# 1110306, Diogo Fernandes
#


# Variáveis em memória.
.data

# Número de pontos.
n:          .word   30
# Array de coordenadas de pontos.
points:     .word   16, 1, 17, 2, 18, 6, 20, 3, 21, 1, 17, 4, 21, 7, 16, 4, 21, 6, 19, 6, 4, 24, 6, 24, 8, 23, 6, 26, 6, 26, 6, 23, 8, 25, 7, 26, 7, 20, 4, 21, 4, 10, 2, 10, 3, 11, 2, 12, 4, 13, 4, 9, 4, 9, 3, 8, 0, 10, 4, 10
# Número de centroides.
k:          .word   3
# Array de coordenadas de centroides.
centroids:  .word   0, 0, 0, 0, 0, 0
# Número máximo de iterações do algoritmo k-means.
l:          .word   5

### Clusters Array #OPTIMIZATION
# Tem informação sobre cada centroide num ciclo de mainKMeans.
# Para cada centroide é guardado a soma das coordenadas dos pontos (X e Y separadamente) 
# e o número de pontos associados ao cluster desse centroide.
# Reduz tamanho do array de n (n points) para 3*k (k centroides) (mais pequeno). 
# Menos memória e menos iterações.
# Ex: para um centroid C é guardado: sum(X's), sum(Y's), n 
clusters:   .word   0, 0, 0, 0, 0, 0, 0, 0, 0

### Changed #OPTIMIZATION
# Variável de estado correspondente à alteração da posicão dos centroides.
# 0 = iteração de k-means não alterou posição dos centroides. 
# 1 = posição de centroide/s alterada/s na iteração (inicialmente: changed = 1).
# Interrompe o loop principal mais cedo se não houverem mudanças, evitando
# iterações desnecessárias e, por isso, melhorando o tempo de execução do algoritmo.
changed:    .word   1

### First #OPTIMIZATION
# Variável de estado correspondente ao número da iteração de k-means.
# 1 = primeira iteração de k-means. (inicialmente: first = 1).
# 0 = segunda ou mais iteração de k-means.
# Usada, por exemplo, para evitar a limpeza dos centroides na 1ª iteração do loop principal.
# Melhora a eficiência ao evitar operações desnecessárias
first:      .word   1

# Definicões de cores a usar no projeto.
# Cores dos pontos do cluster 0 1 2 etc.
colors:     .word   0xff0000 0x00ff00 0x0000ff
.equ        black   0
.equ        white   0xffffff

# Código 
.text

### main
# Limpa LED matrix por inteiro e chama mainKMeans l vezes ou até não haver
# alterações na posição dos centroides.
# Argumentos: nenhum
# Retorno: 0
main:
# Constantes
    la      s0  n
    lw      s0  0(s0)                       # s0 <- Valor de n
    la      s1  points                      # s1 <- Endereço de points 
    la      s2  k
    lw      s2  0(s2)                       # s2 <- Valor de k
    la      s3  centroids                   # s3 <- Endereço de centroids
    la      s4  l
    lw      s4  0(s4)                       # s4 <- Valor de l 
    la      s5  changed                     # s5 <- Endereço de changed
# cleanScreen call
    jal     cleanScreen                     # limpar LED Matrix (Matriz Branca)
# Verificar k == 1                          # Se k = 1 evita o loop
    addi t0 x0 1
    beq s2 t0 skip_mainLoop                 # k == 1 ? skip_mainLoop : continue
# initializeCentroids call
    mv      a0  s2                          # a0 <- s2 (valor de k)
    mv      a1  s3                          # a1 <- s3 (Endereço de centroids)
    jal     initializeCentroids             # inicializar centroides (Aleatório)
# mainKMeans Loop
mainLoop:
    lw      t0  0(s5)                       # t0 <- Valor de changed 
    beq     t0  x0  end_mainLoop            # changed == 0 ? end_mainLoop : continue
    ble     s4  x0  end_mainLoop            # l <= 0 ? end_mainLoop : continue
    sw      x0  0(s5)                       # Muda valor de changed para 0
    mv      a0  s0                          # a0 <- Valor de n (s0)
    mv      a1  s1                          # a1 <- Endereço de points (s1)
    mv      a2  s2                          # a2 <- Valor de k (s2)
    mv      a3  s3                          # a3 <- Endereço de centroids (s3)
    jal     mainKMeans                      # call mainKMeans
    addi    s4  s4   -1                     # Decrementa o valor de l
    j       mainLoop                        # Próxima iteração
skip_mainLoop:
    mv      a0  s0                          # a0 <- Valor de n (s0)
    mv      a1  s1                          # a1 <- Endereço de points (s1)
    mv      a2  s2                          # a2 <- Valor de k (s2)   
    mv      a3  s3                          # a3 <- Endereço de centroids (s3)
    jal     mainKMeans                      # call mainKMeans (k == 1)
# Fim do programa (chamada ao sistema)
end_mainLoop:
    li      a7  10
    ecall


### cleanScreen
# Limpa todos os LEDs (branco) da LED matrix.
# Argumentos: nenhum
# Retorno: nenhum
# OPTIMIZATION
# Este loop foi otimizado para percorrer a LED matrix e limpá-la
# através de acessos diretos aos endereços de cada posição da LED,
# em vez de recorrer à função printPoint, que tornaria esta função 
# mais lenta por ter de executar mais instruções
cleanScreen:
    li      t0  LED_MATRIX_0_BASE           # t0 <- Endereço de LED[0]
    li      t1  LED_MATRIX_0_SIZE           # Tamanho da LED Matrix [bytes]
    add     t1  t1  t0                      # t1 <- Endereço de LED[n]
    li      t2  white                       # t2 <- Cor branca
cleanScreenLoop:
    bge     t0  t1  end_CleanScreen         # While(LED[atual] <= LED[n])
    sw      t2  0(t0)                       # t0 (LED[atual]) <- Pintar de Branco
    addi    t0  t0  4                       # LED++
    j       cleanScreenLoop                 # Próxima iteração
end_CleanScreen:
    jr      ra                              # retorno


### initializeCentroids
# Inicializa os valores iniciais do vetor centroids.	
# Cada um dos k centroides é colocado num par de coordenadas escolhido de forma pseudoaleatória.
# O algoritmo que rege esta escolha é o LCG (Linear Congruential Generator) 
# que se baseia em: Xn+1 = (Xn * a + c) % m.
# Argumentos:
#   - a0: Valor de k
#   - a1: Endereço de centroids
# Retorno: nenhum

initializeCentroids:
    mv      t0  a0                          # Valor de k (a0)
    slli    t0  t0  3                       # x e y (8 bytes por centroide)
    mv      t1  a1                          # t1 <- Endereço de centroids (a1)                   
    add     t0  t1  t0                      # t0 <- Endereço do final de centroids

# Seed para função pesudo-aleatória:
# System call do Ripes -> Time_msec: Milisegundos desde 01/01/1970.
    addi    a7  x0  30                      # System call code para Time_msec
    ecall                                   # Retorna o valor em a0 (seed)
# Confirguração do LCG (Valores escolhidos a partir de documentação sobre LCG para m = 32)
    addi    t2  x0  13                      # (t2) <- a = 13
    addi    t3  x0  5                       # (t3) <- c = 5
    addi    t4  x0  32                      # (t4) <- m = 32
lcgLoop:
    bge     t1  t0  end_lcg                 # (Endereço atual >= Endereço final) -> end_lcg
    mul     a0  a0  t2                      # a0 =iteracoes Xn * a
    add     a0  a0  t3                      # a0 = a0 + c
# Valor de a0 negativo? 
    bge a0 x0 lcgRem                        # if (a0 >= 0) -> lcgRem
    sub a0 x0 a0                            # a0 < 0 -> a0 = abs(a0)
lcgRem:
    rem     a0  a0  t4                      # a0 = a0 % m 
    sw      a0  0(t1)                       # Guardar nova coordenada do centroide                   
    addi    t1  t1  4                       # Coordenada++
    j       lcgLoop                         # Próxima iteração
end_lcg:   
    jr ra


### mainKMeans
# Executa 1 instância do algoritmo k-means, ou seja:
#   -> limpa centroides da LED Matrix
#   -> faz update à LED matrix com novas cores para points e coordenadas para centroides
# Argumentos:
#   - a0: Valor de n
#   - a1: Endereço de points
#   - a2: Valor de k
#   - a3: Endereço de centroids
# Retorno: nenhum

mainKMeans:
# Stack Push
    addi    sp  sp  -24
    sw      ra  0(sp)
    sw      s0  4(sp)
    sw      s1  8(sp)
    sw      s2  12(sp)
    sw      s3  16(sp)
    sw      s4  20(sp) 
# Argumentos
    mv      s0  a0                          # s0 <- Valor de n (a0)
    mv      s1  a1                          # s1 <- Endereço de points (a1)
    mv      s2  a2                          # s2 <- Valor de k (a2)
    mv      s3  a3                          # s3 <- Endereço de centroids (a3)
    la      s4 clusters                     # s4 <- Endereço de clusters
# cleanCentroids
    la      t0  first                       # t0 <- Endereço de first
    lw      t1  0(t0)                       # t1 <- Valor de first
    sw      x0  0(t0)                       # Set first = 0 (em memória)
    bne     t1  x0  skip_cleanCentroids     # if first (t1) == 1 -> skip_cleanCentroids
    mv      a0  s2                          # a0 <- Valor de k (s2)
    mv      a1  s3                          # a1 <- Endereço de centroids (s3)
    jal     cleanCentroids                  # limpa centroides da LED Matrix
skip_cleanCentroids:  
# resetClusters call (garante clusters[] = {0} para cálculo de centroides na nova iteração).
    mv      a0  s2                          # a0 <- Valor de k (s2)
    mv      a1  s4                          # a1 <- Endereço de clusters (s4)
    jal     resetClusters                   # resetClusters call (clusters = {0})     
# printClusters call
    mv      a0  s0                          # a0 <- Valor de n (s0)
    mv      a1  s1                          # a1 <- Endereço de points (s1)
    mv      a2  s2                          # a2 <- Valor de k (s2)
    mv      a3  s3                          # a3 <- Endereço de centroids (s3)
    jal     printClusters                   
# calculateCentroids call
    mv      a0  s2                          # a0 <- Valor de k (s2)
    mv      a1  s3                          # a1 <- Endereço de centroids (s3)
    mv      a2  s4                          # a2 <- endereço de clusters (s4)
    jal     calculateCentroids
# printCentroids call
    mv      a0  s2                          # a0 <- Valor de k (s2)
    mv      a1  s3                          # a1 <- Endereço de centroids
    jal     printCentroids
# Stack Pop
    lw      ra  0(sp)
    lw      s0  4(sp)
    lw      s1  8(sp)
    lw      s2  12(sp)
    lw      s3  16(sp)
    lw      s4  20(sp)
    addi    sp  sp  24
# Return
    jr ra


### cleanCentroids
# Limpa os centroides (a branco) da LED matrix.
# Argumentos:
#   - a0: k val
#   - a1: centroids addr
# Retorno: nenhum
# OPTIMIZATION
# Em vez do ecrã ser totalmente limpo no início de cada iteração do algoritmo,
# é mais eficiente limpar apenas os centroides, pois são os únicos que podem
# mudar de posição (os pontos mudam apenas de cor, então basta apenas pintar por cima).

cleanCentroids:
# Stack Push
    addi    sp  sp  -16
    sw      ra  0(sp)
    sw      s0  4(sp)
    sw      s1  8(sp)
    sw      s2  12(sp)
# Setup
    mv      s0  a0                          # s0 <- Valor de k (a0)
    slli    s0  s0  3                       # x e y (2 words por centroide)
    mv      s1  a1                          # s1 <- Endereço de centroids (a1)
    add     s0  s1  s0                      # s0 <- Endereço final de centroids
    li      s2  white                       # s2 <- Cor branca
cleanCentroidsLoop:
    bge     s1  s0  end_cleanCentroids      # if Endereço Atual >= Endereço Final -> end_cleanCentroids
    lw      a0  0(s1)                       # a0 <- Coordenada x do centroide
    lw      a1  4(s1)                       # a1 <- Coordenada y do centroide
    mv      a2  s2                          # a2 <- Cor branca
    jal     printPoint                      # call printPoint
    addi    s1  s1  8                       # Endereço do Próximo Centroid
    j       cleanCentroidsLoop              # Próxima iteração
end_cleanCentroids:
#stack pop
    lw      ra  0(sp)
    lw      s0  4(sp)
    lw      s1  8(sp)
    lw      s2  12(sp)
    addi    sp  sp  16
    jr      ra

### resetClusters
# Coloca os valores do array clusters a 0.
# Necessário no início de cada iteração de k-means.
# No início de cada iteração cada centroide tem 0 pontos associados.
# Argumentos:
#     - a0: Valor de k
#     - a1: Endereço de clusters
# Retorno: nenhum

resetClusters:
    addi    t0  x0  12                      # Cada centroide ocupa 12 bytes no clusters (3 words)
    mul     t0  t0  a0
    add     t0  a1  t0                      # t0 <- Endereço final do clusters
resetClustersLoop:
    bge     a1  t0  end_resetClusters       # if EndereçoAtual >= EndereçoFinal -> end_resetClusters
    sw      x0  0(a1)                       # Reset do somatório de X do centroide (sum(x) = 0)
    sw      x0  4(a1)                       # Reset do somatório de Y do centroide (sum(y) = 0)
    sw      x0  8(a1)                       # Reset do número de pontos associado ao centroide
    addi    a1  a1  12                      # Próximo Centroide
    j       resetClustersLoop               # Próxima Iteração
end_resetClusters:
    jr      ra                              # Return 


### printPoint
# Pinta o ponto (x,y) na LED matrix com a cor passada por argumento.
# Argumentos:
#   - a0: x
#   - a1: y
#   - a2: cor

printPoint:
    li      a3  LED_MATRIX_0_HEIGHT
    sub     a1  a3  a1
    addi    a1  a1  -1
    li      a3  LED_MATRIX_0_WIDTH
    mul     a3  a3  a1
    add     a3  a3  a0
    slli    a3  a3  2
    li      a0  LED_MATRIX_0_BASE
    add     a3  a3  a0                      
    sw      a2  0(a3)
    jr      ra


### printClusters
# Pinta os agrupamentos na LED matrix com a cor correspondente.
# Chama nearestCluster para calcular o cluster de cada ponto.
# Chama updateClusters para fazer update do respetivo centroide.
# Chama printPoint para pintar cada ponto.
# Argumentos:
#   - a0: Valor de n
#   - a1: Endereço de points
#   - a2: Valor de k
#   - a3: Endereço de centroids
# Retorno: nenhum

printClusters:
# Stack Push
    addi    sp  sp  -28
    sw      ra  0(sp)
    sw      s0  4(sp)
    sw      s1  8(sp)
    sw      s2  12(sp)
    sw      s3  16(sp)
    sw      s4  20(sp)
    sw      s5  24(sp)
# Argumentos
    mv      s0  a0                          # Valor de n
    slli    s0  s0  3                       # 8 bytes (por ponto)
    mv      s1  a1                          # s1 <- Endereço de points (a1)
    add     s0  s1  s0                      # s0 <- Endereço final de points
    mv      s2  a2                          # s2 <- Valor de k
    mv      s3  a3                          # s3 <- Endereço de centroids
    la      s4  clusters                    # s4 <- Endereço de clusters
    la      s5  colors                      # s5 <- Endereço de colors
printClustersLoop:
    bge     s1  s0  end_printClustersLoop   # if (EndereçoAtual >= EndereçoFinal) -> end_printClustersLoop
    
    lw      a0  0(s1)                       # a0 <- x do ponto
    lw      a1  4(s1)                       # a1 <- y do ponto
    mv      a2  s2                          # a2 <- Valor de k (s2)
    mv      a3  s3                          # a3 <- Endereço de centroids (s3)
    jal     nearestCluster                  # nearestCluster (a0 <- índice do centroide mais próximo)
    
    mv      a2  a0                          # a2 <- Índice do centroide (a0)
    lw      a0  0(s1)                       # a0 <- x do ponto
    lw      a1  4(s1)                       # a1 <- y do ponto
    mv      a3  s4                          # a3 <- Endereço de clusters
    jal     updateClusters                  # updateClusters (a0 <- índice do centroide mais próximo)
    
    slli    a0  a0  2                       # Offset da cor [bytes]
    add     a0  s5  a0                      # Endereço da cor
    lw      a2  0(a0)                       # a2 <- Cor do ponto
    lw      a0  0(s1)                       # a0 <- x do ponto
    lw      a1  4(s1)                       # a1 <- y do ponto
    jal     printPoint                      # printPoint call
    addi    s1  s1  8                       # i++ (points)
    
    j printClustersLoop                     # Próxima Iteração
end_printClustersLoop:
# Stack Pop
    lw      ra  0(sp)
    lw      s0  4(sp)
    lw      s1  8(sp)
    lw      s2  12(sp)
    lw      s3  16(sp)
    lw      s4  20(sp)
    lw      s5  24(sp)
    addi    sp  sp  28
# Return
    jr      ra

### nearestCluster
# Calcula a distância de Manhattan do ponto (x, y) e retorna o índice do centroide mais próximo deste.
# Argumentos:
#   - a0: x do ponto
#   - a1: y do ponto
#   - a2: Valor de k
#   - a3: Endereço de centroids
# Retorno:
#   - a0: índice do centróide mais próximo do ponto (x, y)
#OPTIMIZATION
# A verificação inicial de k == 1 evita a execução desnecessária do algoritmo quando há apenas um centroide. 
# Isso reduz o número de instruções ao atribuir ao ponto o único centroide possível.
nearestCluster:
# Check (k == 1 -> Não é preciso calcular centroide mais próximo)
    addi    t0  x0  1 
    beq     t0  a2  skip_nearestCluster     # if (k == 1) -> skip_nearestCluster
# Stack Push
    addi    sp  sp  -32
    sw      ra  0(sp)
    sw      s0  4(sp)
    sw      s1  8(sp)
    sw      s2  12(sp)
    sw      s3  16(sp)
    sw      s4  20(sp)
    sw      s5  24(sp)
    sw      s6  28(sp)
# Argumentos
    mv      s0  a0                          # s0 <- x do ponto (a0)
    mv      s1  a1                          # s1 <- y do ponto (a1)
    mv      s2  a2                          # s2 <- valor de k (a2)
    mv      s3  a3                          # s3 <- Endereço de centroids (a3)
    
    addi    s4  x0  0                       # s4 <- índice
    addi    s5  x0  63                      # s5 <- maior distância possível é 63
    addi    s6  x0  0                       # s6 <- Valor de retorno
nearestClusterLoop:
    bge     s4  s2  end_nearestCluster      # if (índice >= k) -> end_nearestCluster
    mv      a0  s0                          # a0 <- x do ponto
    mv      a1  s1                          # a1 <- y do ponto
    lw      a2  0(s3)                       # a3 <- x do centroide
    lw      a3  4(s3)                       # a4 <- y do centroide
    jal     manhattanDistance               # manhattanDistance call (a0 <- manhattan distance)
    bge     a0  s5  next_nearestClusterLoop # if (atual distance >= saved distance) -> next_nearestClusterLoop
    mv      s5  a0                          # Guardar manhattan distance atual  (mais pequena)
    mv      s6  s4                          # Guardar índice do centroide atual (mais próximo)
next_nearestClusterLoop:
    addi    s3  s3  8                       # Próximo centroide
    addi    s4  s4  1                       # índice++
    j nearestClusterLoop
end_nearestCluster:
    mv      a0  s6                          # Return do índice do centroide (mais próximo)
# Stack Pop
    lw      ra  0(sp)
    lw      s0  4(sp)
    lw      s1  8(sp)
    lw      s2  12(sp)
    lw      s3  16(sp)
    lw      s4  20(sp)
    lw      s5  24(sp)
    lw      s6  28(sp)
    addi    sp  sp  32
    jr      ra                              # Return    
skip_nearestCluster:                        # (k == 1)
    addi    a0  x0  0                       # índice = 0
    jr      ra                              # Return 


### manhattanDistance
# Calcula e retorna a distância de Manhattan entre (x0, y0) e (x1, y1).
# Esta distância é dada pela expressão: |x0 - x1| + |y0 - y1|
# Argumentos:
# a0, a1: x0, y0
# a2, a3: x1, y1
# Retorno:
# a0: distância de Manhattan entre dois pontos

manhattanDistance:
    sub     t0  a0  a2                      # t0 <- (x = x0 - x1)
    sub     t1  a1  a3                      # t1 <- (y = y0 - y1)
    bge     t0  x0  manhattanDistance_Y     # if (x > 0) -> manhattanDistance_Y
    sub     t0  x0  t0                      # t0 <- abs(x)
manhattanDistance_Y:
    bge     t1  x0  end_manhattanDistance   # if (y > 0) -> end_manhattanDistance
    sub     t1  x0  t1                      # t1 <- abs(y)
end_manhattanDistance:
    add     a0  t0  t1                      # a0 <- x + y
    jr ra                                   # Return


### updateClusters
# Recebe coordenadas x e y de um ponto e o índice do cluster (centroide) a que pertence.
# Para o cluster associado, atualiza os somatórios de (X, Y) e incrementa o número de pontos.
# Argumentos:
#   - a0: x do ponto
#   - a1: y do ponto
#   - a2: Índice do cluster (respetivo centroide)
#   - a3: Endereço de clusters
# Retorno:
#   - a0: Índice de cluster

updateClusters:
    addi    t0  x0  12
    mul     t0  a2  t0
    add     t0  a3  t0                      # Endereço de clusters[i]
    lw      t1  0(t0)                       # Load do x de clusters[i]
    add     t1  t1  a0                      # t1 <- sumX = sumX + xDoPonto
    sw      t1  0(t0)                       # Guarda sumX
    lw      t1  4(t0)                       # Load do y de clusters[i]
    add     t1  t1  a1                      # t1 <- sumY = sumY + yDoPonto 
    sw      t1  4(t0)                       # Guarda sumY 
    lw      t1  8(t0)                       # Load do N de clusters[i]
    addi    t1  t1  1                       # t1 <- novoN = nAnterior + 1
    sw      t1  8(t0)                       # Guarda novoN
    mv      a0  a2                          # Devolve índice de cluster
    jr      ra                              # Return


### calculateCentroids
# Calcula a posição dos k centroides, a partir dos valores respetivos no array clusters.
# newX = sum(X) / n. newY = sum(Y) / n.
# Verifica se nova posição de centroides é igual à antiga.
# Muda a variável de estado 'changed' para 1 se houve alteração nas posições de centroides.
# As optimizações (array clusters e variável de estado 'changed') são aqui evidentes.
# Argumentos:
#   - a0: Valor de k
#   - a1: Endereço de centroids
#   - a2: Endereço de clusters
# Retorno: nenhum


calculateCentroids:
    addi    a3  x0  0                           # a3 <- índice
calculateCentroidsLoop:
    bge     a3  a0  end_calculateCentroids      # if(índice >= k) -> end_calculateCentroids 
    lw      t1  8(a2)                           # Load do N (número de pontos no cluster)
    beq     t1  x0 next_calculateCentroids      # if (N == 0) -> next_calculateCentroids 
    lw      t0  0(a2)                           # Load do sum(X) do cluster
    div     t0  t0  t1                          # newX (centroide) = sum(X)/N
    lw      t2  4(a2)                           # Load do sum(Y) do cluster
    div     t2  t2  t1                          # newY (centroide) = sum(Y)/N
# Verificação de mudança de posição do centroide
    lw      t3  0(a1)                           # Load x antigo do centroide
    lw      t4  4(a1)                           # Load y antigo do centroide
    bne     t0  t3  notEqual_calculateCentroids # if (antigo x != novo x) -> notEqual_calculateCentroids
    bne     t2  t4  notEqual_calculateCentroids # if (antigo y != novo y) -> notEqual_calculateCentroids
    j       equal_calculateCentroids            # if (antigo (x e y) == novo (x e y)) -> equal_calculateCentroids 

notEqual_calculateCentroids:                    # Centroide antigo != Centroide novo
    la      t5  changed
    addi    t6  x0  1
    sw      t6  0(t5)                           # Changed = 1
equal_calculateCentroids:                    
    sw      t0  0(a1)                           # Update centroide x
    sw      t2  4(a1)                           # Update centroide y
next_calculateCentroids:
    addi    a2  a2  12                          # clusters++
    addi    a1  a1  8                           # centroids++
    addi    a3  a3  1                           # índice++
    j       calculateCentroidsLoop              # Próxima Iteração
end_calculateCentroids:
    jr      ra                                  # Return

### printCentroids
# Pinta os centroides na LED Matrix.
# Centroides são pintados de preto.
# Argumentos:
#   - a0: Valor de k
#   - a1: Endereço de centroids
# Retorno: nenhum

printCentroids:
# Stack Push
    addi    sp  sp  -16
    sw      ra  0(sp)
    sw      s0  4(sp)
    sw      s1  8(sp)
    sw      s2  12(sp)
# setup
    mv      s0  a0                          # s0 <- Valor de k (a0)
    slli    s0  s0  3                       # 8 bytes por centroide
    mv      s1  a1                          # s1 <- Endereço de centroids
    add     s0  s1  s0                      # s0 <- Endereço final de centroids
    li      s2  black                       # s2 <- Cor Preta
printCentroid:
    bge     s1  s0  end_printCentroids      # if (EndereçoAtual >= EndereçoFinal) -> end_printCentroids
    lw      a0  0(s1)                       # Load x do centroide
    lw      a1  4(s1)                       # Load y do centroide
    mv      a2  s2                          # a2 <- Cor Preta (s2)
    jal     printPoint                      # printPoint call
    addi    s1  s1  8                       # Próximo centroide
    j       printCentroid                   # Próxima iteração
end_printCentroids:
# Stack Pop
    lw      ra  0(sp)
    lw      s0  4(sp)
    lw      s1  8(sp)
    lw      s2  12(sp)
    addi    sp  sp  16
    jr ra                                   # Return