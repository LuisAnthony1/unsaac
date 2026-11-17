import MiLibreria
import random

def Line(C,N):
    return C*N

def Presentacion():
    L=len("Universidad Nacional de San Antonio Abad del Cusco")
    print(Line("-",L+4))
    print("| Universidad Nacional de San Antonio Abad del Cusco |")
    print(Line("-",L+4))
    print("| Autor: Luis Anthony Mamani Mescco                  |")
    print(Line("-",L+4))
    print("| Programa: Operaciones Aritmeticas                  |")
    print(Line("-",L+4))

# Modulos para las operaciones matematicas
def Suma(A, B):
    return A + B

def Resta(A, B):
    if A >= B:
        return A - B
    return False

def Multiplicacion(A, B):
    return A * B

def Division(A, B):
    if B != 0:
        return A // B
    return False

def menu():
    print("====== Menu ======")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Salir")
    opcion=MiLibreria.LeerEntero(1,5,"Escoge tu opcion: ")
    return opcion

def Sumar():
    A = random.randint(1,99)
    B = random.randint(1,99)
    r=Suma(A,B)
    print(f"La suma de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

def Restar():
    A = random.randint(1,99)
    B = random.randint(1,49)
    r=Resta(A,B)
    while r is False:
        print("Probando Otros Numeros")
        A = random.randint(1,99)
        B = random.randint(1,49)
        r=Resta(A,B)
    print(f"La resta de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

def Multiplicar():
    A = random.randint(1,12)
    B = random.randint(1,12)
    r=Multiplicacion(A,B)
    print(f"La Multiplicacion de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

def Dividir():
    A = random.randint(1,12)
    B = random.randint(1,12)
    r=Multiplicacion(A,B)
    print(f"La Division de {r} y {B} es?")
    resultado=int(input("-> "))
    if resultado==Division(r,B):
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
