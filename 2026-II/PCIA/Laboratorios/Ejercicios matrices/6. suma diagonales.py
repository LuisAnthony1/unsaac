# ejercicio 6: diagonal principal secundaria y suma

def procesar_diagonales(matriz):
    n = len(matriz)
    diag_princ = []
    diag_sec = []
    suma = 0
    for i in range(n):
        diag_princ.append(matriz[i][i])
        diag_sec.append(matriz[i][n - 1 - i])
        suma = suma + matriz[i][i] + matriz[i][n - 1 - i]
    return diag_princ, diag_sec, suma

n = int(input("ingrese orden de la matriz cuadrada: "))
matriz = []
print("ingrese elementos:")
for i in range(n):
    fila = []
    for j in range(n):
        fila.append(int(input(f"posicion [{i}][{j}]: ")))
    matriz.append(fila)

dp, ds, total = procesar_diagonales(matriz)
print("diagonal principal:", dp)
print("diagonal secundaria:", ds)
print("suma de ambas diagonales:", total)
