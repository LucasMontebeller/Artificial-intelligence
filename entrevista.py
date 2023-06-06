def is_palidrome(numero):

    numero = str(numero)
    numero_list = [int(x) for x in numero]
    numero_list_copy = numero_list.copy()

    numero_list_reversed = []
    while numero_list_copy:
        numero_atual = numero_list_copy.pop()
        numero_list_reversed.append(numero_atual)

    return numero_list == numero_list_reversed
    

print(is_palidrome(155676551))