import numpy as np
from Hill import (
    MOD,
    texto_a_vector, vector_a_texto, rellenar_bloque,
    inversa_modular,
    cifrar, descifrar,
    formatear_matriz, formatear_vector, separador,
)

K = np.array([[2, 3, 1],
              [1, 1, 2],
              [3, 2, 1]], dtype=int)


def menu():
    # Menú principal
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "CIFRADO DE HILL 3x3 — Z27" + " " * 28 + "║")
    print("╠" + "═" * 68 + "╣")
    print("║  1) Cifrar un texto" + " " * 48 + "║")
    print("║  2) Descifrar un texto" + " " * 44 + "║")
    print("║  3) Mostrar matriz K y su inversa K⁻¹" + " " * 29 + "║")
    print("║  4) Salir" + " " * 57 + "║")
    print("╚" + "═" * 68 + "╝")


def opcion_cifrar():
    # Opción 1: cifrar texto
    separador("OPCIÓN 1: CIFRAR TEXTO")
    texto = input("  Ingrese el texto a cifrar: ").strip()
    if not texto:
        print("  ⚠ No ingresó ningún texto.")
        return

    vector_orig = texto_a_vector(texto)
    vector = rellenar_bloque(vector_orig.copy())
    texto_norm = texto.upper().replace(" ", "")

    print(f"\n  Texto normalizado     : {texto_norm}")
    print(f"  Texto rellenado (X)   : {vector_a_texto(vector)}")
    print(f"  Vector numérico       : {formatear_vector(vector)}")

    print("\n  Matriz clave K:")
    print(formatear_matriz(K))

    try:
        K_inv, det, inv_det = inversa_modular(K)
    except ValueError as e:
        print(f"  ✘ {e}")
        return

    print(f"\n  det(K) mod 27         : {det}")
    print(f"  Inverso de {det} mod 27   : {inv_det}")

    print("\n  --- Proceso de cifrado (bloque a bloque) ---")
    C = cifrar(K, vector, verbose=True)
    texto_cifrado = vector_a_texto(C)

    print(f"\n  Vector cifrado        : {formatear_vector(C)}")
    print(f"  ► TEXTO CIFRADO       : {texto_cifrado}")

    esperado = input(
        "\n  (Opcional) Ingrese el texto cifrado ESPERADO para comparar "
        "(Enter para omitir): "
    ).strip().upper().replace(" ", "")

    if esperado:
        if esperado == texto_cifrado:
            print(f"  ✔ CORRECTO: coincide con el esperado '{esperado}'.")
        else:
            print(f"  ✘ DIFERENTE: obtenido '{texto_cifrado}' "
                  f"≠ esperado '{esperado}'.")


def opcion_descifrar():
    # Opción 2: descifrar texto
    separador("OPCIÓN 2: DESCIFRAR TEXTO")
    texto = input("  Ingrese el texto cifrado: ").strip()
    if not texto:
        print("  ⚠ No ingresó ningún texto.")
        return

    try:
        vector = texto_a_vector(texto)
    except ValueError as e:
        print(f"  ✘ {e}")
        return

    print(f"\n  Texto normalizado     : {texto.upper().replace(' ', '')}")
    print(f"  Vector numérico       : {formatear_vector(vector)}")

    print("\n  Matriz clave K:")
    print(formatear_matriz(K))

    try:
        K_inv, det, inv_det = inversa_modular(K, verbose=True)
    except ValueError as e:
        print(f"  ✘ {e}")
        return

    print("\n  Matriz inversa K⁻¹ (mod 27):")
    print(formatear_matriz(K_inv))

    print("\n  --- Proceso de descifrado (bloque a bloque) ---")
    P = descifrar(K_inv, vector, verbose=True)
    texto_descifrado = vector_a_texto(P)

    print(f"\n  Vector descifrado     : {formatear_vector(P)}")
    print(f"  ► TEXTO DESCIFRADO    : {texto_descifrado}")

    esperado = input(
        "\n  (Opcional) Ingrese el texto original ESPERADO para comparar "
        "(Enter para omitir): "
    ).strip().upper().replace(" ", "")

    if esperado:
        if texto_descifrado == esperado:
            print(f"  ✔ CORRECTO: coincide con el esperado '{esperado}'.")
        elif texto_descifrado.rstrip("X") == esperado.rstrip("X"):
            print(f"  ✔ CORRECTO (ignorando relleno 'X'): '{esperado}'.")
        else:
            print(f"  ✘ DIFERENTE: obtenido '{texto_descifrado}' "
                  f"≠ esperado '{esperado}'.")


def opcion_mostrar_matrices():
    # Opción 3: mostrar K y K⁻¹
    separador("OPCIÓN 3: MATRIZ CLAVE K Y SU INVERSA K⁻¹")
    print("  Matriz K:")
    print(formatear_matriz(K))

    try:
        K_inv, det, inv_det = inversa_modular(K, verbose=True)
    except ValueError as e:
        print(f"  ✘ {e}")
        return

    print("\n  Matriz inversa K⁻¹ (mod 27):")
    print(formatear_matriz(K_inv))

    identidad = (K @ K_inv) % MOD
    print("\n  Verificación K · K⁻¹ (mod 27):")
    print(formatear_matriz(identidad))
    print("  ¿Es la identidad?     :",
          "✔ SÍ" if np.array_equal(identidad, np.eye(3, dtype=int)) else "✘ NO")


def main():
    # Bucle del menú
    while True:
        menu()
        opcion = input("  Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            opcion_cifrar()
        elif opcion == "2":
            opcion_descifrar()
        elif opcion == "3":
            opcion_mostrar_matrices()
        elif opcion == "4":
            print("\n  ¡Hasta luego! 👋\n")
            break
        else:
            print("\n  ⚠ Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
