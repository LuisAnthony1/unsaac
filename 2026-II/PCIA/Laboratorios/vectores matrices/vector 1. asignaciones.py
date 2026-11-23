# vector 1: asignaciones y suma de posiciones

a = [1, 0, 5, -2, -5, 7]
suma = a[0] + a[1] + a[5]
print("la suma es:", suma)

a[4] = 100
print("vector modificado:")
for elemento in a:
    print(elemento)
