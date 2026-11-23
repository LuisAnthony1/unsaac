# vector 3: cuadrado de 10 numeros reales

reales = []
cuadrados = []
print("ingrese 10 numeros reales:")
for i in range(10):
    val = float(input(f"numero {i + 1}: "))
    reales.append(val)
    cuadrados.append(val ** 2)

print("conjunto original:", reales)
print("conjunto de cuadrados:", cuadrados)
