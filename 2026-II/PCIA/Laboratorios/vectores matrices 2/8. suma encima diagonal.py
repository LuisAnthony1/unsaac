# ejercicio 8: suma de elementos encima de la diagonal principal

def suma_encima_diagonal(matriz):
    suma = 0
    for i in range(3):
        for j in range(3):
            if j > i:
                suma = suma + matriz[i][j]
    return suma

print("ingrese elementos de la matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

resultado = suma_encima_diagonal(matriz)
print("la suma de elementos encima de la diagonal es:", resultado)
