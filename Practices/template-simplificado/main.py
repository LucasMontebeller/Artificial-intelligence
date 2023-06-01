
import random

from collections import deque
from viewer import MazeViewer
from math import inf, sqrt
import time
import numpy as np



def gera_labirinto(n_linhas, n_colunas, inicio, goal, percentual_bloqueio=0.50):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que (percentual_bloqueio)% do labirinto esteja ocupado
    numero_de_obstaculos = int(percentual_bloqueio * n_linhas * n_colunas)
    while np.count_nonzero(labirinto) < numero_de_obstaculos:
        linha = random.randint(0, n_linhas-1)
        coluna = random.randint(0, n_colunas-1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto


class Celula:
    def __init__(self, y, x, anterior, custo_total=0):
        self.y = y
        self.x = x
        self.anterior = anterior
        self.custo_total = custo_total


def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto):
    # generate neighbors of the current state
    vizinhos = [
        Celula(y=celula_atual.y-1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+1, anterior=celula_atual),
    ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


def breadth_first_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.popleft()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    gerados = expandidos.union(set(fronteira))
    tempo_final = time.time()

    return caminho, custo, expandidos, gerados, (tempo_final - tempo_inicial)


def depth_first_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o primeiro item da pilha
        no_atual = fronteira.pop()

        # verifica se o goal foi alcançado
        if (no_atual.x == goal.x) and (no_atual.y == goal.y):
            goal_encontrado = no_atual
            break

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # seleciona os vizinhos proximos que ainda não foram expandidos e que não estejam na fronteira, ordenando-os de forma aleatória.
        vizinhos_acessiveis= [v for v in vizinhos if not esta_contido(expandidos, v) and not esta_contido(fronteira, v)]
        random.shuffle(vizinhos_acessiveis)
        for v in vizinhos_acessiveis:
            fronteira.append(v)

        expandidos.add(no_atual)
        
        # viewer.update(generated=fronteira,
        #                   expanded=expandidos)
        # viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    gerados = expandidos.union(set(fronteira))
    tempo_final = time.time()

    return caminho, custo, expandidos, gerados, (tempo_final - tempo_inicial)


def a_star_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = list()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    inicio.custo_total = distancia(inicio, goal)
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):
        
        # fila com prioridade, encontrando o no com menor custo.
        fronteira.sort(key=lambda x: x.custo_total)
        no_atual = fronteira.pop(0)

        # verifica se o goal já foi alcançado
        if (no_atual.x == goal.x) and (no_atual.y == goal.y):
            goal_encontrado = no_atual
            break

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # seleciona os nos vizinhos que ainda não foram expandidos
        vizinhos_acessiveis = [v for v in vizinhos if not esta_contido(expandidos, v)]
        for v in vizinhos_acessiveis:
            # f(n) = g(n) + h(n)
            custo_total = custo_caminho(obtem_caminho(v)) + distancia(v, goal) 
            v.custo_total = custo_total

            # adiciona os que ainda não estão na fronteira
            if (not esta_contido(fronteira, v)):
                fronteira.append(v)

            # para os que já estão, valida se o custo atual é menor e caso positivo, efetua-se a troca.
            else:
                indice, celula_fronteira = [(indice, celula) for indice, celula in enumerate(fronteira) if celula.x == v.x and celula.y == v.y][0]
                if custo_total < celula_fronteira.custo_total:
                    fronteira[indice] = v

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        # viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    gerados = expandidos.union(set(fronteira))
    tempo_final = time.time()

    return caminho, custo, expandidos, gerados, (tempo_final - tempo_inicial)

def uniform_cost_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = list()

    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):
        
        # fila com prioridade, encontrando o no com menor custo.
        fronteira.sort(key=lambda x: x.custo_total)
        no_atual = fronteira.pop(0)

        # verifica se o goal já foi alcançado
        if (no_atual.x == goal.x) and (no_atual.y == goal.y):
            goal_encontrado = no_atual
            break

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # seleciona os nos vizinhos que ainda não foram expandidos
        vizinhos_acessiveis = [v for v in vizinhos if not esta_contido(expandidos, v)]
        for v in vizinhos_acessiveis:
            # f(n) = g(n)
            custo_total = custo_caminho(obtem_caminho(v))
            v.custo_total = custo_total

            # adiciona os que ainda não estão na fronteira
            if (not esta_contido(fronteira, v)):
                fronteira.append(v)

            # para os que já estão, valida se o custo atual é menor e caso positivo, efetua-se a troca.
            else:
                indice, celula_fronteira = [(indice, celula) for indice, celula in enumerate(fronteira) if celula.x == v.x and celula.y == v.y][0]
                if custo_total < celula_fronteira.custo_total:
                    fronteira[indice] = v

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        # viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    gerados = expandidos.union(set(fronteira))
    tempo_final = time.time()

    return caminho, custo, expandidos, gerados, (tempo_final - tempo_inicial)



#-------------------------------


def main():

    def _exibe_resultado(algoritmo, caminho, custo_total, expandidos, gerados, tempo_gasto):
        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"{algoritmo}:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tTamanho do caminho (quadrados percorridos): {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tNumero total de nos gerados: {len(gerados)}.\n"
            f"\tTempo total gasto: {tempo_gasto}.\n\n"
        )

    for i in range(1): #range(10)
        print(f"Iteração {i}\n")
        SEED = 42  # coloque None no lugar do 42 para deixar aleatorio
        random.seed(SEED)
        N_LINHAS  = 300
        N_COLUNAS = 300
        INICIO = Celula(y=0, x=0, anterior=None)
        GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None)
        PERCENTUAL_BLOQUEIO = 0.50


        """
        O labirinto sera representado por uma matriz (vizinhos de vizinhoss)
        em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
        """
        labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL, PERCENTUAL_BLOQUEIO)

        viewer = MazeViewer(labirinto, INICIO, GOAL,
                            step_time_miliseconds=50, zoom=3)

        #----------------------------------------
        # BFS Search
        #----------------------------------------
        viewer._figname = "BFS"
        caminho, custo_total, expandidos, gerados, tempo_gasto = \
                breadth_first_search(labirinto, INICIO, GOAL, viewer)
        
        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, gerados, tempo_gasto)        

        # viewer.update(path=caminho)
        # viewer.pause()
        #----------------------------------------
        # DFS Search
        #----------------------------------------
        viewer._figname = "DFS"
        caminho, custo_total, expandidos, gerados, tempo_gasto = \
                depth_first_search(labirinto, INICIO, GOAL, viewer)

        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, gerados, tempo_gasto)        

        # viewer.update(path=caminho)
        # viewer.pause()
        #----------------------------------------
        # A-Star Search
        #----------------------------------------
        viewer._figname = "A-Star"
        caminho, custo_total, expandidos, gerados, tempo_gasto = \
                a_star_search(labirinto, INICIO, GOAL, viewer)

        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, gerados, tempo_gasto)        

        # viewer.update(path=caminho)
        # viewer.pause()

        #----------------------------------------
        # Uniform Cost Search (Obs: opcional)
        #----------------------------------------
        viewer._figname = "UCS"
        caminho, custo_total, expandidos, gerados, tempo_gasto = \
                uniform_cost_search(labirinto, INICIO, GOAL, viewer)

        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, gerados, tempo_gasto)        

        viewer.update(path=caminho)
        viewer.pause()
        print('-' * 100)



    print("OK! Pressione alguma tecla pra finalizar...")
    input()


if __name__ == "__main__":
    main()
