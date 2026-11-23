# ejercicio 7: matriz con mayores valores entre dos matrices 3x3

def matriz_mayores(a, b):
    c = []
    for i in range(3):
        fila = []
        for j in range(3):
            if a[i][j] > b[i][j]:
                fila.append(a[i][j])
            else:
                fila.append(b[i][j])
        c.append(fila)
    return c

print("ingrese datos de la primera matriz 3x3:")
a = [[int(input(f"a[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

print("ingrese datos de la segunda matriz 3x3:")
b = [[int(input(f"b[{i}][{j}]: ")) for j in range(3)] for i in range(3)]

c = matriz_mayores(a, b)
print("matriz con los valores mayores:")
for fila in c:
    print(fila)
