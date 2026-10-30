# Pide una temperatura en Celsius y conviértela a Fahrenheit y Kelvin.
# Fórmulas: F = C · 9/5 + 32 ; K = C + 273.15

# Leer temperatura
celcius = int(input("Ingrese temperatura: "))

# calular temperaturas en Fahrenheit y Kelvin
fah = celcius * 9/5 + 32
kel = celcius + 273.15

# mostrar resultados
print("La temperatura en Fahrenheit es:",fah)
print("La temperatura en Kelvin es:",kel)

