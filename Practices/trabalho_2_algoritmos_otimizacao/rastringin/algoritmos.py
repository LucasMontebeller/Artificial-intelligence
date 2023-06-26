import numpy as np
import random as rd
from abc import ABC, abstractmethod

## Agrupar futuramente essas classes em uma só, para que TSP e Rastrigin utilizem as em conjunto
class Algoritmo(ABC):

    @abstractmethod
    def executa(self):
        pass

class Estado():

    def __init__(self, x=None, y=None, limite=5.2):
        self.x = x or rd.uniform(-limite, limite)
        self.y = y or rd.uniform(-limite, limite)
        self.custo = self.funcao_rastrgin(self.x, self.y)

    # sigma = desvio padrão
    def gera_vizinho_aleatorio(self, sigma=0.7):
        x = self.x + (sigma * np.random.randn())
        y = self.y + (sigma * np.random.randn())

        return Estado(x, y)
    
    # Define comparativo baseado no hash (solucao, custo)
    def __eq__(self, other):
        if isinstance(other, Estado):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    @staticmethod
    def funcao_rastrgin(x, y):
        return 20 + np.power(x,2) - (10 * np.cos(2 * np.pi * x)) + np.power(y,2) - (10 * np.cos(2 * np.pi * y))
    

class Hill_Climbing(Algoritmo):

    def __init__(self, solucao_inicial: Estado):
        self.solucao_inicial = solucao_inicial
        self.passos = []
        self.melhor_custo = []

    def executa(self):
        melhor_estado = self.solucao_inicial

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

    def __init__(self, solucao_inicial: Estado, num_restarts):
        self.solucao_inicial = solucao_inicial
        self.num_restarts = num_restarts
        self.passos = []
        self.melhor_custo = []

    def executa(self):
        melhor_estado_global = None

        # limpa as informações da classe
        self.limpa_dados()
        passos = 0

        hill_climbing = Hill_Climbing(self.solucao_inicial)
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


class Simulating_Anneling(Algoritmo):

    def __init__(self, solucao_inicial, temperatura, taxa_resfriamento):
        self.solucao_inicial = solucao_inicial
        self.temperatura = temperatura
        self.taxa_resfriamento = taxa_resfriamento
        self.passos = []
        self.melhor_custo = []

    # probabilidade dada pelo fator de Boltzmann
    def aceita_vizinho(self, energia: float, temperatura: float):
        return True if np.random.random() < np.exp(-energia/temperatura) else False
        
    def executa(self):
        estado = self.solucao_inicial
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
                melhor_estado = estado

            # aumento de energia, aceita novos vizinhos com probabilidade ~ T
            elif self.aceita_vizinho(delta_e, temperatura):
                estado = estado_vizinho
                
            # atualiza temperatura
            temperatura*=self.taxa_resfriamento
            passos+=1

        return melhor_estado, self.coleta_dados()
    
    def coleta_dados(self):
        return self.passos, self.melhor_custo
    
    def limpa_dados(self):
        self.passos.clear()
        self.melhor_custo.clear()

class Genetic_Algorithm():

    def __init__(self, solucao_inicial, max_iteracoes=50, taxa_mutacao=0.15, tamanho_populacao=20, erro=None):
        self.solucao_inicial = solucao_inicial
        self.max_iteracoes = max_iteracoes
        self.taxa_mutacao = taxa_mutacao
        self.tamanho_populacao = tamanho_populacao
        self.erro = erro
        self.passos = []
        self.melhor_custo = []

    @staticmethod
    def reproduz(e1: Estado, e2: Estado):
        alpha_x, alpha_y = (np.random.uniform(0,1) for _ in range(2))
        x = (alpha_x * e1.x) + (1 - alpha_x) * e2.x
        y = (alpha_y * e1.y) + (1 - alpha_y) * e2.y

        return Estado(x, y)
    
    def mutacao(self, estado: Estado):
        if np.random.random() < self.taxa_mutacao:
            return estado.gera_vizinho_aleatorio()
        
        return estado

    def selecao(self, e1: Estado, e2: Estado):
        return e1 if e1.custo < e2.custo else e2

    def executa(self):
        # população inicial
        estado_inicial = self.solucao_inicial
        populacao = set(estado_inicial.gera_vizinho_aleatorio() for _ in range(self.tamanho_populacao))
        populacao_sucessora = set()
        passos=0
        for _ in range(self.max_iteracoes):
            # Valida se o melhor estado encontrado está dentro do possível erro estipulado
            melhor_estado = sorted(populacao, key=lambda x: x.custo)[0]
            if self.erro is not None and (-self.erro <= melhor_estado.custo <= self.erro):
                break

            for p in populacao:
                # gera dois vizinhos aleatórios
                estado_vizinho_1 = p.gera_vizinho_aleatorio()
                estado_vizinho_2 = p.gera_vizinho_aleatorio()

                # crossover
                filho_1 = self.reproduz(e1=p, e2=estado_vizinho_1)
                filho_2 = self.reproduz(e1=p, e2=estado_vizinho_2)

                # selecao (torneio)
                filho = self.selecao(filho_1, filho_2)

                # mutacao
                filho = self.mutacao(filho)

                populacao_sucessora.add(filho)

                passos+=1


            populacao = populacao_sucessora.copy()
            populacao_sucessora.clear()

        return melhor_estado, self.coleta_dados()
    
    def coleta_dados(self):
        return self.passos, self.melhor_custo
    
    def limpa_dados(self):
        self.passos.clear()
        self.melhor_custo.clear()
