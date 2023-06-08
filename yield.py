import time 
SIZE_LIST = int(1e8)

def list_generator():
    lista = []
    for i in range(SIZE_LIST):
        lista.append(i)

    return lista

def list_generator_w_yield():
    for i in range(SIZE_LIST):
        yield i

tempo_inicial = time.time()
for i in list_generator():
    if i == 1000:
        break
tempo_final = time.time()
print(f"Tempo gasto sem yield: {tempo_final - tempo_inicial}")

print('-' * 100)

tempo_inicial = time.time()
for i in list_generator_w_yield():
    if i == 1000:
        break
tempo_final = time.time()
print(f"Tempo gasto com yield: {tempo_final - tempo_inicial}")