def cociente(A, B):
    if A < B:
        return 0
    return 1 + cociente(A - B, B)

def resto(A, B):
    if A < B:
        return A
    return resto(A - B, B)

A = int(input("Ingrese dividendo (A): "))
B = int(input("Ingrese divisor (B): "))

if B <= 0 or A < 0:
    print("Error: Ingrese numeros enteros positivos (B > 0).")
else:
    q = cociente(A, B)
    r = resto(A, B)
    print(f"El cociente entero de {A} // {B} es: {q}")
    print(f"El resto de {A} % {B} es: {r}")
