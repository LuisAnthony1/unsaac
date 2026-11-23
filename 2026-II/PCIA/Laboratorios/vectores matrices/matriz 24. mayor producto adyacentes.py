# matriz 24: mayor producto de 4 numeros adyacentes en matriz

def mayor_producto_4(m):
    filas = len(m)
    cols = len(m[0])
    max_prod = 0

    # horizontal
    for i in range(filas):
        for j in range(cols - 3):
            p = m[i][j] * m[i][j+1] * m[i][j+2] * m[i][j+3]
            if p > max_prod:
                max_prod = p

    # vertical
    for i in range(filas - 3):
        for j in range(cols):
            p = m[i][j] * m[i+1][j] * m[i+2][j] * m[i+3][j]
            if p > max_prod:
                max_prod = p

    # diagonal principal
    for i in range(filas - 3):
        for j in range(cols - 3):
            p = m[i][j] * m[i+1][j+1] * m[i+2][j+2] * m[i+3][j+3]
            if p > max_prod:
                max_prod = p

    # diagonal secundaria
    for i in range(filas - 3):
        for j in range(3, cols):
            p = m[i][j] * m[i+1][j-1] * m[i+2][j-2] * m[i+3][j-3]
            if p > max_prod:
                max_prod = p

    return max_prod

# ejemplo de matriz pequeña 4x4
m = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]
print("el mayor producto de 4 adyacentes es:", mayor_producto_4(m))
