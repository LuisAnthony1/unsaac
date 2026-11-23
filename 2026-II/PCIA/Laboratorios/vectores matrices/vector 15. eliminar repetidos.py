# vector 15: eliminar elementos repetidos en vector de 20

vector = []
print("ingrese 20 numeros enteros:")
for i in range(20):
    vector.append(int(input(f"numero {i + 1}: ")))

sin_repetidos = []
for n in vector:
    if n not in sin_repetidos:
        sin_repetidos.append(n)

print("elementos sin repetidos:")
print(sin_repetidos)
