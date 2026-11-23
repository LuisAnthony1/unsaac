# vector 13: posicion del mayor y menor en 5 valores

vector = []
print("ingrese 5 valores:")
for i in range(5):
    vector.append(float(input(f"posicion {i}: ")))

pos_mayor = 0
pos_menor = 0

for i in range(1, len(vector)):
    if vector[i] > vector[pos_mayor]:
        pos_mayor = i
    if vector[i] < vector[pos_menor]:
        pos_menor = i

print("el mayor esta en la posicion:", pos_mayor)
print("el menor esta en la posicion:", pos_menor)
