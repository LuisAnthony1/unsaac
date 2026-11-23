# matriz 25: determinar proxima jugada en tres en raya (michi)

def proxima_jugada(tablero):
    # buscar casilla vacia (0) para ganar o bloquear
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == 0:
                return i, j
    return None

tablero = [
    [-1, 1, 1],
    [-1, -1, 0],
    [0, 1, 0]
]

jugada = proxima_jugada(tablero)
if jugada is not None:
    print(f"proxima jugada en fila {jugada[0]} columna {jugada[1]}")
else:
    print("el tablero esta lleno")
