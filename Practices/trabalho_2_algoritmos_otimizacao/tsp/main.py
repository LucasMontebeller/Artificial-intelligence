from tsp import gera_coordenadas_aleatorias, gera_problema_tsp, plota_rotas
from algoritmos import Hill_Climbing, Hill_Climbing_Restart, Simulating_Anneling, Genetic_Algorithm, Forca_Bruta
import numpy as np

# Validar possibilidade de execução multi-threading
def executa_algoritmos(algoritmos: set(), n_vezes: int):
    for x in algoritmos:
        melhores_estados = []
        print(f'### Executando algoritmo {x.__class__.__name__} ###\n')
        for _ in range(n_vezes):
            estado = x.executa()
            print(f'{estado.custo:7.3f}, {estado.solucao}')
            melhores_estados.append(estado)

        # Ordena as soluções pelo custo em ordem crescente
        
        melhor_estado = sorted(melhores_estados, key=lambda x: x.custo)[0]

        print(f'\n \033[32mMelhor solução: {melhor_estado.custo:7.3f}, {melhor_estado.solucao}\033[0m')
        print('-' * 100)

def main():
    # Simula a criação de N cidades
    # com suas respectivas distâncias
    n_cidades=10
    df_coordenadas = gera_coordenadas_aleatorias(n_cidades)

    tsp = gera_problema_tsp(df_coordenadas)

    solucao_inicial = ['A'+str(i) for i in range(n_cidades)]
    # plota_rotas(df_coordenadas, solucao_inicial)

    # Executa os algoritmos
    print('')
    algoritmos = {
        Hill_Climbing(tsp, solucao_inicial),
        Hill_Climbing_Restart(tsp, solucao_inicial, 15), 
        Simulating_Anneling(tsp, solucao_inicial, temperatura=10, taxa_resfriamento=0.995),
        Genetic_Algorithm(tsp, solucao_inicial, max_iteracoes=500, taxa_mutacao=0.20, tamanho_populacao=15),
        Forca_Bruta(tsp)
    }
    executa_algoritmos(algoritmos, 10)

    
if __name__ == '__main__':
    main()