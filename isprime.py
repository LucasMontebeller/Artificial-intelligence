import numpy as np
import time

# TEOREMA DE VANTIEGHEMS (problema --> overflow no 13)
def is_prime(numero : np.uint64):
    if numero <= 3:
        return True
    
    produtorio = 1
    for i in range(1, numero):
        produtorio *= np.power(2, i) - 1

    if (produtorio - numero) % (np.power(2, numero) - 1) == 0:
        return True
    
    return False

# Força bruta
def is_prime_testing(numero : np.uint64):
    if numero <= 3:
        return True
    
    # se o numero possui algum divisor além dele mesmo e 1, não é primo
    for i in range(2, numero):
        if np.mod(numero, i) == 0:
            return False
    
    return True

# ---------------------
# lista = np.random.randint(1, 1000, size=1000)
lista = np.arange(1, 10_000, dtype=np.uint64)
primos = []

inicio = time.time()
for i in lista:
    if is_prime_testing(i):
        primos.append(i)

print(f'tempo: {time.time() - inicio}, total = {len(primos)}, numeros = {primos}')