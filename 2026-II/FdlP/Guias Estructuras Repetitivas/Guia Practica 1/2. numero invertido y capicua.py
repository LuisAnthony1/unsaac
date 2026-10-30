# Escribir un algoritmo que lea un numero entero positivo, obtenga el
# numero con sus digitos en orden inverso y determine si el numero es capicua
# (se lee igual de izquierda a derecha que de derecha a izquierda)

# Leer numero
num = int(input("Ingrese el numero: "))

# guardar el numero original
ori=num
inv=0

# invertir numero
while num>0:
    dig=num%10
    inv=inv*10+dig
    num=num//10

if ori==inv:
    mensaje="Es capicua"
else:
    mensaje="No es capicua"

# mostrar
print("Invertido ->",inv,mensaje)
