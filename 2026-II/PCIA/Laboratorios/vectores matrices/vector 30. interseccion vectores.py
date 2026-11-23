# vector 30: interseccion de dos vectores de 10 elementos

a = []
b = []
print("ingrese 10 elementos para a:")
for i in range(10):
    a.append(int(input(f"a[{i}]: ")))

print("ingrese 10 elementos para b:")
for i in range(10):
    b.append(int(input(f"b[{i}]: ")))

interseccion = []
for elem in a:
    if elem in b and elem not in interseccion:
        interseccion.append(elem)

print("interseccion sin repetidos:", interseccion)
