# matriz 23: calcular b = a^2 para matriz 3x3

print("ingrese matriz a 3x3:")
a = [[int(input(f"a[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

b = []
for i in range(3):
    fila = []
    for j in range(3):
        suma = 0
        for k in range(3):
            suma = suma + a[i][k] * a[k][j]
        fila.append(suma)
    b.append(fila)

print("matriz b = a^2:")
for f in b:
    print(f)
