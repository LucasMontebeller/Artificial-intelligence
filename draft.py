import random as rd
import numpy as np

distribuicao = [8, 2, 1, 3, 8, 6, 2, 5]

def calcula_distancia(x_1, x_2, y_1, y_2):
    delta_x = np.abs(x_2 - x_1)
    delta_y = np.abs(y_2 - y_1)

    return np.sqrt(delta_x**2 + delta_y**2)

def is_diagonal(i, j):
    # if (distribuicao[i] + i == distribuicao[j] + j) or (distribuicao[i] - i == distribuicao[j] - j):
    if round(calcula_distancia(i, j, distribuicao[i], distribuicao[j]) / np.sqrt(2), 10).is_integer():
        return True
    return False

ataques = 0
for i in range(len(distribuicao)):
    for j in range(i + 1, len(distribuicao)):
        if distribuicao[i] == distribuicao[j] or is_diagonal(i,j):
            ataques+=1 

print(ataques)