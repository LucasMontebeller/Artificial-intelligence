import numpy as np
import random as rd

class Estado():

    def __init__(self, x=None, y=None, limite=5.2):
        self.x = x or rd.uniform(-limite, limite)
        self.y = y or rd.uniform(-limite, limite)
        self.funcao_objetivo = self.funcao_rastrgin(self.x, self.y)

    # sigma = desvio padrão
    # ver funcao random.normal
    def gerar_estado(self, sigma=1.2):
        x = self.x + (sigma * np.random.randn())
        y = self.y + (sigma * np.random.randn())

        return Estado(x, y)
    
    @staticmethod
    def funcao_rastrgin(x, y):
        return 20 + np.power(x,2) - (10 * np.cos(2 * np.pi * x)) + np.power(y,2) - (10 * np.cos(2 * np.pi * y))


def genetic_algorithm(tamanho_populacao=20, num_geracoes=100, erro=0.1):

    populacao = set(Estado() for _ in range(tamanho_populacao))
    nova_populacao = set()
    taxa_mutacao = 0.30

    # validar alpha (aleatorio?)
    def reproduz(e1: Estado, e2: Estado, alpha=0.1):
        x = (alpha * e1.x) + (1 - alpha) * e2.x
        y = (alpha * e1.y) + (1 - alpha) * e2.y

        return Estado(x, y)
    
    def mutacao(x: Estado):
        return x.gerar_estado()
    
    def torneio(e: Estado):
        x, y = (e.gerar_estado() for _ in range(2))
        return x if x.funcao_objetivo <= y.funcao_objetivo else y
    
    def selecao(e : Estado):
        x = torneio(e)
        y = torneio(e)
        while x == y:
            y = torneio()

        return x, y

    
    passos=geracoes = 0
    erro = 0.25
    while True:
        geracoes+=1
        melhor_estado = sorted(populacao, key=lambda x: x.funcao_objetivo)[0]
        if -erro <= melhor_estado.funcao_objetivo <= erro or geracoes >= num_geracoes:
            break

        for p in populacao:
            passos+=1

            # selecao --> torneio simples
            x, y = selecao(p)

            # crossover
            filho = reproduz(e1=x, e2=y)

            # mutacao
            if rd.random() < taxa_mutacao:
                mutacao(filho)

            nova_populacao.add(filho)

        populacao = nova_populacao.copy()
        nova_populacao.clear()

    return melhor_estado, geracoes, passos

def main():

    estado, geracoes, passos = genetic_algorithm()
    print(f"Genetic Algorithm - \t(x,y): {estado.x, estado.y} \tfuncao minimizada: {estado.funcao_objetivo} \tgeracoes: {geracoes} \tpassos: {passos}")

if __name__ == '__main__':
    main()