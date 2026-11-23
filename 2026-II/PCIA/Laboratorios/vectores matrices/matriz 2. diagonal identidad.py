# matriz 2: matriz 5x5 con 1 en diagonal principal y 0 en resto

matriz = []
for i in range(5):
    fila = []
    for j in range(5):
        if i == j:
            fila.append(1)
        else:
            fila.append(0)
    matriz.append(fila)

print("matriz resultante:")
for fila in matriz:
    print(fila)
