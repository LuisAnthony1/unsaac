# vector 25: 100 primeros naturales no multiplos de 7 ni terminados en 7

vector = []
numero = 1

while len(vector) < 100:
    if numero % 7 != 0 and numero % 10 != 7:
        vector.append(numero)
    numero = numero + 1

print("vector de 100 elementos:")
print(vector)
