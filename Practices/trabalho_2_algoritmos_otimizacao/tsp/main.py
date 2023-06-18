from tsp import gera_coordenadas_aleatorias, gera_problema_tsp, plota_rotas
from algoritmos import Hill_Climbing, Simulating_Anneling, Genetic_Algorithm

# Validar possibilidade de execução multi-threading
def executa_algoritmos(algoritmos: set(), n_vezes: int):
    for x in algoritmos:
        melhores_solucoes = []
        print(f'### Executando algoritmo {x.__class__.__name__} ###\n')
        for _ in range(n_vezes):
            custo, solucao = x.executa()
            print(f'{custo:7.3f}, {solucao}')
            melhores_solucoes.append((custo, solucao))

        # Ordena as soluções pelo custo em ordem crescente
        melhores_solucoes.sort(key=lambda s: s[0])
        melhor_custo, melhor_solucao = melhores_solucoes[0]

        print(f'\n \033[32mMelhor solução: {melhor_custo:7.3f}, {melhor_solucao}\033[0m')
        print('-' * 100)

def main():
    # Simula a criação de N cidades
    # com suas respectivas distâncias
    n_cidades=10
    df_coordenadas = gera_coordenadas_aleatorias(n_cidades)

    tsp = gera_problema_tsp(df_coordenadas)

    # solucao_inicial = ['A'+str(i) for i in range(n_cidades)]
    # plota_rotas(df_coordenadas, solucao_inicial)

    # Executa os algoritmos
    print('')
    algoritmos = {
        # Hill_Climbing(tsp), 
        # Simulating_Anneling(tsp, temperatura=5000, taxa_resfriamento=0.995, max_iteracoes=50),
        Genetic_Algorithm(tsp)
    }
    executa_algoritmos(algoritmos, 10)

    
if __name__ == '__main__':
    main()