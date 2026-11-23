# vector 19: llenar vector de 50 con formula (i + 5*i) % (i + 1)

vector = []
for i in range(50):
    valor = (i + 5 * i) % (i + 1)
    vector.append(valor)

print("vector generado:")
print(vector)
