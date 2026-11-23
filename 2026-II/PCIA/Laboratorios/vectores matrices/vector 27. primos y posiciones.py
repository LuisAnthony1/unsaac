# vector 27: numeros primos y sus posiciones en vector de 10

def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

vector = []
print("ingrese 10 enteros:")
for i in range(10):
    vector.append(int(input(f"posicion {i}: ")))

print("primos encontrados:")
for i in range(len(vector)):
    if es_primo(vector[i]):
        print(f"numero primo {vector[i]} en la posicion {i}")
