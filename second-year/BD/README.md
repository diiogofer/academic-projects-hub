# ✈️ BD: Aviation Management System
> **Data Modeling, SQL, Web Development, Data analysis & Performance Tuning**
> **Grade:** 20 / 20 

This repository hosts the complete project for the Database Systems course, developed in two phases. The goal was to architect and build a robust information system for an **International Aviation Company**, managing everything from fleet and flights to ticket sales and check-in operations. Beyond transactional features, the system includes complex OLAP queries to extract critical business insights and was rigorously tested and successfully defended before the faculty.

---

## 🌍 Language / Língua
* [English Version](#-project-overview-en)
* [Versão Portuguesa](#-resumo-dos-projetos-pt)

---

## 🇬🇧 Project Overview (EN)

### Phase 1: Data Modeling & Schema Design
**Goal:** Design the core database architecture for the airline ecosystem.
* **Conceptual Modeling:** Designed a comprehensive Entity-Relationship (ER) Model covering Airports, Terminals, Fleet (Models, Seats), Commercial Flights, and Sales.
* **Relational Schema:** Mapped the ER model to a normalized Relational Schema to ensure data integrity.
* **Complex Logic:** Modeled hierarchical seat classes (1st/2nd class), flight schedules, and passenger manifests.



### Phase 2: Application & Optimization
**Goal:** Develop a transactional Web API and optimize database performance.
* **Web API (Flask):** Built a RESTful API using **Python** and **Psycopg 3** with a Connection Pool.
    * **Endpoints:** Implemented flight search (`/voos/<partida>`), ticket purchasing (`/compra`), and automatic seat allocation (`/checkin`).
* **Concurrency Control:**
    * Implemented **ACID Transactions** to handle critical operations.
    * Used **Row-Level Locking** (`FOR UPDATE SKIP LOCKED`) in the check-in logic to prevent multiple passengers from grabbing the same seat simultaneously.
* **Integrity Constraints:** Enforced complex business rules using SQL Triggers (e.g., ensuring ticket sales don't exceed aircraft capacity).
* **Performance Tuning:** Analyzed query plans with `EXPLAIN ANALYZE` and optimized slow queries using B-Tree/Hash Indexes.

---

## 🇵🇹 Resumo dos Projetos (PT)

### Fase 1: Modelação de Dados
**Objetivo:** Desenhar a arquitetura da base de dados para o ecossistema da companhia aérea.
* **Modelação Concetual:** Criação de um Modelo Entidade-Associação (EA) complexo abrangendo Aeroportos, Terminais, Frota (Modelos, Assentos), Voos Comerciais e Vendas.
* **Esquema Relacional:** Mapeamento para um esquema normalizado, garantindo integridade e minimizando redundância.
* **Lógica de Negócio:** Modelação de classes de assentos (1ª/2ª classe), escalas de voo e manifestos de passageiros.

[Imagem do Diagrama EA ou Esquema Relacional]

### Fase 2: Aplicação e Otimização
**Objetivo:** Desenvolver uma Web API transacional e otimizar a performance.
* **Web API (Flask):** Desenvolvimento de uma API RESTful usando **Python** e **Psycopg 3** com Connection Pool.
    * **Endpoints:** Pesquisa de voos (`/voos/<partida>`), compra de bilhetes (`/compra`) e alocação automática de assentos (`/checkin`).
* **Controlo de Concorrência:**
    * Implementação de **Transações ACID** para operações críticas.
    * Uso de **Bloqueio ao Nível da Linha** (`FOR UPDATE SKIP LOCKED`) na lógica de check-in para impedir que múltiplos passageiros reservem o mesmo lugar ao mesmo tempo.
* **Restrições de Integridade:** Implementação de regras de negócio complexas via Triggers SQL (ex: garantir que vendas não excedem a capacidade do avião).
* **Otimização:** Análise de planos de execução com `EXPLAIN ANALYZE` e criação de Índices B-Tree/Hash para acelerar pesquisas volumosas.

---

### 🛠️ Tech Stack
* **Database:** PostgreSQL
* **Backend:** Python, Flask, Psycopg 3
* **Performance:** `EXPLAIN ANALYZE`, Database Indexing
* **Concepts:** ACID Transactions, Row-Level Locking, REST API, ER Modeling

### 👨‍💻 Authors / Autores
* **Michael Maycock**
* **Diogo Fernandes**
* **Pedro Ideias**