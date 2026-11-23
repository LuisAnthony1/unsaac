# vector 7: mayor elemento y su posicion

vector = []
print("ingrese 10 numeros enteros:")
for i in range(10):
    vector.append(int(input(f"posicion {i}: ")))

mayor = vector[0]
pos = 0

for i in range(1, len(vector)):
    if vector[i] > mayor:
        mayor = vector[i]
        pos = i

print("vector:", vector)
print("el mayor es:", mayor)
print("se encuentra en la posicion:", pos)
