# vector 36: ordenar vector de 10 reales

vector = []
print("ingrese 10 numeros reales:")
for i in range(10):
    vector.append(float(input(f"numero {i + 1}: ")))

for i in range(len(vector) - 1):
    for j in range(len(vector) - 1 - i):
        if vector[j] > vector[j + 1]:
            temp = vector[j]
            vector[j] = vector[j + 1]
            vector[j + 1] = temp

print("vector ordenado:", vector)
