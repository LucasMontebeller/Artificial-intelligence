import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import copy

### EXIBICAO ### --> baseado nos metodos fornecidos pelo professor no colab
# Os metodos criados aqui serão utilizados tanto pelo TSP quanto função de Rastringin

# Cria DataFrame para armazenar os resultados dos custos
def cria_df_custos(algoritmos, n_vezes):
    nomes_algoritmos = [algoritmo.__class__.__name__ for algoritmo in algoritmos]
    df_results = pd.DataFrame(index=nomes_algoritmos, columns=range(n_vezes))
    df_results.index.name = 'ALGORITMO'
    return df_results

# Executa os algoritmos N vezes e registra os custos
def executa_n_vezes(algoritmos, n_vezes, problema='TSP'):
    df_custo = cria_df_custos(algoritmos, n_vezes)
    estatisticas = pd.DataFrame(index=['min', 'max', '50%', 'std'], columns=[algoritmo.__class__.__name__ for algoritmo in algoritmos])
    graficos = {}

    for algoritmo in algoritmos:
        melhores_estados = []
        dados_evolucao = {}
        nome = algoritmo.__class__.__name__
        
        print(f'### Executando algoritmo {nome} ###\n')
        for i in range(n_vezes):
            estado, dados = algoritmo.executa()
            melhores_estados.append(estado)
            dados_evolucao[estado] = copy.deepcopy(dados)

            # Exibição parcial dos dados
            if problema == 'TSP':
                print(f'{estado.custo:7.3f}, {estado.solucao}')
            else:
                print(f'{estado.custo:7.3f}, {(estado.x, estado.y)}')

            # atualiza data frame
            df_custo.loc[nome, i] = estado.custo

        # Ordena as soluções pelo custo em ordem crescente
        melhor_estado = sorted(melhores_estados, key=lambda x: x.custo)[0]
        # Salva o gráfico da função do fitness que será exibido
        graficos[nome] = dados_evolucao[melhor_estado]

        if problema == 'TSP':
            print(f'\n \033[32mMelhor solução: {melhor_estado.custo:7.3f}, {melhor_estado.solucao}\033[0m')
        else:
            print(f'\n \033[32mMelhor solução: {melhor_estado.custo:7.3f}, {(estado.x, estado.y)}\033[0m')
        print('-' * 100)

        # Cálculo das estatísticas
        estatisticas.loc['min', nome] = df_custo.loc[nome].min()
        estatisticas.loc['max', nome] = df_custo.loc[nome].max()
        estatisticas.loc['50%', nome] = df_custo.loc[nome].median()
        estatisticas.loc['std', nome] = df_custo.loc[nome].std()


    df_custo = df_custo.astype(float)
    return df_custo, estatisticas, graficos

def boxplot_sorted(df, rot=90, figsize=(10,6), fontsize=10):
    df2 = df.T
    meds = df2.median().sort_values(ascending=False)
    axes = df2[meds.index].boxplot(figsize=figsize, rot=rot, fontsize=fontsize,
                                   boxprops=dict(linewidth=4, color='cornflowerblue'),
                                   whiskerprops=dict(linewidth=4, color='cornflowerblue'),
                                   medianprops=dict(linewidth=4, color='firebrick'),
                                   capprops=dict(linewidth=4, color='cornflowerblue'),
                                   flierprops=dict(marker='o', markerfacecolor='dimgray',
                                        markersize=12, markeredgecolor='black'),
                                   return_type="axes")

    axes.set_title("Cost of Algorithms", fontsize=fontsize)
    plt.tight_layout()
    plt.show()

def plota_graficos(dados: dict):

    for algoritmo, dados_algoritmo in dados.items():
        sns.lineplot(x=dados_algoritmo[0], y=dados_algoritmo[1], label=algoritmo)

    plt.title('Evolução da Função Objetivo')
    plt.xlabel('Passos (escala logaritmica)')
    plt.ylabel('Custo')
    plt.xscale('log')
    plt.show()