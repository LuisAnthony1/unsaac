# vector 28: separar elementos en v1 impares y v2 pares

v = []
print("ingrese 10 numeros enteros:")
for i in range(10):
    v.append(int(input(f"valor {i + 1}: ")))

v1 = []
v2 = []

for num in v:
    if num % 2 != 0:
        v1.append(num)
    else:
        v2.append(num)

print("vector v1 (impares):", v1)
print("vector v2 (pares):", v2)
