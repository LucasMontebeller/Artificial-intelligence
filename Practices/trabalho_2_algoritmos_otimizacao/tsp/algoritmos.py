from tsp import solucao_aleatoria, obtem_melhor_vizinho, calcula_custo
from abc import ABC, abstractmethod
import numpy as np

class Algoritmo(ABC):

    def __init__(self, tsp):
        self.tsp = tsp

    @abstractmethod
    def executa(self):
        pass

class Estado():

    def __init__(self, tsp, solucao=None, custo=None):
        self.tsp = tsp
        self.solucao = solucao or solucao_aleatoria(tsp)
        self.custo = custo or calcula_custo(tsp, self.solucao)

    def gera_vizinho_aleatorio(self):
        corte_inicial, corte_final = self.gera_cortes() 
        solucao_vizinho = self.solucao.copy()

        # efetua a troca na solução
        aux = solucao_vizinho[corte_inicial]
        solucao_vizinho[corte_inicial] = solucao_vizinho[corte_final]
        solucao_vizinho[corte_final] = aux

        return Estado(self.tsp, solucao_vizinho)

    def gera_cortes(self, ordem_importante=False):
        # gera duas posições aleatórias dentro da solução, não alterando a cidade inicial A0
        tamanho_solucao = len(self.solucao)
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
    
    # Define comparativo baseado no hash (solucao, custo)
    def __eq__(self, other):
        if isinstance(other, Estado):
            return self.solucao == other.solucao and self.custo == other.custo
        return False
    
    def __hash__(self):
        return hash((tuple(self.solucao), self.custo))


class Hill_Climbing(Algoritmo):

    def __init__(self, tsp, solucao_inicial):
        super().__init__(tsp)
        self.solucao_inicial = solucao_inicial
        self.passos = []
        self.melhor_custo = []

    def executa(self):
        melhor_estado = Estado(self.tsp, self.solucao_inicial)

        # limpa as informações da classe
        passos = 0
        self.limpa_dados()
        while True:
            # Dados para gerar o gráfico da evolução da função objetivo
            self.passos.append(passos)
            self.melhor_custo.append(melhor_estado.custo)

            estado_vizinho = melhor_estado.gera_vizinho_aleatorio()

            if estado_vizinho.custo < melhor_estado.custo:
                melhor_estado = estado_vizinho
            else:
                break   # custo nao melhorou, entao sai do while

            passos += 1

        return melhor_estado, self.coleta_dados()
    
    def coleta_dados(self):
        return self.passos, self.melhor_custo
    
    def limpa_dados(self):
        self.passos.clear()
        self.melhor_custo.clear()

    
class Hill_Climbing_Restart(Algoritmo):

    def __init__(self, tsp, solucao_inicial, num_restarts):
        super().__init__(tsp)
        self.solucao_inicial = solucao_inicial
        self.num_restarts = num_restarts
        self.passos = []
        self.melhor_custo = []

    def executa(self):
        melhor_estado_global = None

        # limpa as informações da classe
        self.limpa_dados()
        passos = 0

        hill_climbing = Hill_Climbing(self.tsp, self.solucao_inicial)
        for _ in range(self.num_restarts):
            melhor_estado_local = hill_climbing.executa()[0]

            if melhor_estado_global is None or melhor_estado_local.custo < melhor_estado_global.custo:
                melhor_estado_global = melhor_estado_local

            self.passos.append(passos)
            self.melhor_custo.append(melhor_estado_global.custo)
            passos+=1

        return melhor_estado_global, self.coleta_dados()
    
    def coleta_dados(self):
        return self.passos, self.melhor_custo
    
    def limpa_dados(self):
        self.passos.clear()
        self.melhor_custo.clear()
        

class Simulated_Annealing(Algoritmo):

    def __init__(self, tsp, solucao_inicial, temperatura, taxa_resfriamento):
        super().__init__(tsp)
        self.solucao_inicial = solucao_inicial
        self.temperatura = temperatura
        self.taxa_resfriamento = taxa_resfriamento
        self.passos = []
        self.melhor_custo = []

    # probabilidade dada pelo fator de Boltzmann
    def aceita_vizinho(self, energia: float, temperatura: float):
        return True if np.random.random() < np.exp(-energia/temperatura) else False
        
    def executa(self):
        estado = Estado(self.tsp, self.solucao_inicial)
        melhor_estado = estado
        temperatura = self.temperatura

        # limpa as informações da classe
        passos = 0
        self.limpa_dados()
        while temperatura > 0.1:
            # Dados para gerar o gráfico da evolução da função objetivo
            self.passos.append(passos)
            self.melhor_custo.append(melhor_estado.custo)

            estado_vizinho = estado.gera_vizinho_aleatorio()
            
            # energia do estado
            delta_e = estado_vizinho.custo - estado.custo

            # redução de energia, implicando que a nova solução é melhor que a anterior
            if delta_e < 0:
                estado = estado_vizinho

            # aumento de energia, aceita novos vizinhos com probabilidade ~ T
            elif self.aceita_vizinho(delta_e, temperatura):
                estado = estado_vizinho

            # atualiza o melhor estado
            if estado.custo < melhor_estado.custo:
                melhor_estado = estado
                
            # atualiza temperatura
            temperatura*=self.taxa_resfriamento
            passos+=1

        return melhor_estado, self.coleta_dados()
    
    def coleta_dados(self):
        return self.passos, self.melhor_custo
    
    def limpa_dados(self):
        self.passos.clear()
        self.melhor_custo.clear()
    

class Genetic_Algorithm(Algoritmo):

    def __init__(self, tsp, solucao_inicial, max_iteracoes=50, taxa_mutacao=0.15, tamanho_populacao=15):
        super().__init__(tsp)
        self.solucao_inicial = solucao_inicial
        self.max_iteracoes = max_iteracoes
        self.taxa_mutacao = taxa_mutacao
        self.tamanho_populacao = tamanho_populacao
        self.passos = []
        self.melhor_custo = []

    def cross_over_ox(self, estado_1: Estado, estado_2: Estado):
        
        # caso as duas soluções sejam iguais, não faz sentido continuar o crossover
        if estado_1.solucao == estado_2.solucao:
            return estado_1, estado_2
        
        corte_inicial, corte_final = estado_1.gera_cortes(ordem_importante=True)
        tamanho_solucao = len(estado_1.solucao)

        # gera os descendentes
        filho_1 = [estado_1.solucao[0] if _ == 0 else '' for _ in range(tamanho_solucao)]
        filho_2 = [estado_1.solucao[0] if _ == 0 else '' for _ in range(tamanho_solucao)]

        filho_1[corte_inicial:corte_final] = estado_2.solucao[corte_inicial:corte_final]
        filho_2[corte_inicial:corte_final] = estado_1.solucao[corte_inicial:corte_final]

        # aplica o cross over OX
        genes_1 = estado_1.solucao[corte_final:] + estado_1.solucao[:corte_final]
        genes_1 = [x for x in genes_1 if x not in filho_1]

        genes_2 = estado_2.solucao[corte_final:] + estado_2.solucao[:corte_final]
        genes_2 = [x for x in genes_2 if x not in filho_2]

        # preenche os espaços vazios
        i = corte_final
        for j in range(tamanho_solucao):
            # valida se já esvaziou
            if not genes_1 and not genes_2:
                break

            indice = (i + j) % tamanho_solucao  # índice cíclico

            if filho_1[indice] == '' and genes_1[0] not in filho_1:
                filho_1[indice] = genes_1.pop(0)

            if filho_2[indice] == '' and genes_2[0] not in filho_2:
                filho_2[indice] = genes_2.pop(0)


        return Estado(self.tsp, filho_1), Estado(self.tsp, filho_2)
            
    
    def mutacao(self, estado: Estado):
        # nesse caso a mutação nada mais é que gerar um vizinho, i.e, trocar duas cidades de posição.
        if np.random.random() < self.taxa_mutacao:
            return estado.gera_vizinho_aleatorio()

        return estado
    
    # torneio --> retorna os melhores ou aleatórios n_individuos
    def selecao(self, populacao: set(), n_individuos: int, aleatorio=False):
        if aleatorio:
            return np.random.choice(list(populacao), n_individuos, replace=False)
        return sorted(populacao, key=lambda x: x.custo)[:n_individuos]
    
    def executa(self):
        # população inicial
        estado_inicial = Estado(self.tsp, self.solucao_inicial)
        populacao = set(estado_inicial.gera_vizinho_aleatorio() for _ in range(self.tamanho_populacao))

        # limpa as informações da classe
        passos = 0
        self.limpa_dados()
        for _ in range(self.max_iteracoes):
            melhor_estado = self.selecao(populacao, 1)[0]
            
            # Dados para gerar o gráfico da evolução da função objetivo
            self.passos.append(passos)
            self.melhor_custo.append(melhor_estado.custo)
            
            # selecao
            primeiro_parente, segundo_parente = self.selecao(populacao, 2, aleatorio=False)

            # crossover (gera dois filhos)
            estado_filho_1, estado_filho_2 = self.cross_over_ox(primeiro_parente, segundo_parente)

            # mutacao
            estado_filho_1 = self.mutacao(estado_filho_1)
            estado_filho_2 = self.mutacao(estado_filho_2)

            # adiciona na próxima lista de herdeiros
            populacao.add(estado_filho_1)
            populacao.add(estado_filho_2)

            passos+=1

        return melhor_estado, self.coleta_dados()

    def coleta_dados(self):
        return self.passos, self.melhor_custo
    
    def limpa_dados(self):
        self.passos.clear()
        self.melhor_custo.clear()

class Genetic_Algorithm_Elitismo(Genetic_Algorithm):

    def __init__(self, tsp, solucao_inicial, max_iteracoes=50, taxa_mutacao=0.15, tamanho_populacao=15):
        super().__init__(tsp, solucao_inicial, max_iteracoes, taxa_mutacao, tamanho_populacao)

    # metodo alterntivo para execução com elitismo
    def executa(self):
        
        # população inicial
        estado_inicial = Estado(self.tsp, self.solucao_inicial)
        populacao = set(estado_inicial.gera_vizinho_aleatorio() for _ in range(self.tamanho_populacao))
        populacao_sucessora = []
        melhor_estado = None

        # limpa as informações da classe
        passos = 0
        self.limpa_dados()
        for _ in range(self.max_iteracoes):
            melhor_estado = sorted(populacao, key=lambda x: x.custo)[0] if melhor_estado is None else populacao[0]
            
            for estado in populacao:
                # Dados para gerar o gráfico da evolução da função objetivo
                self.passos.append(passos)
                self.melhor_custo.append(melhor_estado.custo)
                
                # geração de vizinho
                estado_vizinho = estado.gera_vizinho_aleatorio()

                # crossover (gera dois filhos)
                estado_filho_1, estado_filho_2 = self.cross_over_ox(estado, estado_vizinho)

                # mutacao
                estado_filho_1 = self.mutacao(estado_filho_1)
                estado_filho_2 = self.mutacao(estado_filho_2)

                # adiciona na próxima lista de herdeiros
                populacao_sucessora.extend([estado_filho_1, estado_filho_2])

                passos+=1

            # seleção por truncamento
            # limpa as soluções herdeiras para reiniciar o ciclo de busca, preservando os melhores indivíduos até o momento (elitismo)
            populacao = sorted(set(populacao_sucessora.copy()), key=lambda x: x.custo) [:self.tamanho_populacao]
            populacao_sucessora.clear()

        return melhor_estado, self.coleta_dados()
    
    

class Forca_Bruta(Algoritmo):

    def __init__(self, tsp):
        super().__init__(tsp)

    def executa(self):
        estado = Estado(self.tsp)
        melhor_estado = estado

        while True:

            # tenta obter um candidato melhor
            estado_vizinho = Estado(self.tsp, *obtem_melhor_vizinho(self.tsp, melhor_estado.solucao))

            if estado_vizinho.custo < melhor_estado.custo:
                melhor_estado = estado_vizinho
            else:
                break   # custo nao melhorou, entao sai do while

        return melhor_estado, (list(), list()) # a principio não exibiremos no gráfico