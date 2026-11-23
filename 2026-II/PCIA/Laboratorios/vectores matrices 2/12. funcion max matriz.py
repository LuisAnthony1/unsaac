# ejercicio 12: funcion max que retorna k, lin, col

def max_matriz(a):
    k = a[0][0]
    lin = 0
    col = 0
    for i in range(3):
        for j in range(3):
            if a[i][j] > k:
                k = a[i][j]
                lin = i
                col = j
    return k, lin, col

print("ingrese matriz 3x3:")
a = [[int(input(f"a[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

k, lin, col = max_matriz(a)
print(f"el mayor elemento es k = {k} en la fila {lin} y columna {col}")
