# vector 23: producto escalar de dos vectores de 5 reales

x = []
y = []
print("ingrese 5 elementos de x:")
for i in range(5):
    x.append(float(input(f"x[{i}]: ")))

print("ingrese 5 elementos de y:")
for i in range(5):
    y.append(float(input(f"y[{i}]: ")))

prod_escalar = 0
for i in range(5):
    prod_escalar = prod_escalar + x[i] * y[i]

print("vector x:", x)
print("vector y:", y)
print("producto escalar:", prod_escalar)
