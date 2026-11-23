# matriz 18: vector con suma de cada columna de matriz 3x3

print("ingrese elementos de matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

vector_sumas = []
for j in range(3):
    suma_col = 0
    for i in range(3):
        suma_col = suma_col + matriz[i][j]
    vector_sumas.append(suma_col)

print("vector con la suma de las columnas:")
print(vector_sumas)
