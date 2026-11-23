# matriz 6: matriz 4x4 con los mayores valores entre dos matrices

print("ingrese primera matriz 4x4:")
a = [[int(input(f"a[{i}][{j}]: ")) for j in range(4)] for i in range(4)]

print("ingrese segunda matriz 4x4:")
b = [[int(input(f"b[{i}][{j}]: ")) for j in range(4)] for i in range(4)]

c = []
for i in range(4):
    fila = []
    for j in range(4):
        if a[i][j] > b[i][j]:
            fila.append(a[i][j])
        else:
            fila.append(b[i][j])
    c.append(fila)

print("matriz con los mayores valores:")
for f in c:
    print(f)
