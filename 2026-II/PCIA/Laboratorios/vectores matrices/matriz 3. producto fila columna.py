# matriz 3: matriz 4x4 con producto del valor de fila y columna

matriz = []
for i in range(4):
    fila = []
    for j in range(4):
        fila.append(i * j)
    matriz.append(fila)

print("matriz 4x4 con i * j:")
for fila in matriz:
    print(fila)
