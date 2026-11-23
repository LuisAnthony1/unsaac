# matriz 22: producto c = a * b para matrices 3x3

print("primera matriz a:")
a = [[int(input(f"a[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

print("segunda matriz b:")
b = [[int(input(f"b[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

c = []
for i in range(3):
    fila = []
    for j in range(3):
        suma = 0
        for k in range(3):
            suma = suma + a[i][k] * b[k][j]
        fila.append(suma)
    c.append(fila)

print("matriz c = a * b:")
for f in c:
    print(f)
