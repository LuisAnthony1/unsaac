# ejercicio 3: media de diagonal secundaria en matriz 10x10

def media_secundaria(matriz):
    n = len(matriz)
    suma = 0
    for i in range(n):
        suma = suma + matriz[i][n - 1 - i]
    return suma / n

matriz = []
print("ingrese datos para matriz 10x10:")
for i in range(10):
    fila = []
    for j in range(10):
        valor = int(input(f"posicion [{i}][{j}]: "))
        fila.append(valor)
    matriz.append(fila)

promedio = media_secundaria(matriz)
print("media de la diagonal secundaria:", promedio)
