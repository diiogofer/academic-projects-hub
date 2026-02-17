# Descrição detalhada da ideia:
# O nosso objetivo é antes do solver, criar as variáveis do problema de forma a evitar criar variáveis inúteis.
# Para além de mais, temos de evitar restrições que sejam redundantes pois o solver é mais rápido quando menos restrições tem de verificar
# Para isso, aqui estão algumas ideias:
# 1) Se uma criança recebe no máximo 1 brinquedo, mas não tem fabricas ou tem fábricas k com stock 0, entao nao criamos x_(i,k)
# 2) Se uma criança está num país no qual o mínimo de brinquedos a receber é 0, então não criamos x_(i,k) para essa criança. Não sei se isto está feito
# 3) Já está feito: 3) Se uma criança está num país diferente das fábricas que pediu, e o país das fábricas tem maximo export = 0 então não criamos

from pulp import *

# Tudo Para lines e depois fazemos o parse
lines = sys.stdin.read().strip().split('\n')
idx = 0
n, m, t = map(int, lines[idx].split())
idx += 1

# Para evitar a criação de range_() varias vezes
range_n = range(n) # fabricas
range_m = range(m) # países
range_t = range(t) # crianças

# Fábricas
stock_max = [0] * n
fabrica_country = [0] * n

for _ in range_n:
    fabric_id, country_id, stock_limit = map(int, lines[idx].split())
    idx += 1
    stock_max[fabric_id - 1] = stock_limit
    fabrica_country[fabric_id - 1] = country_id - 1

# Países
max_export_list = [0] * m
min_distr_list = [0] * m

for _ in range_m:
    country_id, max_export, min_distr = map(int, lines[idx].split())
    idx += 1
    max_export_list[country_id - 1] = max_export
    min_distr_list[country_id - 1] = min_distr

# Crianças
pais_crianca = [0] * t
fabricas_crianca = [[] for _ in range_t]
crianças_por_fabrica = [[] for _ in range_n]
pairs_in_country = [[] for _ in range_m]
pairs_export_by_country = [[] for _ in range_m]
numberOfDesejos = [0] * t

for _ in range_t:
    info = list(map(int, lines[idx].split()))
    idx += 1
    child_id = info[0] - 1
    child_country = info[1] - 1
    pais_crianca[child_id] = child_country
    
    # Linha reconstruída baseada na lógica visível e comentários
    factories = [f-1 for f in info[2:] if (stock_max[f-1] > 0)]
    
    # # Aqui evitamos que na lista de fábricas da criança estejam fábricas sem stock ou até mesmo fábricas de países que não possam exportar
    fabricas_crianca[child_id] = factories
    for i in factories:
        crianças_por_fabrica[i].append(child_id) # Aqui não dá logo para dizer que crianas por fabrica [i] = factories e acabou a conversa
        pairs_in_country[child_country].append((i, child_id)) # Para na restrição do min_distr não se percorrer o x todo a cada iteração
        # tenho de garantir que a criança está num pais diferente ou no mesmo pais da fabrica ou nao tenho de fazer nada e está bom assim?
        if fabrica_country[i] != child_country: # (simboliza que vai exportar)
            pairs_export_by_country[fabrica_country[i]].append((i, child_id))
    numberOfDesejos[child_id] += 1

# Definir o problema como Maximização
prob = LpProblem("Proj3", LpMaximize)

# As Variáveis do Problema estão em x_(i,k) = fábrica i, criança k
x = {}
for k in range_t:
    for i in fabricas_crianca[k]:
        x[(i, k)] = LpVariable(f"x_{i}_{k}", 0, 1, cat="Binary")

# Função Objetivo
prob += pulp.lpSum(x[(i, k)] for (i, k) in x)

# Restrições

# 1) Cada criança recebe no máximo 1 brinquedo
for k in range_t:
    if numberOfDesejos[k] != 0:
        prob += lpSum(x[(i, k)] for i in fabricas_crianca[k]) <= 1

# 2) Cada fábrica tem um máximo de stock
for i in range_n:
    maracuja = lpSum(x[(i, k)] for k in crianças_por_fabrica[i])
    if len(crianças_por_fabrica[i]) > stock_max[i]:
        prob += maracuja <= stock_max[i]

# 3) Cada país tem um mínimo de brinquedos a receber
for j in range_m:
    maracuja = lpSum(x[(i,k)] for (i,k) in pairs_export_by_country[j])
    if len(pairs_export_by_country[j]) > max_export_list[j]:
        prob += maracuja <= max_export_list[j]
    
    if pairs_in_country[j]: # se houver ao menos uma variável
        prob += lpSum(x[(i, k)] for (i, k) in pairs_in_country[j]) >= min_distr_list[j]
    else: # Se não houverem nem se fazem restrições
        continue

# 4) Cada país tem um máximo de exportação (Nota: já tratado acima no loop #3)

# Magia do Python Solve
prob.solve(pulp.PULP_CBC_CMD(msg=0))
status = LpStatus[prob.status]

if status in ("Optimal", "Feasible"):
    print(int(value(prob.objective)))
else:
    print(-1)
