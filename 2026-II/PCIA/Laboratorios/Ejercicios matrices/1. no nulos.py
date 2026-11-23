# ejercicio 1: contar posiciones no nulas en matriz 10x10

def contar_no_nulos(matriz):
    contador = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] != 0:
                contador = contador + 1
    return contador

matriz = []
print("ingrese datos para matriz 10x10:")
for i in range(10):
    fila = []
    for j in range(10):
        valor = int(input(f"posicion [{i}][{j}]: "))
        fila.append(valor)
    matriz.append(fila)

total = contar_no_nulos(matriz)
print("cantidad de posiciones no nulas:", total)
