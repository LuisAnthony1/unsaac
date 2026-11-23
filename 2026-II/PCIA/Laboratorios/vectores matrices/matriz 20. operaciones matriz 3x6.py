# matriz 20: operaciones con matriz 3x6 de reales

print("ingrese matriz 3x6 de reales:")
matriz = [[float(input(f"[{i}][{j}]: ")) for j in range(6)] for i in range(3)]

# suma de columnas impares (indices 1, 3, 5)
suma_impares = 0
for i in range(3):
    for j in [1, 3, 5]:
        suma_impares = suma_impares + matriz[i][j]

# media de columnas 2 y 4 (indices 1 y 3)
suma_2_4 = 0
for i in range(3):
    suma_2_4 = suma_2_4 + matriz[i][1] + matriz[i][3]
media_2_4 = suma_2_4 / 6

# columna 6 (indice 5) = columna 1 + columna 2 (indices 0 y 1)
for i in range(3):
    matriz[i][5] = matriz[i][0] + matriz[i][1]

print("suma de columnas impares:", suma_impares)
print("media de columnas 2 y 4:", media_2_4)
print("matriz modificada:")
for f in matriz:
    print(f)
