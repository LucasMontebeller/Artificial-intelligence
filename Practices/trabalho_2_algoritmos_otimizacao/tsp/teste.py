
import numpy as np

solucao_1 = ['A0', 'A2', 'A8', 'A9', 'A1', 'A3', 'A4', 'A5', 'A6', 'A7']
solucao_2 = ['A0', 'A7', 'A6', 'A2', 'A8', 'A9', 'A1', 'A3', 'A4', 'A5']


corte_inicial = np.random.randint(1, len(solucao_1) + 1)
corte_final = np.random.randint(1, len(solucao_1) + 1)

while corte_inicial == corte_final:
    corte_final = np.random.randint(1, len(solucao_1) + 1)

if corte_inicial > corte_final:
    aux = corte_final
    corte_final = corte_inicial
    corte_inicial = aux

print(corte_inicial, corte_final)

filho_1 = [solucao_1[0] if _ == 0 else '' for _ in range(len(solucao_1))]
filho_2 = [solucao_1[0] if _ == 0 else '' for _ in range(len(solucao_2))]

filho_1[corte_inicial:corte_final] = solucao_2[corte_inicial:corte_final]
filho_2[corte_inicial:corte_final] = solucao_1[corte_inicial:corte_final]

genes_1 = solucao_1[corte_final:] + solucao_1[:corte_final]
genes_1 = [x for x in genes_1 if x not in filho_1]

genes_2 = solucao_2[corte_final:] + solucao_2[:corte_final]
genes_2 = [x for x in genes_2 if x not in filho_2]

# print(genes_1, genes_2)

print(filho_1, genes_1, filho_2, genes_2)
for i in range(len(filho_1) - 1, -1, -1):
    if filho_1[i] == '' and genes_1[0] not in filho_1:
        filho_1[i] = genes_1.pop(0)

for i in range(len(filho_2) - 1, -1, -1):
    if filho_2[i] == '' and genes_2[0] not in filho_2:
        filho_2[i] = genes_2.pop(0)

print(filho_1)
print(filho_2)
