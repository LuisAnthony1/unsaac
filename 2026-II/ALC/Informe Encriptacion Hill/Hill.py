from math import gcd
import numpy as np

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"    # A=0 ... Z=26
MOD = 27                                    # Módulo Z27
BLOQUE = 3                                  # Tamaño de bloque


def texto_a_vector(texto):
    # Texto -> vector numérico
    texto = texto.upper().replace(" ", "")
    for c in texto:
        if c not in ALFABETO:
            raise ValueError(f"El carácter '{c}' no pertenece al alfabeto Z27.")
    return np.array([ALFABETO.index(c) for c in texto], dtype=int)


def vector_a_texto(vector):
    # Vector numérico -> texto
    return "".join(ALFABETO[int(v) % MOD] for v in vector)


def rellenar_bloque(vector):
    # Rellena con 'X' hasta múltiplo de BLOQUE
    faltan = (-len(vector)) % BLOQUE
    if faltan:
        relleno = np.full(faltan, ALFABETO.index("X"), dtype=int)
        vector = np.concatenate([vector, relleno])
    return vector


def determinante_sarrus(M):
    # Determinante 3x3 por Sarrus
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return int(a*e*i + b*f*g + c*d*h - c*e*g - a*f*h - b*d*i)


def matriz_cofactores(M):
    # Matriz de cofactores (menores 2x2 con signo)
    cof = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            menor = np.delete(np.delete(M, i, axis=0), j, axis=1)
            det_menor = menor[0, 0]*menor[1, 1] - menor[0, 1]*menor[1, 0]
            cof[i, j] = ((-1) ** (i + j)) * det_menor
    return cof % MOD


def inversa_modular(M, verbose=False):
    # M⁻¹ = (det M)⁻¹ · Adj(M)  mod 27
    det = determinante_sarrus(M) % MOD
    if gcd(det, MOD) != 1:
        raise ValueError(f"M no es invertible mod 27: MCD({det}, 27) != 1")
    inv_det = pow(det, -1, MOD)
    cof = matriz_cofactores(M)
    adjunta = cof.T
    M_inv = (inv_det * adjunta) % MOD
    if verbose:
        print("   Matriz de cofactores C:\n", formatear_matriz(cof))
        print("   Matriz adjunta Adj(M) = C^T:\n", formatear_matriz(adjunta))
        print(f"   det(M) mod 27 = {det}, inverso = {inv_det}")
    return M_inv, det, inv_det


def cifrar_bloque(M, P):
    # C = M · P  mod 27
    return (M @ P) % MOD


def descifrar_bloque(M_inv, C):
    # P = M⁻¹ · C  mod 27
    return (M_inv @ C) % MOD


def cifrar(M, vector, verbose=False):
    # Cifra por bloques
    res = []
    for ini in range(0, len(vector), BLOQUE):
        P = vector[ini:ini + BLOQUE]
        C = cifrar_bloque(M, P)
        if verbose:
            print(f"   P = {formatear_vector(P)}  ->  C = K·P = {formatear_vector(C)}")
        res.extend(C.tolist())
    return np.array(res, dtype=int)


def descifrar(M_inv, vector, verbose=False):
    # Descifra por bloques
    res = []
    for ini in range(0, len(vector), BLOQUE):
        C = vector[ini:ini + BLOQUE]
        P = descifrar_bloque(M_inv, C)
        if verbose:
            print(f"   C = {formatear_vector(C)}  ->  P = K⁻¹·C = {formatear_vector(P)}")
        res.extend(P.tolist())
    return np.array(res, dtype=int)


def formatear_matriz(M, ancho=4):
    # Matriz con columnas alineadas
    return "\n".join(
        "[" + "".join(f"{int(v):>{ancho}}" for v in fila) + " ]"
        for fila in M
    )


def formatear_vector(v, ancho=4):
    # Vector alineado [ v1 v2 v3 ]
    return "[" + "".join(f"{int(x):>{ancho}}" for x in v) + " ]"


def separador(titulo=""):
    # Línea separadora con título
    print("\n" + "═" * 70)
    if titulo:
        print(f"  {titulo}")
        print("═" * 70)


if __name__ == "__main__":
    K = np.array([[2, 3, 1],
                  [1, 1, 2],
                  [3, 2, 1]], dtype=int)
    texto = "ANTHONY"
    vector = rellenar_bloque(texto_a_vector(texto))
    K_inv, det, inv_det = inversa_modular(K)
    C = cifrar(K, vector)
    P = descifrar(K_inv, C)
    print("Texto original :", texto)
    print("Vector rellenado:", formatear_vector(vector))
    print("Matriz K:\n", formatear_matriz(K))
    print(f"det(K) mod 27 = {det}, inverso = {inv_det}")
    print("Matriz K⁻¹:\n", formatear_matriz(K_inv))
    print("Texto cifrado  :", vector_a_texto(C))
    print("Texto descifrado:", vector_a_texto(P))
    print("¿K·K⁻¹ = I?    :", np.array_equal((K @ K_inv) % MOD, np.eye(3, dtype=int)))
