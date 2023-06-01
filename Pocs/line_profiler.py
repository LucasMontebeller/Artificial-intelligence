import line_profiler
import random as rd

def selection_sort(list):
    for i in range(len(list)):
        lower = list[i]
        troca = i
        for j in range(i + 1, len(list)):
            if list[j] < lower:
                lower = list[j]
                troca = j

        list[troca] = list[i]
        list[i] = lower
    return list

random_list = [rd.randint(0, 10000) for x in range(0,10000)]

if __name__ == '__main__':
    # Criação do profiler
    profiler = line_profiler.LineProfiler()

    # Adiciona a função ao profiler
    profiler.add_function(selection_sort)

    # Executa o código a ser analisado
    profiler.enable_by_count()
    selection_sort(random_list)
    profiler.disable_by_count()

    # Imprime o resultado da análise
    profiler.print_stats()
