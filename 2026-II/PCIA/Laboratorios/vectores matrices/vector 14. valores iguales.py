# vector 14: verificar si existen valores iguales

vector = []
print("ingrese 10 numeros:")
for i in range(10):
    vector.append(int(input(f"posicion {i}: ")))

repetidos = []
for i in range(len(vector)):
    for j in range(i + 1, len(vector)):
        if vector[i] == vector[j] and vector[i] not in repetidos:
            repetidos.append(vector[i])

if len(repetidos) > 0:
    print("valores repetidos encontrados:", repetidos)
else:
    print("no existen valores iguales")
