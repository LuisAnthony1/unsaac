# ejercicio 13: contar bombas alrededor de una posicion

bomba = -1

def contar_bombas(matriz, lin, col):
    filas = len(matriz)
    columnas = len(matriz[0])
    contador = 0
    
    for i in range(lin - 1, lin + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < filas and 0 <= j < columnas:
                if (i != lin or j != col) and matriz[i][j] == bomba:
                    contador = contador + 1
                    
    return contador

tablero = [
    [0, -1, 0],
    [-1, 0, 0],
    [0, 0, -1]
]
print(tablero)
fila = int(input("ingrese fila (0 a 2): "))
columna = int(input("ingrese columna (0 a 2): "))

total = contar_bombas(tablero, fila, columna)
print("cantidad de bombas alrededor:", total)
