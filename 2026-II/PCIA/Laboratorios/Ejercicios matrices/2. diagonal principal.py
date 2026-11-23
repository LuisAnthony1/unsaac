# ejercicio 2: diagonal principal de matriz 6x6

def obtener_diagonal(matriz):
    vector = []
    for i in range(len(matriz)):
        vector.append(matriz[i][i])
    return vector

matriz = []
print("ingrese datos para matriz 6x6:")
for i in range(6):
    fila = []
    for j in range(6):
        valor = int(input(f"posicion [{i}][{j}]: "))
        fila.append(valor)
    matriz.append(fila)

diagonal = obtener_diagonal(matriz)
print("vector con diagonal principal:")
print(diagonal)
