# vector 39: triangulo de pascal con n lineas

n = int(input("ingrese numero de lineas n: "))

fila_anterior = []
for i in range(n):
    fila = [1] * (i + 1)
    for j in range(1, i):
        fila[j] = fila_anterior[j - 1] + fila_anterior[j]
    print(fila)
    fila_anterior = fila
