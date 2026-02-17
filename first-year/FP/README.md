# 🐍 Fundamentos da Programação (FP) | 2023-2024
> **Grade / Nota:** 18,69 / 20 (proj1)  
> **Grade / Nota:** 18,57 / 20 (proj2)

Este diretório contém uma proposta de solução minha para os projetos de Fundamentos da Programação.

---

## 🌍 Language / Língua
* [English Version](#-project-overview-en)
* [Versão Portuguesa](#-resumo-dos-projetos-pt)

---

## 🇬🇧 Project Overview (EN)

### ℹ️ Important Note on Project History
These projects were originally developed and submitted via the University's internal **GitLab** instance. The code present here was migrated to this centralized hub. Therefore, the commit history in this repository does not reflect the original development process carried out 2 years ago (1st Semester, 1st Year).

### 🎮 Project 1: Mountains and Valleys (Montanhas e Vales)
An algorithmic challenge focused on territory analysis using matrix-like structures (tuples of tuples).  
**Goal:** Develop functions to identify mountain chains, connected regions, and "valleys" (adjacent free intersections).  
**Core Concepts:** Matrix traversal, recursion/connectivity algorithms, and rigorous argument validation.  
**Tech:** Python (Pure).  

### 🍱 Project 2: Go Game Engine
Implementation of the logic and Abstract Data Types (ADTs) for the ancient board game **Go**.  
**Goal:** Create a functional engine following official rules, including stone capture, suicide moves, and the "Ko" rule (repetition).  
**Key Focus:** Strict adherence to **Abstraction Barriers** and implementation of complex ADTs (*Interseção*, *Pedra*, *Goban*).  
**Tech:** Python (Functional & Procedural approaches).  

---

## 🇵🇹 Resumo dos Projetos (PT)

### ℹ️ Nota sobre o Histórico de Commits
Estes projetos foram originalmente realizados e submetidos através do **GitLab** interno da Universidade. O código aqui presente foi migrado para este hub centralizado. Como tal, o histórico de commits não reflete o processo de desenvolvimento original ocorrido há 2 anos (1º Semestre, 1º Ano).

### 🏔️ Projeto 1: Montanhas e Vales
Um desafio algorítmico focado na análise de territórios representados por estruturas matriciais.  
**Objetivo:** Identificar cadeias de montanhas, ligações entre interseções e determinar "vales".  
**Conceitos:** Travessia de matrizes, algoritmos de conectividade e validação rigorosa de argumentos.  

### ⚪⚫ Projeto 2: Motor de Jogo Go
Implementação da lógica e Tipos Abstratos de Dados (TADs) para o jogo de tabuleiro **Go**.  
**Objetivo:** Criar um motor funcional que respeite as regras oficiais (captura, suicídio e regra do *Ko*).  
**Foco:** Respeito total pelas **Barreiras de Abstração** e implementação de TADs complexos.  

---

## 🛠️ How to run / Como executar
Cada projeto consiste num ficheiro único `.py`.

```bash
# Project 1
python3 project1.py

# Project 2
python3 project2.py
``` 


## 🧪 Testing & Validation / Testes e Validação

### 🇬🇧 English
> **Note on Academic Integrity:** The test suites (both Public and Private) used for evaluation are the intellectual property of the Faculty. In compliance with academic integrity guidelines, these files are not included in this repository.

**Methodology:** The projects were rigorously validated using the `pytest` framework.  
**Evaluation:** Both projects underwent automated grading via **GitLab CI/CD**, achieving the referred marks in functional correctness.  
**Abstraction Barriers:** For Project 2 (Go), the implementation was verified to ensure strict adherence to Abstract Data Types and abstraction barriers.  

### 🇵🇹 Português
> **Nota sobre Integridade Académica:** As baterias de testes (Públicas e Privadas) utilizadas na avaliação são propriedade intelectual do corpo docente. Em conformidade com as normas de integridade académica, estes ficheiros não são publicados neste repositório.

**Metodologia:** Os projetos foram rigorosamente validados utilizando o framework `pytest`.  
**Avaliação:** Tanto o Projeto 1 como o Projeto 2 foram submetidos ao sistema de avaliação automática via **GitLab CI/CD**, obtendo a pontuação já referida na componente de execução funcional.  
**Barreiras de Abstração:** No Projeto 2 (Go), a implementação foi também verificada para garantir o respeito rigoroso pelos Tipos Abstratos de Dados (TADs).