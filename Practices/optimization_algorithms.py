import random as rd
import numpy as np
from enum import Enum, auto

class Selecao(Enum):
    TORNEIO = auto()
    PONDERADA = auto()

class Estado():

    def __init__(self, distribuicao=None):
        self.distribuicao = distribuicao or self.gerar_estado()
        self.ataques = self.calcula_ataques()

    @staticmethod
    def gerar_estado():
        return rd.sample(range(8), 8)
    
    def eh_diagonal(self, i, j):
        if abs(self.distribuicao[i] - self.distribuicao[j]) == abs(i - j):
            return True
        return False
    
    # funcao objetivo(fitness)
    def calcula_ataques(self):
        ataques = 0
        for i in range(len(self.distribuicao)):
            for j in range(i + 1, len(self.distribuicao)):
                if self.distribuicao[i] == self.distribuicao[j] or self.eh_diagonal(i,j):
                    ataques+=1 
        
        return ataques



# ------------------------------------------------- Algoritmos De Otimização
def hill_climbing():
    estado = Estado()
    passos=0
    while True:
        passos+=1
        proximo_estado = Estado()

        # queremos minimizar a funcao objetivo, portanto se o vizinho for maior paramos
        # a desvantagem do hill climbing é que ele provavelmente ficará preso em um minimo ou maximo local
        if (proximo_estado.ataques) > estado.ataques:
            break
        
        estado = proximo_estado

    return estado, passos


def simulating_annealing(iteracoes, temperatura, taxa_resfriamento=0.95):
    estado = Estado()
    passos = 0
    for _ in range(iteracoes):
        if estado.ataques == 0 or np.round(temperatura, 2) == 0:
            break

        passos+=1
        temperatura*=taxa_resfriamento
        proximo_estado = Estado()
        
        delta_E = proximo_estado.ataques - estado.ataques
        # valida se o estado vizinho é melhor em relação ao fitness ou troca para um outro com probabilidade ~ Temperatura
        if (delta_E < 0): # or (delta_E > 0 and rd.random() < np.exp(delta_E/temperatura)):
            estado = proximo_estado
        elif (rd.random() < np.exp(-delta_E/temperatura)):
            estado = proximo_estado

    return estado, passos

def genetic_algorithm(selecao: Selecao):
    # inicial
    populacao = set(Estado() for x in range(10))
    nova_populacao = set()
    taxa_mutacao = 0.30

    def reproduz(x: Estado, y: Estado):
        corte = rd.randint(0, len(x.distribuicao))
        distribuicao = x.distribuicao[:corte]
        distribuicao.extend(y.distribuicao[corte:])

        return Estado(distribuicao)
    
    def mutacao(x: Estado):
        corte = rd.randint(0, len(x.distribuicao) - 1)
        x.distribuicao[corte] = rd.randint(0,8)

        return x
    
    def selecao_ponderada(populacao):
        pesos = [np.exp(-x.ataques/2) for x in populacao]
        return rd.choices(list(populacao), weights=pesos, k=1)
    
    def selecao_torneio():
        x, y = rd.choices(list(populacao), k=2)
        return x if x.ataques <= y.ataques else y
    
    passos = 0
    while True:
        melhor_estado = sorted(populacao, key=lambda x: x.ataques)[0]
        if melhor_estado.ataques == 0 or passos == 5000:
            break

        for _ in populacao:
            passos+=1

            # selecao
            if selecao.value == Selecao.PONDERADA:
                x = selecao_ponderada(populacao)
                y = selecao_ponderada(populacao - set(x))
            else:
                x = selecao_torneio()
                y = selecao_torneio()
                while x == y:
                    y = selecao_torneio()


            # crossover
            filho = reproduz(x[0], y[0]) if selecao.value == Selecao.PONDERADA else reproduz(x, y)

            # mutacao
            if rd.random() < taxa_mutacao:
                mutacao(filho)

            nova_populacao.add(filho)

        populacao = nova_populacao.copy()
        nova_populacao.clear()

    return melhor_estado, passos


# forca bruta
def solucao_exata():
    passos=0
    while True:
        passos+=1
        estado = Estado()
        if estado.ataques == 0:
            break
    
    return estado, passos

def main():
    estado, passos = hill_climbing()    
    print(f"Hill climbing - \testado: {estado.distribuicao} \tataques: {estado.ataques} \tpassos: {passos}")

    estado, passos = simulating_annealing(iteracoes=1000, temperatura=100)
    print(f"Simulating annealing - \testado: {estado.distribuicao} \tataques: {estado.ataques} \tpassos: {passos}")

    estado, passos = genetic_algorithm(Selecao.TORNEIO)
    print(f"Genetic Algorithm - \testado: {estado.distribuicao} \tataques: {estado.ataques} \tpassos: {passos}")

    estado, passos = solucao_exata() 
    print(f"Solução exata - \testado: {estado.distribuicao} \tataques: {estado.ataques} \tpassos: {passos}")

if __name__ == '__main__':
    main()