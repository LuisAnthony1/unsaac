# vector 8: leer 6 enteros y mostrar en orden inverso

vector = []
print("ingrese 6 numeros enteros:")
for i in range(6):
    vector.append(int(input(f"numero {i + 1}: ")))

print("valores en orden inverso:")
for i in range(len(vector) - 1, -1, -1):
    print(vector[i])
