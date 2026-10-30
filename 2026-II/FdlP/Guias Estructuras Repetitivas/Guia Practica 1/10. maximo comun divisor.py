# Escribir un algoritmo que calcule el máximo común divisor (MCD) de
# dos números enteros positivos A y B mediante el algoritmo de Euclides:
# se divide A entre B; si el resto es cero, B es el MCD; si no, A toma
# el valor de B, B toma el valor del resto y se repite el proceso.

# Leer numeros
a = int(input("Ingrese primer numero : "))
b = int(input("Ingrese segundo numero: "))

# calcular por euclides
while b > 0:
    resto = a % b
    a = b
    b = resto
    
# mostrar salida
print("El MCD es", a)
