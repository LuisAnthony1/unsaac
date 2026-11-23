# vector 32: suma producto diferencia interseccion y union de x e y

x = []
y = []
print("ingrese 5 elementos para x:")
for i in range(5):
    x.append(int(input(f"x[{i}]: ")))

print("ingrese 5 elementos para y:")
for i in range(5):
    y.append(int(input(f"y[{i}]: ")))

suma = [x[i] + y[i] for i in range(5)]
producto = [x[i] * y[i] for i in range(5)]

diferencia = []
for elem in x:
    if elem not in y and elem not in diferencia:
        diferencia.append(elem)

interseccion = []
for elem in x:
    if elem in y and elem not in interseccion:
        interseccion.append(elem)

union = list(x)
for elem in y:
    if elem not in union:
        union.append(elem)

print("suma elemento a elemento:", suma)
print("producto elemento a elemento:", producto)
print("diferencia x - y:", diferencia)
print("interseccion:", interseccion)
print("union:", union)
