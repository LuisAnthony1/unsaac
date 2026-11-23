import MiLibreria
import random

# Modulo linea decorativa
def Line(C,N):
    return C*N

# Modulo presentacion institucional
def Presentacion():
    L=len("Universidad Nacional de San Antonio Abad del Cusco")
    print(Line("-",L+4))
    print("| Universidad Nacional de San Antonio Abad del Cusco |")
    print(Line("-",L+4))
    print("| Autor: Luis Anthony Mamani Mescco                  |")
    print(Line("-",L+4))
    print("| Programa: Operaciones Aritmeticas                  |")
    print(Line("-",L+4))

# Modulo menu principal
def menu():
    print("====== Menu ======")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Salir")
    opcion=MiLibreria.LeerEntero(1,5,"Escoge tu opcion: ")
    return opcion

# Modulo Sumar enteros
def Sumar():
    A = random.randint(1,99)
    B = random.randint(1,99)
    r = A + B
    print(f"La suma de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

# Modulo Restar enteros
def Restar():
    A = random.randint(1,99)
    B = random.randint(1,49)
    while A < B:
        print("Probando Otros Numeros")
        A = random.randint(1,99)
        B = random.randint(1,49)
    r = A - B
    print(f"La resta de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

# Modulo Multiplicar enteros
def Multiplicar():
    A = random.randint(1,12)
    B = random.randint(1,12)
    r = A * B
    print(f"La Multiplicacion de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

# Modulo Dividir enteros
def Dividir():
    A = random.randint(1,12)
    B = random.randint(1,12)
    r = A * B
    print(f"La Division de {r} y {B} es?")
    resultado=int(input("-> "))
    if resultado==A:
        print("Correcto!")
    else:
        print("Mal el resultado es",A)

# Programa Principal
Presentacion()
opcion=menu()

# operaciones
while opcion != 5:
    if opcion == 1:
        Sumar()
    elif opcion == 2:
        Restar()
    elif opcion == 3:
        Multiplicar()
    elif opcion == 4:
        Dividir()
    print()
    opcion=menu()

print("\n¡Hasta luego!")
