# 🧠 AI: Nuruomino Solver
> **Artificial Intelligence | Inteligência Artificial**  
> **Grade:** 20 / 20

This repository contains a high-performance solver for the **Nuruomino** puzzle, developed for the Artificial Intelligence course. The project applies a generic search library to a Constraint Satisfaction Problem (CSP), utilizing heuristics to navigate the state space efficiently.

---

## 🌍 Language / Língua
* [English Version](#-project-overview-en)
* [Versão Portuguesa](#-resumo-do-projeto-pt)

---

## 🇬🇧 Project Overview (EN)

### 🧩 The Puzzle: Nuruomino
Nuruomino is a logic puzzle played on a rectangular grid. Some cells contain numbers. The goal is to partition the grid into polyominoes (blocks of connected cells) such that:
1.  Each number $n$ must be part of a polyomino of size $n$.
2.  Each polyomino must contain exactly one number.
3.  Two polyominoes of the same size cannot share an edge (orthogonal adjacency).

### 🚀 Technical Implementation
* **Heuristics:** Designed custom admissible heuristics to guide the A* algorithm, estimating the remaining cost to solve the board and pruning invalid branches early.
* **State Representation:** Efficient modeling of the board state (`NuruominoState`) to minimize memory usage during deep recursion.

### 🛠️ Tech Stack
* **Language:** Python 3.8+
* **Concepts:** State-Space Search, Heuristics, Constraint Satisfaction Problems (CSP), Graph Theory, Forward Checking.

---

## 🇵🇹 Resumo do Projeto (PT)

### 🧩 O Puzzle: Nuruomino
O Nuruomino é um puzzle lógico jogado numa grelha retangular. O objetivo é particionar a grelha em poliominós (blocos de células conectadas) respeitando as regras:
1.  Cada número $n$ deve fazer parte de um poliominó de tamanho $n$.
2.  Cada poliominó deve conter exatamente um número.
3.  Dois poliominós do mesmo tamanho não podem partilhar uma aresta (adjacência ortogonal).

### 🚀 Implementação Técnica
* **Heurísticas:** Criação de heurísticas admissíveis personalizadas para guiar o algoritmo A*, estimando o custo restante e cortando ramos inválidos rapidamente.
* **Representação de Estado:** Modelação eficiente do estado do tabuleiro (`NuruominoState`) para minimizar o uso de memória durante a recursão profunda.

### 👨‍💻 Authors / Autores
* Diogo Fernandes
* Michael Maycock