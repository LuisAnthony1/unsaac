# vector 38: insertar 10 valores ordenadamente a medida que se leen

vector = []
print("ingrese 10 numeros:")
for i in range(10):
    num = int(input(f"numero {i + 1}: "))
    # buscar la posicion correcta para insertar
    insertado = False
    for j in range(len(vector)):
        if num < vector[j]:
            vector.insert(j, num)
            insertado = True
            break
    if not insertado:
        vector.append(num)
    print("vector actual:", vector)

print("vector final ordenado:", vector)
