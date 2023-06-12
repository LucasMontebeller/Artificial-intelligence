import numpy as np

def funcao_rastrgin(x, y):
    return 20 + np.power(x,2) - (10 * np.cos(2 * np.pi * x)) + np.power(y,2) - (10 * np.cos(2 * np.pi * y))

