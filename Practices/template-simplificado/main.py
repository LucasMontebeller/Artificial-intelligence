
import random

from collections import deque
from viewer import MazeViewer
from math import inf, sqrt
import time



def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 25% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.50 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
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

def distancia_manhattan(celula_1, celula_2):
    dx = abs(celula_1.x - celula_2.x)
    dy = abs(celula_1.y - celula_2.y)
    return dx + dy

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

        viewer.update(generated=fronteira,
                      expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    tempo_final = time.time()

    return caminho, custo, expandidos, (tempo_final - tempo_inicial)


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
        proximo_no = None

        # seleciona o primeiro item da pilha
        no_atual = fronteira[-1]

        # verifica se o goal já foi alcançado
        if (no_atual.x == goal.x) and (no_atual.y == goal.y):
            goal_encontrado = no_atual
            break

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # seleciona o proximo no ainda não expandido
        for v in vizinhos:
            if (not esta_contido(expandidos, v)):
                proximo_no = v
                break

        # caso exista entra na pilha
        if (proximo_no is not None):
            fronteira.append(proximo_no)
        else:
            fronteira.pop()

        expandidos.add(no_atual)
        
        viewer.update(generated=fronteira,
                          expanded=expandidos)
        # viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    tempo_final = time.time()

    return caminho, custo, expandidos, (tempo_final - tempo_inicial)


def a_star_search(labirinto, inicio, goal, viewer):
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
        
        # fila com prioridade
        fronteira.sort(key=lambda x: x.custo_total)
        no_atual = fronteira.pop(0)

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # verifica se o goal já foi alcançado
        if (no_atual.x == goal.x) and (no_atual.y == goal.y):
            goal_encontrado = no_atual
            break

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                # f(n) = g(n) + h(n)
                v.custo_total = distancia(v, inicio) + distancia_manhattan(v, goal) 
                fronteira.append(v)

        expandidos.add(no_atual)

        viewer.update(generated=fronteira,
                      expanded=expandidos)
        # viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)
    tempo_final = time.time()

    return caminho, custo, expandidos, (tempo_final - tempo_inicial)



#-------------------------------


def main():

    def _exibe_resultado(algoritmo, caminho, custo_total, expandidos, tempo_gasto):
        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"{algoritmo}:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo total gasto: {tempo_gasto}.\n\n"
        )

    for _ in range(10):
        #SEED = 42  # coloque None no lugar do 42 para deixar aleatorio
        #random.seed(SEED)
        N_LINHAS  = 15
        N_COLUNAS = 15
        INICIO = Celula(y=0, x=0, anterior=None)
        GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None)


        """
        O labirinto sera representado por uma matriz (vizinhos de vizinhoss)
        em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
        """
        labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL)

        viewer = MazeViewer(labirinto, INICIO, GOAL,
                            step_time_miliseconds=20, zoom=40)

        #----------------------------------------
        # BFS Search
        #----------------------------------------
        viewer._figname = "BFS"
        caminho, custo_total, expandidos, tempo_gasto = \
                breadth_first_search(labirinto, INICIO, GOAL, viewer)

        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, tempo_gasto)        

        viewer.update(path=caminho)
        viewer.pause()
        #----------------------------------------
        # DFS Search
        #----------------------------------------
        viewer._figname = "DFS"
        caminho, custo_total, expandidos, tempo_gasto = \
                depth_first_search(labirinto, INICIO, GOAL, viewer)

        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, tempo_gasto)        

        viewer.update(path=caminho)
        viewer.pause()
        #----------------------------------------
        # A-Star Search
        #----------------------------------------
        viewer._figname = "A-Star"
        caminho, custo_total, expandidos, tempo_gasto = \
                a_star_search(labirinto, INICIO, GOAL, viewer)

        _exibe_resultado(viewer._figname, caminho, custo_total, expandidos, tempo_gasto)        

        viewer.update(path=caminho)
        viewer.pause()

        #----------------------------------------
        # Uniform Cost Search (Obs: opcional)
        #----------------------------------------




    print("OK! Pressione alguma tecla pra finalizar...")
    input()


if __name__ == "__main__":
    main()