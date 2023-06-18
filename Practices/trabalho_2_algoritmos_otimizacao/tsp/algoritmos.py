from tsp import solucao_aleatoria, obtem_melhor_vizinho, calcula_custo
from abc import ABC, abstractmethod
import numpy as np

# obs : validar com o professor se a solução inicial não deveria ser a mesma para todos os algoritmos !
class Algoritmo(ABC):

    def __init__(self, tsp):
        self.tsp = tsp

    @abstractmethod
    def executa(self):
        pass
        

class Hill_Climbing(Algoritmo):

    def __init__(self, tsp):
        super().__init__(tsp)

    def executa(self):

        solucao = solucao_aleatoria(self.tsp)
            
        # melhor solucao ate o momento
        solucao_melhor, custo_melhor = obtem_melhor_vizinho(self.tsp, solucao)

        while True:

            # tenta obter um candidato melhor
            candidato_atual, custo_atual = obtem_melhor_vizinho(self.tsp, solucao_melhor)

            if custo_atual < custo_melhor:
                custo_melhor = custo_atual
                solucao_melhor = candidato_atual
            else:
                break   # custo nao melhorou, entao sai do while
        
        return custo_melhor, solucao_melhor
    
    
class Simulating_Anneling(Algoritmo):

    def __init__(self, tsp, temperatura, taxa_resfriamento, max_iteracoes=2000):
        super().__init__(tsp)
        self.temperatura = temperatura # não está sendo usado devido a mudança no calculo da probabilidade
        self.taxa_resfriamento = taxa_resfriamento
        self.max_iteracoes = max_iteracoes
        self.passos = 0

    # Probabilidade decrecendo linearmente até 90% das iterações, depois zero.
    def aceita_vizinho(self):
        if self.passos >= 0.9 * self.max_iteracoes:
            return False
        else:
            return True if np.random.random() <= 1 - (self.passos/self.max_iteracoes) else False

    def executa(self):

        solucao = solucao_aleatoria(self.tsp)

        # melhor solucao ate o momento
        solucao_melhor, custo_melhor = obtem_melhor_vizinho(self.tsp, solucao)

        for _ in range(self.max_iteracoes):

            # tenta obter um candidato melhor
            candidato_atual, custo_atual = obtem_melhor_vizinho(self.tsp, solucao_melhor)

            # valida se o estado vizinho é melhor em relação ao fitness ou troca para um outro com probabilidade ~ passos (até 90% das iterações), depois 0
            if custo_atual < custo_melhor:
                custo_melhor = custo_atual
                solucao_melhor = candidato_atual
                
            elif self.aceita_vizinho():
                custo_melhor = custo_atual
                solucao_melhor = candidato_atual
                
            # atualiza temperatura e passos
            self.temperatura*=self.taxa_resfriamento
            self.passos+=1

        self.passos=0
        return custo_melhor, solucao_melhor
    

class Genetic_Algorithm(Algoritmo):

    def __init__(self, tsp, max_iteracoes=50, taxa_mutacao=0.15, tamanho_populacao=20):
        super().__init__(tsp)
        self.max_iteracoes = max_iteracoes
        self.taxa_mutacao = taxa_mutacao
        self.tamanho_populacao = tamanho_populacao

    def cross_over_ox(self, solucao_1, solucao_2):
        
        # caso as duas soluções sejam iguais, não faz sentido continuar o crossover
        if solucao_1 == solucao_2:
            return solucao_1, calcula_custo(self.tsp, solucao_1)

        corte_inicial, corte_final = self.gera_cortes(len(solucao_1) + 1, ordem_importante=True)

        # gera os descendentes
        filho_1 = [solucao_1[0] if _ == 0 else '' for _ in range(len(solucao_1))]
        filho_2 = [solucao_1[0] if _ == 0 else '' for _ in range(len(solucao_2))]

        filho_1[corte_inicial:corte_final] = solucao_2[corte_inicial:corte_final]
        filho_2[corte_inicial:corte_final] = solucao_1[corte_inicial:corte_final]

        # aplica o cross over OX
        genes_1 = solucao_1[corte_final:] + solucao_1[:corte_final]
        genes_1 = [x for x in genes_1 if x not in filho_1]

        genes_2 = solucao_2[corte_final:] + solucao_2[:corte_final]
        genes_2 = [x for x in genes_2 if x not in filho_2]

        # preenche os espaços vazios
        for i in range(len(filho_1) - 1, -1, -1):
            if filho_1[i] == '' and genes_1[0] not in filho_1:
                filho_1[i] = genes_1.pop(0)

        for i in range(len(filho_2) - 1, -1, -1):
            if filho_2[i] == '' and genes_2[0] not in filho_2:
                filho_2[i] = genes_2.pop(0)
        
        # realiza o torneio
        custo_filho_1 = calcula_custo(self.tsp, filho_1)
        custo_filho_2 = calcula_custo(self.tsp, filho_2)

        return (filho_1, custo_filho_1) if custo_filho_1 <= custo_filho_2 else (filho_2, custo_filho_2)
    
    def mutacao(self, solucao):
        corte_inicial, corte_final = self.gera_cortes(len(solucao))

        aux = solucao[corte_inicial]
        solucao[corte_inicial] = solucao[corte_final]
        solucao[corte_final] = aux

        return solucao, calcula_custo(self.tsp, solucao)
    
    def gera_cortes(self, tamanho_solucao, ordem_importante=False):
        corte_inicial = corte_inicial = np.random.randint(1, tamanho_solucao)
        corte_final = corte_inicial = np.random.randint(1, tamanho_solucao)

        # gera novos cortes em caso de inconsistências
        while corte_inicial == corte_final:
            corte_final = np.random.randint(1, tamanho_solucao)

        if corte_inicial > corte_final and ordem_importante:
            aux = corte_final
            corte_final = corte_inicial
            corte_inicial = aux

        return corte_inicial, corte_final


    def executa(self):
        
        # população inicial
        solucoes = [solucao_aleatoria(self.tsp) for _ in range(self.tamanho_populacao)]
        solucoes_herdeiras = []
        solucao_melhor, custo_melhor = np.inf, np.inf

        for _ in range(self.max_iteracoes):
            
            for solucao_atual in solucoes:
                
                # valida a melhor solução até o momento
                custo_atual = calcula_custo(self.tsp, solucao_atual)
                if custo_atual < custo_melhor:
                    solucao_melhor = solucao_atual
                    custo_melhor = custo_atual
                
                # selecao
                solucao_vizinho, custo_vizinho = obtem_melhor_vizinho(self.tsp, solucao_atual)
                if custo_vizinho < custo_melhor:
                    custo_melhor = custo_vizinho

                # crossover
                solucao_filho, custo_filho = self.cross_over_ox(solucao_atual, solucao_vizinho)

                # mutacao
                if np.random.random() < self.taxa_mutacao:
                    solucao_filho, custo_filho = self.mutacao(solucao_filho)

                # adiciona na próxima lista de herdeiros, tentando preservar os melhores genes 
                if custo_melhor < custo_filho:
                    solucao_filho = solucao_melhor
                solucoes_herdeiras.append(solucao_filho)

            # limpa as soluções herdeiras para reiniciar o ciclo de busca
            solucoes = solucoes_herdeiras.copy()
            solucoes_herdeiras.clear()
                
        return custo_melhor, solucao_melhor