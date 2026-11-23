# ejercicio 4: ordenar vector de 10 numeros reales

def ordenar_burbuja(vector):
    n = len(vector)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if vector[j] > vector[j + 1]:
                temp = vector[j]
                vector[j] = vector[j + 1]
                vector[j + 1] = temp
    return vector

numeros = []
print("ingrese 10 numeros reales:")
for i in range(10):
    numeros.append(float(input(f"valor {i + 1}: ")))

ordenados = ordenar_burbuja(numeros)
print("vector ordenado:")
print(ordenados)
