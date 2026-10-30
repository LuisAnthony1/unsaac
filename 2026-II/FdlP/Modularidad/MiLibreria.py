# Universidad Nacional de San Antonio Abad del Cusco
# Docente: Waldo Ibarra
# Alumno: Luis Anthony Mamani Mescco
# --------------------------------------------------
# Modulo el mayor de 2 numeros
def MayorDos(X,Y):
    if X>Y:
        Mayor=X
    else:
        Mayor=Y    
    return Mayor

def SumaDivisores(N):
    Suma=0
    K=0
    while K<N:
        K+=1
        if N%K==0:
            Suma+=K
    return Suma

def SumaDivisoresPropios(N):
    return SumaDivisores(N)- N

def SumaDivisoresPropios1(N):
    Suma=0
    K=0
    while K<N//2:
        K+=1
        if N%K==0:
            Suma+=K
    return Suma

# Programa Principal
N=int(input("Digite numero: "))
if N==SumaDivisoresPropios1(N):
    Mensaje="Es Perfecto"
else:
    Mensaje="No es Perfecto"
print(Mensaje)
