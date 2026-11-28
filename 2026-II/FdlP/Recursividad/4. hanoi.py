# Universidad Nacional de San Antonio Abad del Cusco
# Departamento Academico de Informatica
# Luis Anthony Mamani Mescco - 194522
# --------------------------------------------------
# Torres de Hanoi
# --------------------------------------------------

def hanoi(N,inicial,final):
    if N==1:
        print("Mover un disco de",inicial," a ",final)
    else:
        auxiliar = 6 - inicial - final
        hanoi(N-1,inicial,auxiliar);
        hanoi(1,inicial,final);
        hanoi(N-1,auxiliar,final);
        return f"Cantidad de movimientos minimos {2**N-1}"

# programa principal

print("Luis Anthony")
print(hanoi(3,1,2))
