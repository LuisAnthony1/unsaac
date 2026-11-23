# matriz 14: generar carton de bingo 5x5 con numeros del 0 al 99 sin repetir

import random

numeros = []
while len(numeros) < 25:
    n = random.randint(0, 99)
    if n not in numeros:
        numeros.append(n)

carton = []
for i in range(5):
    carton.append(numeros[i * 5:(i + 1) * 5])

print("carton de bingo 5x5:")
for f in carton:
    print(f)
