# Se lee un numero entero formado unicamnete por los digitos 0 y 1, que
# representa un numero en base 2. Escribir un algoritmo que lo convierta
# a base 10. validar que el numero ingresado solo contenga ceros y unos

# Leer numero binario
num = int(input("Ingrese numero binario: "))

# verificacion de numero binario
aux = num
while aux>0:
    dig = aux%10
    if dig>=2:
        print("Error el numero no es binario")
        num = int(input("Ingrese numero binario: "))
        aux = num
    else:
        aux=aux//10

# conversion de binario a decimal
k=0
dec=0
while num>0:
    dig=num%10
    val=dig*(2**k)
    dec=dec+val
    k=k+1
    num=num//10
    
# mostrar salida
print("El numero en base 10 es",dec)
