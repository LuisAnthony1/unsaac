# ejercicio 4: simetria respecto a la columna central

def simetrica(m):
    n = len(m)
    centro = n // 2
    for i in range(n):
        for k in range(1, centro + 1):
            if m[i][centro - k] != m[i][centro + k]:
                return False
    return True

n = int(input("ingrese dimension impar de la matriz: "))
matriz = []
print("ingrese elementos:")
for i in range(n):
    fila = []
    for j in range(n):
        valor = int(input(f"posicion [{i}][{j}]: "))
        fila.append(valor)
    matriz.append(fila)

if simetrica(matriz):
    print("la matriz es simetrica respecto a su columna central")
else:
    print("la matriz no es simetrica")
