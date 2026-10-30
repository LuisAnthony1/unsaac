# En la sucesión de Fibonacci los dos primeros términos son 0 y 1, y cada
# término siguiente es la suma de los dos anteriores. Escribir un algoritmo
# que muestre los N primeros términos de la sucesión y la suma de ellos.

# Leer el n-simo termino
n = int(input("N = "))

# serie de fibonacci
a = 0
b = 1
contador = 0
suma = 0

while contador < n:
    print(a, end=" ")
    suma = suma + a
    siguiente = a + b
    a = b
    b = siguiente
    contador = contador + 1

# mostrar la suma total
print("\nLa suma de los terminos es", suma)
