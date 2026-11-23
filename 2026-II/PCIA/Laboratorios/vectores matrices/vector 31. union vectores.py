# vector 31: union de dos vectores de 10 elementos

a = []
b = []
print("ingrese 10 elementos para a:")
for i in range(10):
    a.append(int(input(f"a[{i}]: ")))

print("ingrese 10 elementos para b:")
for i in range(10):
    b.append(int(input(f"b[{i}]: ")))

union = []
for elem in a:
    if elem not in union:
        union.append(elem)

for elem in b:
    if elem not in union:
        union.append(elem)

print("union sin repetidos:", union)
