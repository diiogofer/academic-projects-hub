# 🧮 ASA: Analysis and Synthesis of Algorithms
> **Algorithm Design & Complexity Analysis**

This repository documents three advanced algorithmic challenges solved during the Analysis and Synthesis of Algorithms course. These projects focused on **Dynamic Programming**, **Graph Theory**, and **Linear Programming**, emphasizing strict time and space complexity constraints.

> **⚠️ Note:** The original source code was hosted on the Mooshak evaluation system and is currently unavailable. This documentation is based on the technical reports and complexity analysis performed for the final submission.

---

## 🌍 Language / Língua
* [English Version](#-project-overview-en)
* [Versão Portuguesa](#-resumo-dos-projetos-pt)

---

## 🇬🇧 Project Overview (EN)

### 1️⃣ Project 1: Optimal Bracketing (Dynamic Programming)
**Problem:** Given a sequence of integers and a custom binary operator defined by a value matrix, determine the optimal order of operations (bracketing) to achieve a target result.
* **Algorithm:** Bottom-Up Dynamic Programming.
* **Key Logic:**
    * **DP State:** `dp[i][j]` stores the possible results of the subsequence from index `i` to `j`.
    * **Recurrence:** The solution combines results from sub-problems: $dp(i,j) = \bigcup (dp(i, k) \oplus dp(k+1, j))$.
    * **Optimization:** Used a boolean vector to store only the first occurrence of each result per cell, ensuring constant time lookups and pruning redundant calculations.
* **Complexity:** $O(m^3 n^2)$, where $m$ is the sequence length and $n$ is the domain size (matrix dimension).

### 2️⃣ Project 2: Metro Network Connectivity (Graphs)
**Problem:** Calculate the connectivity index of a metro network, defined as the maximum number of line changes required to travel between any two stations.
* **Algorithm:** Breadth-First Search (BFS) on a Transformed Graph.
* **Key Logic:**
    * **Graph Transformation:** Converted the station-based graph into a **Line Graph**, where vertices represent **Metro Lines** and edges represent connections (shared stations) between them.
    * **Preprocessing:** Removed redundant sub-lines (lines fully contained within others) to reduce graph size.
    * **Execution:** Ran BFS from every line to find the maximum distance (line changes) in the network.
* **Complexity:** $O(L^2 \cdot V \cdot \log(V))$, dominated by the graph construction phase, where $L$ is lines and $V$ stations.

### 3️⃣ Project 3: Global Toy Distribution (Linear Programming)
**Problem:** Maximize the number of children receiving Christmas toys given constraints on factory stocks, country export limits, and minimum distribution quotas per country.
* **Algorithm:** Linear Programming (LP) using the `PuLP` library.
* **Key Logic:**
    * **Modeling:** Defined binary variables $x_{i,k}$ (1 if child $k$ receives a toy from factory $i$, 0 otherwise).
    * **Constraints:** Implemented strict rules for:
        1. Max 1 toy per child.
        2. Factory stock limits ($fmax_i$).
        3. Minimum gifts per country ($pmin_j$).
        4. Maximum exports per country ($pmax_j$).
    * **Optimization:** Variables and constraints were pruned for cases where factory stocks or export limits were zero, reducing the problem size.
* **Complexity:** Dependent on the LP solver, with problem size roughly $O(n \times t)$ variables and $O(t + n + m)$ constraints.

---

## 🇵🇹 Resumo dos Projetos (PT)

### 1️⃣ Projeto 1: Parentisação Ótima (Programação Dinâmica)
**Problema:** Dada uma sequência de inteiros e um operador binário personalizado definido por uma matriz, determinar a ordem de operações (parentisação) para obter um resultado alvo.
* **Algoritmo:** Programação Dinâmica Bottom-Up.
* **Lógica:**
    * **Estado DP:** `dp[i][j]` armazena os resultados possíveis da subsequência de `i` a `j`.
    * **Recorrência:** Combinação de sub-problemas dividindo a sequência em todas as posições possíveis.
    * **Otimização:** Uso de um vetor de booleanos para armazenar apenas resultados únicos por célula, garantindo verificações em tempo constante.
* **Complexidade:** $O(m^3 n^2)$, onde $m$ é o tamanho da sequência e $n$ o tamanho do domínio.

### 2️⃣ Projeto 2: Conectividade de Metro (Grafos)
**Problema:** Calcular o índice de conectividade de uma rede de metro, definido como o número máximo de mudanças de linha necessárias entre quaisquer duas estações.
* **Algoritmo:** Breadth-First Search (BFS) num Grafo Transformado.
* **Lógica:**
    * **Transformação:** Conversão da rede de estações num grafo onde os vértices são as **Linhas** e as arestas são as conexões entre elas.
    * **Pré-processamento:** Remoção de sublinhas redundantes para reduzir o tamanho do grafo.
    * **Execução:** Múltiplas BFS para encontrar a maior distância (em mudanças de linha) na rede.
* **Complexidade:** $O(L^2 \cdot V \cdot \log(V))$, dominada pela construção do grafo.



### 3️⃣ Projeto 3: Distribuição Global (Programação Linear)
**Problema:** Maximizar o número de crianças que recebem brinquedos, sujeito a limites de stock das fábricas, limites de exportação por país e quotas mínimas por país.
* **Algoritmo:** Programação Linear (LP) usando a biblioteca `PuLP`.
* **Lógica:**
    * **Modelação:** Variáveis binárias $x_{i,k}$ (1 se a criança $k$ recebe da fábrica $i$).
    * **Restrições:** Máx 1 brinquedo/criança, Stock da fábrica, Mínimo por país e Máximo de exportação.
    * **Otimização:** Corte de variáveis e restrições desnecessárias (ex: stocks a zero) para reduzir o modelo.
* **Complexidade:** Dependente do solver, com tamanho do problema aprox. $O(n \times t)$ variáveis e $O(t + n + m)$ restrições.

---

### 👨‍💻 Authors / Autores
* **Michael Maycock**
* **Diogo Fernandes**