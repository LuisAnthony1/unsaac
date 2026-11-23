# matriz 4: localizar el mayor elemento en matriz 4x4

matriz = []
print("ingrese datos de matriz 4x4:")
for i in range(4):
    fila = []
    for j in range(4):
        fila.append(int(input(f"posicion [{i}][{j}]: ")))
    matriz.append(fila)

mayor = matriz[0][0]
pos_fila = 0
pos_col = 0

for i in range(4):
    for j in range(4):
        if matriz[i][j] > mayor:
            mayor = matriz[i][j]
            pos_fila = i
            pos_col = j

print("matriz:")
for f in matriz:
    print(f)

print(f"el mayor valor es {mayor} en la fila {pos_fila} y columna {pos_col}")
