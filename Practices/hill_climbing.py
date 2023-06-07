import random as rd

def is_diagonal(estado, i, j):
    if abs(estado[i] - estado[j]) == abs(i - j):
        return True
    return False

# funcao objetivo
def calcula_ataques(estado):
    ataques = 0
    for i in range(len(estado)):
        for j in range(i + 1, len(estado)):
            if estado[i] == estado[j] or is_diagonal(estado,i,j):
                ataques+=1 
    
    return ataques

def gera_estado():
    return [rd.randint(1,8) for x in range(8)]

def hill_climbing():
    estado = gera_estado()
    passos=0
    while True:
        passos+=1
        proximo_estado = gera_estado()
        ataques = calcula_ataques(estado)

        # queremos minimizar a funcao objetivo, portanto se o vizinho for maior paramos
        # a desvantagem do hill climbing é que ele provavelmente ficará preso em um minimo ou maximo local
        if (calcula_ataques(proximo_estado)) > ataques:
            break
        
        estado = proximo_estado

    return estado, ataques, passos

# forca bruta
def solucao_exata():
    passos=0
    while True:
        passos+=1
        estado = gera_estado()
        if calcula_ataques(estado) == 0:
            break
    
    return estado, passos


resultado = hill_climbing()
resultado_exato = solucao_exata()
print(f"Hill climbing - \testado: {resultado[0]} \tataques: {resultado[1]} \tpassos: {resultado[2]}")
print(f"Exato - \testado: {resultado_exato[0]} \tataques: {0} \tpassos: {resultado_exato[1]}")