# ejercicio 10: vector con la suma de cada columna de matriz 3x3

def suma_columnas(matriz):
    vector = []
    for j in range(3):
        suma_col = 0
        for i in range(3):
            suma_col = suma_col + matriz[i][j]
        vector.append(suma_col)
    return vector

print("ingrese matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

resultado = suma_columnas(matriz)
print("vector con la suma de cada columna:")
print(resultado)
