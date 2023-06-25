from tsp import gera_coordenadas_aleatorias, gera_problema_tsp, plota_rotas, boxplot_sorted, executa_n_vezes
from algoritmos import Hill_Climbing, Hill_Climbing_Restart, Simulating_Anneling, Genetic_Algorithm, Forca_Bruta

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
        Hill_Climbing_Restart(tsp, solucao_inicial, 500), 
        Simulating_Anneling(tsp, solucao_inicial, temperatura=10, taxa_resfriamento=0.995),
        Genetic_Algorithm(tsp, solucao_inicial, max_iteracoes=500, taxa_mutacao=0.20, tamanho_populacao=15),
        Forca_Bruta(tsp)
    }

    df_custo, estatisticas = executa_n_vezes(algoritmos, 10)
    print('### Estatisticas ###')
    print(estatisticas)
    boxplot_sorted(df_custo, rot=90, figsize=(8,6), fontsize=12)
    
if __name__ == '__main__':
    main()