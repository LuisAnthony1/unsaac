# vector 5: contar numeros pares en vector de 10

vector = []
print("ingrese 10 numeros:")
for i in range(10):
    vector.append(int(input(f"numero {i + 1}: ")))

pares = 0
for num in vector:
    if num % 2 == 0:
        pares = pares + 1

print("cantidad de valores pares:", pares)
