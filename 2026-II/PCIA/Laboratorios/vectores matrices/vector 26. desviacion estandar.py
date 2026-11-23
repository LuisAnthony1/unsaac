# vector 26: desviacion estandar de 10 numeros

import math

v = []
print("ingrese 10 numeros:")
for i in range(10):
    v.append(float(input(f"valor {i + 1}: ")))

n = len(v)
media = sum(v) / n

suma_cuadrados = 0
for x in v:
    suma_cuadrados = suma_cuadrados + (x - media) ** 2

desviacion = math.sqrt(suma_cuadrados / (n - 1))
print("la media es:", media)
print("la desviacion estandar es:", desviacion)
