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

def menu():
    print("====== Menu ======")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    opcion=MiLibreria.LeerEntero(1,4,"Escoge tu opcion: ")
    return opcion

def Sumar():
    A = random.randint(1,99)
    B = random.randint(1,99)
    r=Sumar(A,B)
    print(f"La suma de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

def Restar():
    A = random.randint(1,99)
    B = random.randint(1,49)
    r=Restar(A,B)
    while r==False:
        print("Probando Otros Numeros")
        A = random.randint(1,99)
        B = random.randint(1,49)
    print(f"La resta de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)


def Multiplicar():
    print(f"La Multiplicacion de {A} y {B} es?")
    resultado=int(input("-> "))
    if resultado==r:
        print("Correcto!")
    else:
        print("Mal el resultado es",r)


def Dividir():
    r=Multiplicar(A,B)
    print(f"La Division de {r} y {B} es?")
    resultado=int(input("-> "))
    if A==Dividir(r,B):
        print("Correcto!")
    else:
        print("Mal el resultado es",r)

# Programa Principal
Presentacion()
opcion=menu()

# operaciones
while

