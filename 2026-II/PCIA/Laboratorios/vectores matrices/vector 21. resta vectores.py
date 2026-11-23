# vector 21: vector c = a - b

a = []
b = []
print("ingrese 10 enteros para vector a:")
for i in range(10):
    a.append(int(input(f"a[{i}]: ")))

print("ingrese 10 enteros para vector b:")
for i in range(10):
    b.append(int(input(f"b[{i}]: ")))

c = []
for i in range(10):
    c.append(a[i] - b[i])

print("vector c (a - b):", c)
