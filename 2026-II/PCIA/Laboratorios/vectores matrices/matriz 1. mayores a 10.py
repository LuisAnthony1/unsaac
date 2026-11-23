# matriz 1: contar cuantos valores mayores que 10 tiene una matriz 4x4

matriz = []
print("ingrese datos para matriz 4x4:")
for i in range(4):
    fila = []
    for j in range(4):
        fila.append(int(input(f"posicion [{i}][{j}]: ")))
    matriz.append(fila)

contador = 0
for i in range(4):
    for j in range(4):
        if matriz[i][j] > 10:
            contador = contador + 1

print("cantidad de valores mayores a 10:", contador)
