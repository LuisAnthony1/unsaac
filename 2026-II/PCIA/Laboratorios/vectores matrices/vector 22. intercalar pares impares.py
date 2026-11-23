# vector 22: pares de a e impares de b

a = []
b = []
print("ingrese 10 datos para a:")
for i in range(10):
    a.append(int(input(f"a[{i}]: ")))

print("ingrese 10 datos para b:")
for i in range(10):
    b.append(int(input(f"b[{i}]: ")))

c = []
for i in range(10):
    if i % 2 == 0:
        c.append(a[i])
    else:
        c.append(b[i])

print("vector resultante:", c)
