# matriz 7: matriz 10x10 segun condiciones sobre indices

matriz = []
for i in range(10):
    fila = []
    for j in range(10):
        if i < j:
            val = 2 * i + 7 * j - 2
        elif i == j:
            val = 3 * (i ** 2) - 1
        else:
            val = 4 * (i ** 3) - 5 * (j ** 2) + 1
        fila.append(val)
    matriz.append(fila)

print("matriz 10x10 generada:")
for fila in matriz:
    print(fila)
