# Universidad Nacional de San Antonio Abad del Cusco
# Luis Anthony Mamani Mescco
# --------------------------------------------------
# Modulo el mayor de 2 numeros
def MayorDos(X,Y):
    if X>Y:
        Mayor=X
    else:
        Mayor=Y    
    return Mayor

# Calcular mayor de 2 numeros
# Leer 2 numeros
A=int(input("Numero 1: "))
B=int(input("Numero 2: "))
C=int(input("Numero 3: "))
D=int(input("Numero 4: "))
E=int(input("Numero 5: "))
F=int(input("Numero 6: "))
G=int(input("Numero 7: "))
H=int(input("Numero 8: "))

# Calcular Mayor
X=MayorDos(A,B)
Y=MayorDos(C,D)
Z=MayorDos(E,F)
W=MayorDos(G,H)
Mayor=MayorDos(MayorDos(X,Y),MayorDos(Z,W))

# Mostrar mayor
print('El mayor es : ',Mayor)
