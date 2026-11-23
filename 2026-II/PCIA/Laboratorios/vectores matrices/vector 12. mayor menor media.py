# vector 12: mostrar 5 valores con mayor menor y media

vector = []
print("ingrese 5 numeros:")
for i in range(5):
    vector.append(float(input(f"valor {i + 1}: ")))

mayor = vector[0]
menor = vector[0]
suma = 0

for num in vector:
    if num > mayor:
        mayor = num
    if num < menor:
        menor = num
    suma = suma + num

print("valores leidos:", vector)
print("mayor:", mayor)
print("menor:", menor)
print("media:", suma / len(vector))
