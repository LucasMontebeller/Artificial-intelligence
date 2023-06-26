import sys
import os

# Necessário para importar corretamente o arquivo exibe_problemas
diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(diretorio_pai)

from algoritmos import Estado, Hill_Climbing, Hill_Climbing_Restart, Simulated_Annealing, Genetic_Algorithm
from exibe_problemas import boxplot_sorted, executa_n_vezes, plota_graficos

def main():

    # Gera um estado inicia, que será o mesmo para todos os algoritmos
    solucao_inicial = Estado()

    # Executa os algoritmos
    print('')
    algoritmos = {
        Hill_Climbing(solucao_inicial),
        Hill_Climbing_Restart(solucao_inicial, 1000),
        Simulated_Annealing(solucao_inicial, temperatura=100, taxa_resfriamento=0.995),
        Genetic_Algorithm(solucao_inicial, max_iteracoes=50, taxa_mutacao=0.30, tamanho_populacao=20),
        # Forca_Bruta(tsp)
    }

    df_custo, estatisticas, dados = executa_n_vezes(algoritmos, 10, problema="Rastringin")
    print('### Estatisticas ###')
    print(estatisticas)
    boxplot_sorted(df_custo, rot=90, figsize=(8,6), fontsize=12)
    plota_graficos(dados)
    
if __name__ == '__main__':
    main()