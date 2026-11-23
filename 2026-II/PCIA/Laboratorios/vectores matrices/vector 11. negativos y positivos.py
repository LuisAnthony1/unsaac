# vector 11: contar negativos y sumar positivos

vector = []
print("ingrese 10 numeros reales:")
for i in range(10):
    vector.append(float(input(f"numero {i + 1}: ")))

negativos = 0
suma_positivos = 0

for num in vector:
    if num < 0:
        negativos = negativos + 1
    elif num > 0:
        suma_positivos = suma_positivos + num

print("cantidad de numeros negativos:", negativos)
print("suma de los numeros positivos:", suma_positivos)
