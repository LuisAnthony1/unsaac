# ejercicio 2: eliminar repetidos de un vector de 20 enteros

def eliminar_repetidos(vector):
    unicos = []
    for num in vector:
        if num not in unicos:
            unicos.append(num)
    return unicos

vector = []
print("ingrese 20 numeros enteros:")
for i in range(20):
    n = int(input(f"numero {i + 1}: "))
    vector.append(n)

resultado = eliminar_repetidos(vector)
print("elementos sin repetir:")
print(resultado)
