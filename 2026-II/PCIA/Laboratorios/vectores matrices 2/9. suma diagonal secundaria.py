# ejercicio 9: suma de elementos de la diagonal secundaria 3x3

def suma_diagonal_secundaria(matriz):
    suma = 0
    for i in range(3):
        suma = suma + matriz[i][2 - i]
    return suma

print("ingrese datos de la matriz 3x3:")
matriz = [[int(input(f"[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

resultado = suma_diagonal_secundaria(matriz)
print("la suma de la diagonal secundaria es:", resultado)
