from math import gcd
import numpy as np
from Hill import (
    MOD,
    texto_a_vector, vector_a_texto, rellenar_bloque,
    determinante_sarrus, inversa_modular,
    cifrar, descifrar,
    formatear_matriz, formatear_vector, separador,
)


def main():
    K = np.array([[2, 3, 1],
                  [1, 1, 2],
                  [3, 2, 1]], dtype=int)

    texto = input("Ingrese el texto a cifrar: ").strip()
    if not texto:
        print("No ingresó ningún texto. Saliendo.")
        return

    vector_original = texto_a_vector(texto)
    vector = rellenar_bloque(vector_original.copy())
    texto_preparado = vector_a_texto(vector)

    separador("PASO 0: PREPARACIÓN DEL TEXTO")
    print(f"  Texto ingresado       : {texto}")
    print(f"  Texto normalizado     : {texto.upper().replace(' ', '')}")
    print(f"  Texto rellenado (X)   : {texto_preparado}  (longitud {len(vector)})")
    print(f"  Vector numérico       : {formatear_vector(vector)}")

    separador("PASO 1: MATRIZ CLAVE K (3×3)")
    print(formatear_matriz(K))

    separador("PASO 2: DETERMINANTE E INVERSA MODULAR")
    det_bruto = determinante_sarrus(K)
    det = det_bruto % MOD
    print(f"  Determinante (Sarrus)    : det(K) = {det_bruto}")
    print(f"  Determinante mod 27      : {det}")
    print(f"  MCD({det}, 27)             : {gcd(det, MOD)}  -> invertible ✔")
    inv_det = pow(det, -1, MOD)
    print(f"  Inverso de {det} mod 27    : {inv_det}  (porque {det}·{inv_det} ≡ 1 mod 27)")

    K_inv, _, _ = inversa_modular(K, verbose=True)
    print("   Matriz inversa K⁻¹ (mod 27):\n", formatear_matriz(K_inv))

    separador("PASO 3: CIFRADO  C = K · P  (mod 27)")
    print(f"  Vector a cifrar P = {formatear_vector(vector)}")
    C = cifrar(K, vector, verbose=True)
    texto_cifrado = vector_a_texto(C)
    print(f"\n  Vector cifrado C      : {formatear_vector(C)}")
    print(f"  Texto cifrado         : {texto_cifrado}")

    separador("PASO 4: DESCIFRADO  P = K⁻¹ · C  (mod 27)")
    print(f"  Vector cifrado C = {formatear_vector(C)}")
    P_rec = descifrar(K_inv, C, verbose=True)
    texto_recuperado = vector_a_texto(P_rec)
    print(f"\n  Vector recuperado     : {formatear_vector(P_rec)}")
    print(f"  Texto recuperado      : {texto_recuperado}")

    separador("PASO 5: VERIFICACIÓN")
    identidad = (K @ K_inv) % MOD
    print("  K · K⁻¹ (mod 27):\n", formatear_matriz(identidad))
    print("  ¿Es la identidad?     :",
          np.array_equal(identidad, np.eye(3, dtype=int)))

    coincide = (texto_recuperado[:len(vector_original)] ==
                texto.upper().replace(" ", ""))
    print("  ¿Se recuperó el texto?:",
          "¡SÍ! ✔" if coincide else "NO ✘")


if __name__ == "__main__":
    main()
