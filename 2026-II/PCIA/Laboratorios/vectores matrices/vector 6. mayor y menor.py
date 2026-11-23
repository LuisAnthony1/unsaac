# vector 6: mayor y menor elemento de vector de 10

vector = []
print("ingrese 10 numeros:")
for i in range(10):
    vector.append(int(input(f"numero {i + 1}: ")))

mayor = vector[0]
menor = vector[0]

for num in vector:
    if num > mayor:
        mayor = num
    if num < menor:
        menor = num

print("el mayor elemento es:", mayor)
print("el menor elemento es:", menor)
