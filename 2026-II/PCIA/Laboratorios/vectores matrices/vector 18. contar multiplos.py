# vector 18: contar multiplos de x en vector de 10

vector = []
print("ingrese 10 numeros:")
for i in range(10):
    vector.append(int(input(f"numero {i + 1}: ")))

x = int(input("ingrese el numero x: "))
multiplos = []

for num in vector:
    if num % x == 0:
        multiplos.append(num)

print(f"cantidad de multiplos de {x}:", len(multiplos))
print("los multiplos son:", multiplos)
