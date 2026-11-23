# vector 37: ordenar primeros 6 crecientes y ultimos decrecientes

vector = []
print("ingrese 11 numeros:")
for i in range(11):
    vector.append(int(input(f"posicion {i}: ")))

parte1 = sorted(vector[:6])
parte2 = sorted(vector[6:], reverse=True)

resultado = parte1 + parte2
print("vector ordenado por partes:", resultado)
