# ==============================================================================
# UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO
# DEPARTAMENTO ACADÉMICO DE INGENIERÍA INFORMÁTICA
# ORGANIZACIÓN Y ARQUITECTURA DEL COMPUTADOR - LABORATORIO 08
#
# Simulador y Validador de Casos de Prueba para Lab08_Palindromo.asm
# Emula con exactitud la lógica a nivel de bytes ejecutada en ensamblador x86-64.
# ==============================================================================

def simular_ensamblador(cadena_entrada):
    # 1. Quitar \n y \r (emulación de .strip_nl)
    input_str = cadena_entrada.rstrip('\r\n')
    input_len = len(input_str)

    # 2. Validación de longitud
    if input_len == 0:
        return {
            "estado": "VACIA",
            "mensaje": "[!] AVISO: La cadena ingresada esta vacia."
        }

    if input_len > 40:
        return {
            "estado": "ERROR_LONGITUD",
            "input_len": input_len,
            "mensaje": f"[!] ERROR: La cadena ingresada excede los 40 caracteres permitidos (ingreso {input_len})."
        }

    # 3. Procesamiento de espacios y mayúsculas (.loop_filtro)
    buf_clean = []
    for ch in input_str:
        if ch in (' ', '\t'):
            continue  # Omitir espacios
        if 'A' <= ch <= 'Z':
            buf_clean.append(chr(ord(ch) + 32))  # Normalizar a minúscula (+32)
        else:
            buf_clean.append(ch)

    clean_str = "".join(buf_clean)
    clean_len = len(clean_str)

    if clean_len == 0:
        return {
            "estado": "SOLO_ESPACIOS",
            "mensaje": "[!] AVISO: La frase contiene unicamente espacios; no hay caracteres utiles."
        }

    # 4. Cadena invertida (.loop_invertir)
    buf_rev = clean_str[::-1]

    # 5. Dos punteros (.loop_comparar)
    es_palindromo = True
    left = 0
    right = clean_len - 1
    while left < right:
        if clean_str[left] != clean_str[right]:
            es_palindromo = False
            break
        left += 1
        right -= 1

    return {
        "estado": "EXITO",
        "input_orig": input_str,
        "input_len": input_len,
        "clean_str": clean_str,
        "clean_len": clean_len,
        "rev_str": buf_rev,
        "es_palindromo": es_palindromo,
        "dictamen": "ES UN PALINDROMO" if es_palindromo else "NO ES UN PALINDROMO"
    }

casos_de_prueba = [
    ("anita lava la tina", True, "Frase clásica con espacios y mayúsculas intermedias"),
    ("dabale arroz a la zorra el abad", True, "Frase célebre de 31 caracteres con múltiples espacios"),
    ("reconocer", True, "Palabra simple capicúa/palíndroma"),
    ("somos o no somos", True, "Frase con 3 espacios"),
    ("radar", True, "Palabra simple corta"),
    ("12321", True, "Palíndromo numérico impar"),
    ("123 43 21", True, "Palíndromo numérico con espacios"),
    ("A ti no bonita", True, "Frase con mayúscula inicial y espacios"),
    ("oso", True, "Palabra simétrica corta"),
    ("Arquitectura de computadoras", False, "Frase normal no palíndroma"),
    ("Hola mundo", False, "Frase común no palíndroma"),
    ("123456", False, "Cadena numérica no simétrica"),
    ("", "VACIA", "Caso borde: Cadena vacía"),
    ("     ", "SOLO_ESPACIOS", "Caso borde: Solo espacios"),
    ("Esta es una frase que tiene mas de cuarenta caracteres en total", "ERROR_LONGITUD", "Validación límite > 40 caracteres")
]

if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO SIMULACIÓN DE CASOS DE PRUEBA (ASSEMBLY x86-64)")
    print("=" * 70)

    todos_pasan = True
    for i, (cad, esperado, desc) in enumerate(casos_de_prueba, 1):
        res = simular_ensamblador(cad)
        print(f"\nCaso #{i:02d}: \"{cad}\"")
        print(f"  Descripción : {desc}")

        if esperado in (True, False):
            cumple = (res["estado"] == "EXITO" and res["es_palindromo"] == esperado)
            print(f"  Procesada   : \"{res['clean_str']}\" (len={res['clean_len']})")
            print(f"  Invertida   : \"{res['rev_str']}\"")
            print(f"  Dictamen    : {res['dictamen']} | Esperado: {'ES PALINDROMO' if esperado else 'NO PALINDROMO'}")
        else:
            cumple = (res["estado"] == esperado)
            print(f"  Estado      : {res['estado']} | Mensaje: {res['mensaje']}")

        print(f"  Resultado   : {'[PASÓ CORRECTAMENTE]' if cumple else '[FALLÓ]'}")
        if not cumple:
            todos_pasan = False

    print("\n" + "=" * 70)
    if todos_pasan:
        print("TODOS LOS CASOS DE PRUEBA PASARON EXITOSAMENTE (100%)")
    else:
        print("SE DETECTARON FALLOS EN LA SIMULACIÓN")
    print("=" * 70)
