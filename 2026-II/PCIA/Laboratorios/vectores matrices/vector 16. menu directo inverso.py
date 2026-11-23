# vector 16: mostrar vector directo o inverso segun codigo

vector = []
print("ingrese 5 numeros reales:")
for i in range(5):
    vector.append(float(input(f"posicion {i}: ")))

codigo = int(input("ingrese codigo (0 salir, 1 directo, 2 inverso): "))

if codigo == 0:
    print("programa finalizado")
elif codigo == 1:
    print("vector en orden directo:", vector)
elif codigo == 2:
    print("vector en orden inverso:", vector[::-1])
else:
    print("codigo invalido")
