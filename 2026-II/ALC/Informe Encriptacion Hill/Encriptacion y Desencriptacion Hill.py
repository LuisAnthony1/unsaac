import numpy as np
from Hill import (
    MOD,
    texto_a_vector, vector_a_texto,
    inversa_modular,
    cifrar, descifrar,
    formatear_matriz,
)

if __name__ == "__main__":
    PIN = "RED"
    K = np.array([[2, 3, 1],
                  [1, 1, 2],
                  [3, 2, 1]], dtype=int)

    K_inv, det, inv_det = inversa_modular(K)
    vector = texto_a_vector(PIN)
    C = cifrar(K, vector)
    P_rec = descifrar(K_inv, C)

    print("1. Texto original:", PIN, "->", vector.tolist())
    print("2. Matriz clave K:\n", formatear_matriz(K))
    print(f"   det(K) mod 27 = {det} | inverso = {inv_det}")
    print("   Matriz inversa K⁻¹ (mod 27):\n", formatear_matriz(K_inv))
    print("3. Texto cifrado:", vector_a_texto(C), "->", C.tolist())
    print("4. Desencriptación:", vector_a_texto(P_rec), "->", P_rec.tolist())
    print("   Verificación K·K⁻¹ = I (mod 27):",
          np.array_equal((K @ K_inv) % MOD, np.eye(3, dtype=int)))
    print("   ¡Desencriptación exitosa!" if vector_a_texto(P_rec) == PIN else "   ERROR")
