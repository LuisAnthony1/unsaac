# ejercicio 3: vector c = a - b con 10 elementos cada uno

def restar_vectores(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i] - b[i])
    return c

a = []
b = []
print("ingrese 10 elementos para el vector a:")
for i in range(10):
    a.append(int(input(f"a[{i}]: ")))

print("ingrese 10 elementos para el vector b:")
for i in range(10):
    b.append(int(input(f"b[{i}]: ")))

c = restar_vectores(a, b)
print("vector c (a - b):")
print(c)
