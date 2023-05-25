import numpy as np
from numpy import random
import random
import pandas as pd
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

G_inicial = nx.Graph()

# inicializando manualmente as cidades (vérticies) e
# os respectivos custos entre elas (arestas).

G_inicial.add_weighted_edges_from([
        ("Arad", "Sibiu", 140),
        ("Arad", "Timisoara", 118),
        ("Arad", "Zerind", 75),
        ("Bucharest", "Fagaras", 211),
        ("Bucharest", "Giurgiu", 90),
        ("Bucharest", "Pitesti", 101),
        ("Bucharest", "Urziceni", 85),
        ("Craiova", "Dobreta", 120),
        ("Craiova", "Pitesti", 138),
        ("Craiova", "Rimnicu_Vilcea", 146),
        ("Dobreta", "Mehadia", 75),
        ("Eforie", "Hirsova", 86),
        ("Fagaras", "Sibiu", 99),
        ("Hirsova", "Urziceni", 98),
        ("Iasi", "Neamt", 87),
        ("Iasi", "Vaslui", 92),
        ("Lugoj", "Mehadia", 70),
        ("Lugoj", "Timisoara", 111),
        ("Oradea", "Zerind", 71),
        ("Oradea", "Sibiu", 151),
        ("Pitesti", "Rimnicu_Vilcea", 97),
        ("Rimnicu_Vilcea", "Sibiu", 80),
        ("Urziceni", "Vaslui", 142)
    ])


Estimation = {
        "Arad": 366,
        "Bucharest": 0,
        "Craiova": 160,
        "Dobreta": 242,
        "Eforie": 161,
        "Fagaras": 178,
        "Giurgiu": 77,
        "Hirsova": 151,
        "Iasi": 226,
        "Lugoj": 244,
        "Mehadia": 241,
        "Neamt": 234,
        "Oradea": 380,
        "Pitesti": 98,
        "Rimnicu_Vilcea": 193,
        "Sibiu": 253,
        "Timisoara": 329,
        "Urziceni": 80,
        "Vaslui": 199,
        "Zerind": 374
}

# Calcula custo total de um caminho
def calcula_custo_caminho(G, caminho):
    custo = 0.0
    for i in range(len(caminho)-1):
        u, v = caminho[i], caminho[i+1]
        custo += G[u][v]['weight']
    return custo

# calcula custo do caminho da cidade origem até a cidade atual
def calcula_custo_g(G, caminho_origem_atual):
    return calcula_custo_caminho(G, caminho_origem_atual)

# No futuro, a funcao abaixo será substituída apropriadamente
# para os cálculos das estimativas euclidianas
def estima_custo_h(cidade_atual):
    # destino == 'Bucharest':
    return Estimation[cidade_atual]

def caminho_minimo(G, s, t):

    L = [t]
    u = t
    while u != s:
        u = G.nodes[u]['pre']
        L.append(u)

    L.reverse()

    return L

# Algoritmos

def UCS(G_inicial, s, destino):
    G = G_inicial.copy()

    # INICIALIZACAO
    for v in G.nodes() - {s}:
        G.nodes[v]['cor'] = 'branco'
        G.nodes[v]['dis'] = np.inf
        G.nodes[v]['pre'] = None

    G.nodes[s]['cor'] = 'cinza'
    G.nodes[s]['dis'] = 0
    G.nodes[s]['pre'] = None

    # Fila (append (right), popleft)
    Q = deque()
    Q.append(s)
    while True:
        # fila com prioridade
        Q = deque(sorted(Q, key=lambda x: G.nodes[x]['dis']))
        u = Q.popleft()

        if u == destino:
            break

        for v in G.neighbors(u):
            distancia = G.nodes[u]['dis'] + calcula_custo_g(G, [u, v])

            if G.nodes[v]['cor'] == 'branco':
                G.nodes[v]['cor'] = 'cinza'
                G.nodes[v]['dis'] = distancia
                G.nodes[v]['pre'] = u
                Q.append(v)

            # Caso o nó já tenha sido visitado, mas a distância pelo caminho atual é menor, efetua-se a troca
            elif G.nodes[v]['cor'] == 'cinza' and distancia < G.nodes[v]['dis']:
                G.nodes[v]['dis'] = distancia
                G.nodes[v]['pre'] = u


        G.nodes[u]['cor'] = 'preto'

        # print(u, G.nodes[u]['dis'], G.nodes[u]['cor'])

    # Grafo G retornado contem as informações de distância
    # e cores desde o nó origem a todos os demais nós
    return G


def main():
    ORIGEM = 'Arad'
    DESTINO = 'Bucharest'

    # UCS
    G = UCS(G_inicial, ORIGEM, DESTINO)
    caminho = caminho_minimo(G, ORIGEM, DESTINO)
    custo = calcula_custo_caminho(G, caminho)
    
    print(f'Custo: {custo}\t->\tCaminho: {caminho}')

    # A-star

    nx.draw(G_inicial, with_labels=True)
    plt.show()

if __name__ == "__main__":
    main()