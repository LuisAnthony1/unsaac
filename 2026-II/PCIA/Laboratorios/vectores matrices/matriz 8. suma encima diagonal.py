# matriz 8: suma de elementos encima de la diagonal principal 3x3

print("ingrese datos de la matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

suma = 0
for i in range(3):
    for j in range(3):
        if j > i:
            suma = suma + matriz[i][j]

print("la suma de elementos encima de la diagonal es:", suma)
