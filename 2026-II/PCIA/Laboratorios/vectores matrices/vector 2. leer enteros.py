# vector 2: leer 6 enteros y mostrar

vector = []
print("ingrese 6 numeros enteros:")
for i in range(6):
    valor = int(input(f"numero {i + 1}: "))
    vector.append(valor)

print("valores leidos:")
for num in vector:
    print(num)
