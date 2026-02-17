# 🏗️ K-Means Clustering em RISC-V | 2023-2024
> **Grade / Nota:** 20 / 20

Este projeto consiste na implementação do algoritmo de **K-Means Clustering** em Assembly RISC-V, otimizado para eficiência de memória e desempenho de execução no simulador Ripes.

---

## 🌍 Language / Língua
* [English Version](#-project-overview-en)
* [Versão Portuguesa](#-resumo-do-projeto-pt)

---

## 🇬🇧 Project Overview (EN)

### 🎯 Objective
To develop a program in **RISC-V Assembly** capable of grouping a set of 2D points into $k$ clusters based on their relative proximity. The visualization is performed using an **LED Matrix** peripheral.

* **Algorithm:** Iterative K-Means.
* **Metric:** Manhattan Distance (to avoid floating-point operations).
* **Architecture:** RISC-V 32-bit (Simulated in Ripes).
* **Visualization:** 32x32 LED Matrix.

### 🚀 Key Optimizations
This project received the maximum grade due to several optimizations that went beyond the professor's base requirements:

1.  **Memory Efficiency (`clusters` array):**
    * *Base requirement:* Store an array of size $N$ mapping each point to a cluster.
    * *Our Implementation:* We replaced the $N$-sized array with a compressed structure of size $3 \times K$. For each centroid, we store only the `sum(X)`, `sum(Y)`, and `count`. This drastically reduces memory usage and eliminates the need to iterate through all points again to calculate averages.

2.  **Rendering Performance (`cleanCentroids` vs `cleanScreen`):**
    * Instead of wiping the entire LED matrix (white) at every iteration, we implemented a targeted cleaning function that only repaints the old centroid positions. This significantly reduces the instruction count per frame.

3.  **Execution Logic:**
    * **Early Exit:** Implemented a `changed` flag. If an iteration produces no changes in centroid positions, the loop terminates immediately, avoiding unnecessary calculations.
    * **Direct Memory Access:** The screen cleaning loop uses direct memory addressing rather than calling the `printPoint` function overhead for every pixel.

4.  **Pseudo-Random Initialization:**
    * Implemented a **Linear Congruential Generator (LCG)** using the system time (`Time_msec` syscall) to generate truly random starting positions for centroids, rather than hardcoded ones.

### 🛠️ How to Run
1.  Open **Ripes**.
2.  Load the `k-means.s` file.
3.  In the "I/O" tab, double-click **LED Matrix**.
    * **Height:** 32
    * **Width:** 32
4.  Run the simulation.

---

## 🇵🇹 Resumo do Projeto (PT)

### 🎯 Objetivo
Desenvolver um programa em **Assembly RISC-V** capaz de agrupar um conjunto de pontos 2D em $k$ clusters, tendo em conta a sua proximidade relativa. A visualização é feita através de um periférico **LED Matrix**.

* **Algoritmo:** K-Means Iterativo.
* **Métrica:** Distância de Manhattan (para evitar vírgula flutuante).
* **Arquitetura:** RISC-V 32-bit (Simulado no Ripes).
* **Visualização:** LED Matrix 32x32.

### 🚀 Principais Otimizações
Este projeto obteve a nota máxima devido a várias otimizações implementadas além do enunciado base:

1.  **Eficiência de Memória (Array `clusters`):**
    * *Enunciado:* Sugeria um vetor de tamanho $N$ para mapear cada ponto a um cluster.
    * *Nossa Solução:* Substituímos esse vetor por uma estrutura comprimida de tamanho $3 \times K$. Guardamos apenas `soma(X)`, `soma(Y)` e `contagem` para cada centróide. Isto reduz drasticamente o uso de memória e elimina uma iteração completa sobre os pontos para calcular médias.

2.  **Performance de Renderização (`cleanCentroids`):**
    * Em vez de limpar o ecrã todo a cada iteração (o que é lento em assembly), implementámos uma limpeza "cirúrgica" que apaga apenas a posição antiga dos centróides, mantendo o resto do ecrã intacto.

3.  **Lógica de Execução:**
    * **Saída Antecipada:** Implementação da flag `changed`. Se uma iteração não alterar a posição dos centróides, o algoritmo termina imediatamente.
    * **Acesso Direto à Memória:** A função de limpar o ecrã escreve diretamente nos endereços de memória da matriz, evitando a sobrecarga de chamar a função `printPoint` 1024 vezes.

4.  **Inicialização Aleatória (LCG):**
    * Implementação de um algoritmo **Linear Congruential Generator** usando a syscall de tempo (`Time_msec`) para gerar posições iniciais verdadeiramente aleatórias, em vez de usar valores fixos.

### 🛠️ Como Executar
1.  Abrir o **Ripes**.
2.  Carregar o ficheiro `k-means.s`.
3.  No separador "I/O", adicionar uma **LED Matrix**.
    * **Height (Altura):** 32
    * **Width (Largura):** 32
4.  Executar a simulação.

---

### Authors / Autores
* **Bernardo Lopes**
* **Michael Maycock**
* **Diogo Fernandes**