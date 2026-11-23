# Universidad Nacional de San Antonio Abad del Cusco
# Departamento Academico de Informatica
# Fundamentos de Programacion
# Luis Anthony Mamani Mescco
# --------------------------------------------------
# Programa principal: OperacionesRacionales.py

import MiLibreria
from MiRacional import (
    Sumar,
    Restar,
    Multiplicar,
    Dividir,
    Simplificar,
    ATexto,
    LeerRacional
)

# Modulo linea decorativa
def Line(C, N):
    return C * N

# Modulo presentacion institucional
def Presentacion():
    L = len("Universidad Nacional de San Antonio Abad del Cusco")
    print(Line("-", L + 4))
    print("| Universidad Nacional de San Antonio Abad del Cusco |")
    print(Line("-", L + 4))
    print("| Autor: Luis Anthony Mamani Mescco                  |")
    print(Line("-", L + 4))
    print(f"| {'Programa: Operaciones Racionales'.ljust(L)} |")
    print(Line("-", L + 4))

# Modulo menu principal
def Menu():
    print("OPERACIONES CON NUMEROS RACIONALES")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Simplificar un racional")
    print("6. Salir del programa")
    opcion = MiLibreria.LeerEntero(1, 6, "Escoge tu operacion: ")
    return opcion

# Programa Principal
Presentacion()
opcion = Menu()

while opcion != 6:
    if opcion == 1:
        r1 = LeerRacional("Primer racional")
        r2 = LeerRacional("Segundo racional")
        res = Sumar(r1, r2)
        print(f"{ATexto(r1)} + {ATexto(r2)} = {ATexto(res)}")

    elif opcion == 2:
        r1 = LeerRacional("Primer racional")
        r2 = LeerRacional("Segundo racional")
        res = Restar(r1, r2)
        print(f"{ATexto(r1)} - {ATexto(r2)} = {ATexto(res)}")

    elif opcion == 3:
        r1 = LeerRacional("Primer racional")
        r2 = LeerRacional("Segundo racional")
        res = Multiplicar(r1, r2)
        print(f"{ATexto(r1)} * {ATexto(r2)} = {ATexto(res)}")

    elif opcion == 4:
        r1 = LeerRacional("Primer racional")
        r2 = LeerRacional("Segundo racional")
        res = Dividir(r1, r2)
        print(f"{ATexto(r1)} / {ATexto(r2)} = {ATexto(res)}")

    elif opcion == 5:
        r = LeerRacional("Racional a simplificar")
        print(f"Forma simplificada: {ATexto(r)}")

    print()
    opcion = Menu()

print("\n¡Hasta luego!")
