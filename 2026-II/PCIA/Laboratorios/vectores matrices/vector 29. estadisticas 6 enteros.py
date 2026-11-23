# vector 29: estadisticas de 6 enteros

vector = []
print("ingrese 6 numeros enteros:")
for i in range(6):
    vector.append(int(input(f"numero {i + 1}: ")))

pares = []
suma_pares = 0
impares = []

for num in vector:
    if num % 2 == 0:
        pares.append(num)
        suma_pares = suma_pares + num
    else:
        impares.append(num)

print("numeros pares:", pares)
print("suma de numeros pares:", suma_pares)
print("numeros impares:", impares)
print("cantidad de impares:", len(impares))
