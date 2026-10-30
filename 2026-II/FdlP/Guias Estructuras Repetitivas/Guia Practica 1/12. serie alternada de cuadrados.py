# Escribir un algoritmo que calcule la suma de la siguiente serie:
# S = 1² − 2² + 3² − 4² + 5² − 6² + ... + 99² − 100² Los términos
# de posición impar se suman y los de posición par se restan. Como
# extensión, generalícelo para los N primeros términos.

# Leer el n-simo termino
n = int(input("N = "))

# Calcular la serie
suma = 0
i = 1

while i <= n:
    if i % 2 != 0:
        suma = suma + (i ** 2)
    else:
        suma = suma - (i ** 2)
    i = i + 1

# Mostrar salida
print("La suma de la serie es", suma)
