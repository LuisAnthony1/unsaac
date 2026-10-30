# Pide el radio de un círculo y muestra su área y perímetro.
# Fórmulas: área = π · r² ; perímetro = 2 · π · r  (usa math.pi).

import math

# leer el radio
radio = float(input("Ingrese el radio: "))

# calcular area y perimetro
area = math.pi*radio*radio
perimetro = math.pi*2*radio

# mostrar resultados
print("El area es:",area)
print("El perimetro es:",perimetro)
