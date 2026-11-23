# vector 33: eliminar ceros de un vector de 15 posiciones

vector = []
print("ingrese 15 numeros:")
for i in range(15):
    vector.append(int(input(f"posicion {i}: ")))

compactado = []
for num in vector:
    if num != 0:
        compactado.append(num)

print("vector compactado (sin ceros):", compactado)
