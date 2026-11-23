# matriz 21: operaciones entre dos matrices 2x2

print("primera matriz 2x2:")
a = [[float(input(f"a[{i}][{j}]: ")) for j in range(2)] for i in range(2)]

print("segunda matriz 2x2:")
b = [[float(input(f"b[{i}][{j}]: ")) for j in range(2)] for i in range(2)]

print("menu: a) sumar  b) restar  c) constante  d) imprimir")
op = input("opcion: ").lower()

if op == 'a':
    c = [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]
    for f in c:
        print(f)
elif op == 'b':
    c = [[b[i][j] - a[i][j] for j in range(2)] for i in range(2)]
    for f in c:
        print(f)
elif op == 'c':
    k = float(input("ingrese constante: "))
    a = [[a[i][j] + k for j in range(2)] for i in range(2)]
    b = [[b[i][j] + k for j in range(2)] for i in range(2)]
    print("matriz a:", a)
    print("matriz b:", b)
elif op == 'd':
    print("matriz a:", a)
    print("matriz b:", b)
