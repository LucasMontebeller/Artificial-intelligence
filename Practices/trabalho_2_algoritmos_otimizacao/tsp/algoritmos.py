from tsp import solucao_aleatoria, obtem_melhor_vizinho, calcula_custo
from abc import ABC, abstractmethod
import numpy as np

# obs : validar com o professor se a solução inicial não deveria ser a mesma para todos os algoritmos !
class Algoritmo(ABC):

    def __init__(self, tsp, solucao_inicial):
        self.tsp = tsp
        self.solucao_inicial = solucao_inicial
        self.primeira_chamada = True

    @abstractmethod
    def executa(self):
        pass
    
    # Metodo para limpar os atributos da instância
    @abstractmethod
    def dispose(self):
        pass
        

class Hill_Climbing(Algoritmo):

    def __init__(self, tsp, solucao_inicial):
        super().__init__(tsp, solucao_inicial)
    
    def dispose(self):
        self.primeira_chamada = True

    def executa(self):

        # solucao inicial
        if self.primeira_chamada:
            solucao = self.solucao_inicial
            self.primeira_chamada = False
        else:
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
        
        self.dispose()
        return custo_melhor, solucao_melhor
    
    
class Simulating_Anneling(Algoritmo):

    def __init__(self, tsp, solucao_inicial, temperatura, taxa_resfriamento, max_iteracoes=2000):
        super().__init__(tsp, solucao_inicial)
        self.temperatura = temperatura
        self.taxa_resfriamento = taxa_resfriamento
        self.max_iteracoes = max_iteracoes
        self.passos = 0

    def dispose(self):
        self.primeira_chamada = True
        self.passos = 0

    # Probabilidade decrecendo linearmente até 90% das iterações, depois zero.
    def aceita_vizinho(self):
        if self.passos >= 0.9 * self.max_iteracoes:
            return False
        else:
            return True if np.random.random() <= 1 - (self.passos/self.max_iteracoes) else False

    def executa(self):

        # solucao inicial
        if self.primeira_chamada:
            solucao = self.solucao_inicial
            self.primeira_chamada = False
        else:
            solucao = solucao_aleatoria(self.tsp)

        # melhor solucao ate o momento
        # solucao_melhor, custo_melhor = solucao, calcula_custo(self.tsp, solucao)
        solucao_melhor, custo_melhor = obtem_melhor_vizinho(self.tsp, solucao)

        for _ in range(self.max_iteracoes):

            # gera uma nova solução aleatória para comparação
            # nova_solucao = solucao_aleatoria(self.tsp)
            # candidato_atual, custo_atual = nova_solucao, calcula_custo(self.tsp, nova_solucao)

            # tenta obter um candidato melhor
            candidato_atual, custo_atual = obtem_melhor_vizinho(self.tsp, solucao_melhor)

            # valida se o estado vizinho é melhor em relação ao fitness ou troca para um outro com probabilidade ~ passos (até 90% das iterações), depois 0
            if custo_atual < custo_melhor:
                custo_melhor = custo_atual
                solucao_melhor = candidato_atual
                
            # elif (np.random.random() < np.exp(-delta_E/self.temperatura)):
            elif self.aceita_vizinho():
                custo_melhor = custo_atual
                solucao_melhor = candidato_atual
                
            # atualiza temperatura e passos
            self.temperatura*=self.taxa_resfriamento
            self.passos+=1

        self.dispose()
        return custo_melhor, solucao_melhor