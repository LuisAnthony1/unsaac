# vector 34: leer 10 numeros diferentes

vector = []
print("ingrese 10 numeros distintos:")
while len(vector) < 10:
    val = int(input(f"numero {len(vector) + 1}: "))
    if val in vector:
        print("el numero ya fue ingresado intente otro")
    else:
        vector.append(val)

print("vector final:", vector)
