#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR DE SUBESPACIOS VECTORIALES DE R^3
=============================================

Programa educativo que recibe por consola una condición que define un
conjunto H de R^3 y analiza, paso a paso, si H es un subespacio vectorial.

Instalación de la única dependencia externa:
    pip install sympy

Ejecución:
    python verificador_subespacios.py

CLASES DE CONDICIONES ADMITIDAS (alcance real del programa)
-----------------------------------------------------------
 A) Ecuación o sistema de ecuaciones LINEALES (homogéneas o no).
    Ejemplos:  x+y+z=0      x=y      x+y+z=1      x+y=0, y-z=0
    -> Decisión COMPLETA (demostración general).

 B) Una ecuación de la forma |expresión lineal| = |expresión lineal|.
    Ejemplo:   |x|=|y|      |x+z|=|y|
    -> Decisión COMPLETA (se usa que H es unión de dos subespacios).

 C) Cualquier otra condición construida con x, y, z, números, + - * / ^,
    abs(...) o |...| y los signos = != < <= > >=. Varias condiciones se
    separan con coma o con la palabra "and".
    Ejemplos:  x*y=0     x^2=y^2     x>=0     z=x^2
    -> Decisión PARCIAL:
         * si el vector cero no cumple la condición  -> NO es subespacio.
         * si se encuentra un contraejemplo exacto   -> NO es subespacio.
         * en otro caso                              -> INDETERMINADO.
       (Que el programa no encuentre contraejemplo NO demuestra que H sea
        subespacio.)

SEGURIDAD: el texto del usuario nunca se pasa directamente a eval().
Primero se filtra con una lista blanca de caracteres (solo x, y, z, abs,
números y operadores) y recién después se convierte con SymPy.
"""

import re
import sys
from itertools import product

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        implicit_multiplication,
    )
except ImportError:
    print("Este programa necesita SymPy. Instálalo con:  pip install sympy")
    sys.exit(1)

# Para que los símbolos ∈, ∉, λ se vean bien en la consola.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ----------------------------------------------------------------------
# 1. VARIABLES Y CONSTANTES GLOBALES
# ----------------------------------------------------------------------
x, y, z = sp.symbols("x y z", real=True)
VARIABLES = (x, y, z)
VECTOR_CERO = (0, 0, 0)

MAX_LONGITUD = 120                      # límite de caracteres de la entrada
CARACTERES_PERMITIDOS = set("0123456789.xyz+-*/()=<>!, ")
OPERADORES = re.compile(r"(<=|>=|==|!=|=|<|>)")
TRANSFORMACIONES = standard_transformations + (implicit_multiplication,)
ESPACIO_SYMPY = {                        # únicos nombres que SymPy "conoce"
    "__builtins__": {},
    "Integer": sp.Integer,
    "Float": sp.Float,
    "Rational": sp.Rational,
    "Symbol": sp.Symbol,
    "Abs": sp.Abs,
}
ESPACIO_LOCAL = {"x": x, "y": y, "z": z, "Abs": sp.Abs, "Rational": sp.Rational}

# Veredictos posibles
SUBESPACIO = "ES SUBESPACIO"
NO_SUBESPACIO = "NO ES SUBESPACIO"
INDETERMINADO = "INDETERMINADO"
ERROR = "ERROR DE ENTRADA"


class ErrorEntrada(Exception):
    """Error que se muestra al usuario con un mensaje comprensible."""


# ----------------------------------------------------------------------
# 2. FUNCIONES DE PRESENTACIÓN
# ----------------------------------------------------------------------
def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def paso(texto):
    print("\n>> " + texto)


def texto_expr(e):
    """Convierte una expresión de SymPy a un texto legible."""
    return str(e).replace("Abs(", "abs(").replace("**", "^")


def texto_rel(rel):
    izq, op, der = rel
    return f"{texto_expr(izq)} {op} {texto_expr(der)}"


def texto_vec(v):
    return "(" + ", ".join(str(c) for c in v) + ")"


# ----------------------------------------------------------------------
# 3. LECTURA Y VALIDACIÓN DE LA ENTRADA
# ----------------------------------------------------------------------
def convertir_barras(texto):
    """Cambia |expr| por Abs(expr). No se admiten barras anidadas."""
    if texto.count("|") % 2 != 0:
        raise ErrorEntrada("Hay un número impar de barras '|'. "
                           "Cada valor absoluto necesita barra de apertura y de cierre.")
    resultado = []
    abierta = False
    for caracter in texto:
        if caracter == "|":
            resultado.append(")" if abierta else "Abs(")
            abierta = not abierta
        else:
            resultado.append(caracter)
    return "".join(resultado)


def preparar_texto(texto):
    """Normaliza y VALIDA el texto con una lista blanca de caracteres."""
    t = texto.strip().lower()
    if not t:
        raise ErrorEntrada("La entrada está vacía.")
    if len(t) > MAX_LONGITUD:
        raise ErrorEntrada(f"La entrada es demasiado larga (máximo {MAX_LONGITUD} caracteres).")

    for viejo, nuevo in (("≤", "<="), ("≥", ">="), ("≠", "!="), ("−", "-"),
                         ("×", "*"), ("·", "*"), ("^", "**"), (";", ",")):
        t = t.replace(viejo, nuevo)
    t = re.sub(r"\band\b", ",", t)
    t = convertir_barras(t)
    t = t.replace("abs(", "Abs(")

    # Lista blanca: quitamos la palabra Abs y revisamos lo que queda.
    for caracter in t.replace("Abs", ""):
        if caracter.isalpha():
            if caracter not in "xyz":
                raise ErrorEntrada(f"Símbolo no reconocido: '{caracter}'. "
                                   "Solo se permiten las variables x, y, z y la función abs.")
        elif caracter not in CARACTERES_PERMITIDOS:
            raise ErrorEntrada(f"Carácter no permitido: '{caracter}'.")

    # Exponentes: solo enteros pequeños (evita cálculos gigantes).
    exponentes = re.findall(r"\*\*\s*(\d+)(?![\d.])", t)
    if len(exponentes) != t.count("**") or any(int(e) > 6 for e in exponentes):
        raise ErrorEntrada("Los exponentes deben ser enteros entre 0 y 6 (ej.: x^2).")

    t = re.sub(r"(?<=[xyz])(?=[xyz])", "*", t)               # xy -> x*y
    t = re.sub(r"(\d+)\.(\d+)", r"Rational('\1.\2')", t)     # 0.5 -> Rational('0.5') (exacto)
    return t


def convertir_lado(texto_lado):
    """Convierte un lado de una relación en una expresión de SymPy."""
    if not texto_lado.strip():
        raise ErrorEntrada("Falta una expresión a un lado del signo de comparación.")
    try:
        expr = parse_expr(texto_lado, local_dict=dict(ESPACIO_LOCAL),
                          global_dict=dict(ESPACIO_SYMPY),
                          transformations=TRANSFORMACIONES)
    except Exception:
        raise ErrorEntrada(f"No pude interpretar la expresión «{texto_lado.strip()}». "
                           "Revisa paréntesis, operadores y multiplicaciones.")
    desconocidos = expr.free_symbols - set(VARIABLES)
    if desconocidos:
        raise ErrorEntrada("Variables no permitidas: " + ", ".join(map(str, desconocidos)))
    return expr


def leer_condiciones(texto):
    """Devuelve una lista de relaciones (lado_izq, operador, lado_der)."""
    preparado = preparar_texto(texto)
    relaciones = []
    for pieza in preparado.split(","):
        partes = OPERADORES.split(pieza)
        if len(partes) != 3:
            raise ErrorEntrada("Cada condición debe tener exactamente UN signo de comparación "
                               "(=, !=, <, <=, >, >=). Separa varias condiciones con coma.")
        izq, op, der = partes
        if op == "==":
            op = "="
        relaciones.append((convertir_lado(izq), op, convertir_lado(der)))
    return relaciones


# ----------------------------------------------------------------------
# 4. PERTENENCIA EXACTA DE UN VECTOR A H
# ----------------------------------------------------------------------
def evaluar_relacion(relacion, punto):
    """True / False si se puede decidir con exactitud; None si no está definida."""
    izq, op, der = relacion
    sustitucion = dict(zip(VARIABLES, punto))
    a = izq.subs(sustitucion)
    b = der.subs(sustitucion)
    if a.has(sp.zoo, sp.nan, sp.oo, -sp.oo) or b.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
        return None
    try:
        d = sp.simplify(a - b)
        if op == "=":
            return bool(d == 0)
        if op == "!=":
            return bool(d != 0)
        if op == "<":
            return bool(d < 0)
        if op == "<=":
            return bool(d <= 0)
        if op == ">":
            return bool(d > 0)
        if op == ">=":
            return bool(d >= 0)
    except TypeError:
        return None
    return None


def pertenece(relaciones, punto):
    """¿El punto cumple TODAS las condiciones?  True / False / None."""
    resultados = [evaluar_relacion(r, punto) for r in relaciones]
    if any(r is False for r in resultados):
        return False
    if any(r is None for r in resultados):
        return None
    return True


# ----------------------------------------------------------------------
# 5. CLASIFICACIÓN DE LA CONDICIÓN
# ----------------------------------------------------------------------
def es_lineal(expr):
    return expr.is_polynomial(*VARIABLES) and sp.Poly(expr, *VARIABLES).total_degree() <= 1


def coeficientes(expr):
    return [sp.diff(expr, v) for v in VARIABLES]


def clasificar(relaciones):
    """Devuelve 'lineal', 'valor_absoluto' o 'general'."""
    if all(op == "=" for _, op, _ in relaciones) and \
            all(es_lineal(sp.expand(i - d)) for i, _, d in relaciones):
        return "lineal"
    if len(relaciones) == 1:
        izq, op, der = relaciones[0]
        if op == "=" and izq.func == sp.Abs and der.func == sp.Abs:
            e1, e2 = izq.args[0], der.args[0]
            if es_lineal(sp.expand(e1)) and es_lineal(sp.expand(e2)):
                c1 = sp.expand(e1).subs({x: 0, y: 0, z: 0})
                c2 = sp.expand(e2).subs({x: 0, y: 0, z: 0})
                if c1 == 0 and c2 == 0:          # solo el caso homogéneo
                    return "valor_absoluto"
    return "general"


# ----------------------------------------------------------------------
# 6. ANÁLISIS DE CADA CLASE
# ----------------------------------------------------------------------
def paso_vector_cero(relaciones):
    """Paso 1 (común a todas las clases): ¿(0,0,0) está en H?"""
    paso("PASO 1: ¿El vector cero (0, 0, 0) pertenece a H?")
    for i, rel in enumerate(relaciones, start=1):
        izq, op, der = rel
        a = izq.subs({x: 0, y: 0, z: 0})
        b = der.subs({x: 0, y: 0, z: 0})
        cumple = evaluar_relacion(rel, VECTOR_CERO)
        if a.has(sp.zoo, sp.nan):
            a = "indefinido"
        if b.has(sp.zoo, sp.nan):
            b = "indefinido"
        marca = {True: "Sí se cumple", False: "NO se cumple", None: "no está definida"}[cumple]
        print(f"   Condición {i}: {texto_rel(rel)}")
        print(f"      Al reemplazar x=y=z=0: lado izquierdo = {a},  lado derecho = {b}")
        print(f"      ¿{a} {op} {b}?  ->  {marca}")
    return pertenece(relaciones, VECTOR_CERO)


def analizar_lineal(relaciones):
    """Sistema lineal con vector cero en H: H = núcleo de una matriz A."""
    funciones = [sp.expand(i - d) for i, _, d in relaciones]
    A = sp.Matrix([coeficientes(f) for f in funciones])

    paso("PASO 2: Interpretación matricial")
    print("   Cada ecuación se escribe como f(x,y,z) = 0 con f lineal:")
    for i, f in enumerate(funciones, start=1):
        print(f"      f{i}(x,y,z) = {texto_expr(f)}")
    print(f"   Matriz de coeficientes A = {A.tolist()}")
    print("   Entonces H = { v en R^3 : A·v = 0 }, el núcleo (espacio nulo) de A.")

    # Vectores genéricos y escalar simbólico
    a1, a2, a3, b1, b2, b3 = sp.symbols("a1 a2 a3 b1 b2 b3", real=True)
    lam = sp.Symbol("λ", real=True)
    u = (a1, a2, a3)
    v = (b1, b2, b3)
    suma = (a1 + b1, a2 + b2, a3 + b3)
    escalado = (lam * a1, lam * a2, lam * a3)

    def evaluar(f, vec):
        return sp.expand(f.subs(dict(zip(VARIABLES, vec)), simultaneous=True))

    paso("PASO 3: Cerradura bajo la suma (verificación simbólica, caso general)")
    print("   Sean u=(a1,a2,a3) y v=(b1,b2,b3) en H, es decir f_i(u)=0 y f_i(v)=0.")
    suma_ok = True
    for i, f in enumerate(funciones, start=1):
        fu, fv, fs = evaluar(f, u), evaluar(f, v), evaluar(f, suma)
        igual = sp.expand(fs - (fu + fv)) == 0
        suma_ok = suma_ok and igual
        print(f"   f{i}(u+v) = {texto_expr(fs)}")
        print(f"            = [{texto_expr(fu)}] + [{texto_expr(fv)}] = f{i}(u) + f{i}(v)"
              f"  ->  {'se cumple' if igual else 'NO se cumple'}")
        print(f"            = 0 + 0 = 0   (porque u y v están en H)")

    paso("PASO 4: Cerradura bajo la multiplicación por escalares (caso general)")
    print("   Sea u en H y λ un número real cualquiera.")
    esc_ok = True
    for i, f in enumerate(funciones, start=1):
        fu, fl = evaluar(f, u), evaluar(f, escalado)
        igual = sp.expand(fl - lam * fu) == 0
        esc_ok = esc_ok and igual
        print(f"   f{i}(λu) = {texto_expr(fl)} = λ·[{texto_expr(fu)}] = λ·f{i}(u)"
              f"  ->  {'se cumple' if igual else 'NO se cumple'}")
        print(f"            = λ·0 = 0   (porque u está en H)")

    if not (suma_ok and esc_ok):      # no debería ocurrir con ecuaciones lineales
        print("\n   Inconsistencia interna: no se pudo verificar la linealidad.")
        return INDETERMINADO

    base = A.nullspace()
    dimension = 3 - A.rank()
    paso("PASO 5: Descripción de H y ejemplo numérico (solo ilustrativo)")
    print(f"   rango(A) = {A.rank()}  ->  dim(H) = 3 - {A.rank()} = {dimension}")
    print("   Base de H: " + (", ".join(texto_vec(list(b)) for b in base) if base else "(vacía: H = {0})"))
    if dimension == 3:
        print("   (Todas las ecuaciones son triviales: H = R^3.)")
    if len(base) >= 2:
        w = tuple(base[0][k] + base[1][k] for k in range(3))
        print(f"   Ejemplo: u={texto_vec(list(base[0]))}, v={texto_vec(list(base[1]))}, "
              f"u+v={texto_vec(w)} ∈ H? {pertenece(relaciones, w)}")
    if len(base) >= 1:
        w = tuple(-2 * base[0][k] for k in range(3))
        print(f"   Ejemplo: (-2)·{texto_vec(list(base[0]))} = {texto_vec(w)} ∈ H? "
              f"{pertenece(relaciones, w)}")
    print("   (Estos ejemplos ilustran; la DEMOSTRACIÓN son los pasos 3 y 4.)")

    paso("CONCLUSIÓN")
    print("   H contiene a 0, es cerrado bajo la suma y bajo el producto por escalares.")
    print("   Como esto se demostró para vectores y escalares GENERALES, H es un SUBESPACIO de R^3.")
    return SUBESPACIO


def base_normalizada(vector):
    """Multiplica por -1 si la primera componente no nula es negativa."""
    for c in vector:
        if c != 0:
            return tuple(-k for k in vector) if c < 0 else tuple(vector)
    return tuple(vector)


def analizar_valor_absoluto(relaciones):
    """Caso |e1| = |e2| con e1, e2 lineales y homogéneas."""
    izq, _, der = relaciones[0]
    e1, e2 = sp.expand(izq.args[0]), sp.expand(der.args[0])
    g1, g2 = sp.expand(e1 - e2), sp.expand(e1 + e2)

    paso("PASO 2: Reescritura sin valor absoluto")
    print("   Para números reales: |a| = |b|  <=>  a² = b²  <=>  (a-b)(a+b) = 0")
    print("                        <=>  a = b   o   a = -b.")
    print(f"   Aquí a = {texto_expr(e1)}, b = {texto_expr(e2)}. Entonces H = W1 ∪ W2 donde:")
    print(f"      W1 = {{ {texto_expr(g1)} = 0 }}   y   W2 = {{ {texto_expr(g2)} = 0 }}")
    print("   Cada Wi es el núcleo de una ecuación lineal homogénea, luego es un SUBESPACIO.")
    B1 = sp.Matrix([coeficientes(g1)]).nullspace()
    B2 = sp.Matrix([coeficientes(g2)]).nullspace()
    print("   Base de W1: " + ", ".join(texto_vec(list(b)) for b in B1))
    print("   Base de W2: " + ", ".join(texto_vec(list(b)) for b in B2))

    def en_subespacio(vec, g):
        return sp.expand(g.subs(dict(zip(VARIABLES, vec)))) == 0

    paso("PASO 3: ¿Una unión de dos subespacios es un subespacio?")
    print("   Teorema: W1 ∪ W2 es subespacio  <=>  W1 ⊆ W2  o  W2 ⊆ W1.")
    w1_en_w2 = all(en_subespacio(b, g2) for b in B1)
    w2_en_w1 = all(en_subespacio(b, g1) for b in B2)
    print(f"   ¿W1 ⊆ W2? (¿los vectores base de W1 cumplen la ecuación de W2?) -> {w1_en_w2}")
    print(f"   ¿W2 ⊆ W1? (¿los vectores base de W2 cumplen la ecuación de W1?) -> {w2_en_w1}")

    if w1_en_w2 or w2_en_w1:
        mayor = "W2" if w1_en_w2 else "W1"
        paso("CONCLUSIÓN")
        print(f"   Un subespacio contiene al otro, así que H = {mayor}, que es un SUBESPACIO de R^3.")
        return SUBESPACIO

    # Buscar testigos: u en W1 \ W2 y v en W2 \ W1
    u = next(base_normalizada(b) for b in B1 if not en_subespacio(b, g2))
    v = next(base_normalizada(b) for b in B2 if not en_subespacio(b, g1))
    s = tuple(u[k] + v[k] for k in range(3))

    paso("PASO 4: Vectores testigo (se verifican con la condición ORIGINAL)")
    print(f"   u = {texto_vec(u)} está en W1 pero no en W2;  v = {texto_vec(v)} está en W2 pero no en W1.")
    pu, pv, ps = pertenece(relaciones, u), pertenece(relaciones, v), pertenece(relaciones, s)
    for nombre, vec, res in (("u", u, pu), ("v", v, pv), ("u+v", s, ps)):
        sust = dict(zip(VARIABLES, vec))
        print(f"   {nombre} = {texto_vec(vec)}:  {texto_expr(izq.subs(sust))} = {texto_expr(der.subs(sust))}"
              f"  ->  {'∈ H' if res else '∉ H'}")
    if pu is True and pv is True and ps is False:
        print("   Si u+v estuviera en W1, entonces v=(u+v)-u estaría en W1 (absurdo); "
              "si estuviera en W2, u estaría en W2 (absurdo).")
        print("   Por tanto u+v ∉ W1 ∪ W2 = H, lo que coincide con la verificación directa.")
        paso("PASO 5: Cerradura bajo escalares (informativo)")
        print("   Cada Wi es cerrado bajo escalares, luego H = W1 ∪ W2 también lo es.")
        paso("CONCLUSIÓN")
        print(f"   u, v ∈ H pero u+v ∉ H: H NO es cerrado bajo la suma.")
        print("   Basta incumplir UNA propiedad: H NO es un subespacio de R^3.")
        return NO_SUBESPACIO
    print("   No se pudo confirmar el contraejemplo de forma exacta.")
    return INDETERMINADO


def buscar_contraejemplo(relaciones, radio=2):
    """Busca contraejemplos exactos con coordenadas enteras en [-radio, radio]."""
    cache = {}

    def pert(p):
        if p not in cache:
            cache[p] = pertenece(relaciones, p)
        return cache[p]

    rango = range(-radio, radio + 1)
    miembros = [p for p in product(rango, repeat=3) if p != VECTOR_CERO and pert(p) is True]
    miembros.sort(key=lambda p: (sum(abs(c) for c in p), p))

    for u in miembros:                                   # cerradura bajo escalares
        for lam in (-1, 2, 3, sp.Rational(1, 2)):
            w = tuple(lam * c for c in u)
            if pert(w) is False:
                return ("escalar", u, lam, w)
    for u in miembros:                                   # cerradura bajo la suma
        for v in miembros:
            w = tuple(a + b for a, b in zip(u, v))
            if pert(w) is False:
                return ("suma", u, v, w)
    return None


def analizar_general(relaciones):
    paso("PASO 2: Búsqueda de contraejemplos exactos (condición no lineal / general)")
    print("   No existe un método general para cualquier condición; se buscan vectores")
    print("   con coordenadas enteras entre -2 y 2 que rompan alguna propiedad.")
    hallazgo = buscar_contraejemplo(relaciones)
    if hallazgo is None:
        paso("CONCLUSIÓN")
        print("   No se encontró contraejemplo. Esto NO demuestra que H sea subespacio.")
        print("   Resultado: INDETERMINADO. Se requiere un análisis matemático adicional.")
        return INDETERMINADO
    tipo, u, extra, w = hallazgo
    if tipo == "escalar":
        print(f"   u = {texto_vec(u)} ∈ H,  λ = {extra},  λu = {texto_vec(w)}")
        print(f"   Verificación exacta: u ∈ H -> {pertenece(relaciones, u)};  λu ∈ H -> {pertenece(relaciones, w)}")
        paso("CONCLUSIÓN")
        print("   H NO es cerrado bajo la multiplicación por escalares: NO es un subespacio.")
    else:
        print(f"   u = {texto_vec(u)} ∈ H,  v = {texto_vec(extra)} ∈ H,  u+v = {texto_vec(w)}")
        print(f"   Verificación exacta: u ∈ H -> {pertenece(relaciones, u)};  v ∈ H -> "
              f"{pertenece(relaciones, extra)};  u+v ∈ H -> {pertenece(relaciones, w)}")
        paso("CONCLUSIÓN")
        print("   H NO es cerrado bajo la suma: NO es un subespacio.")
    return NO_SUBESPACIO


# ----------------------------------------------------------------------
# 7. FUNCIÓN PRINCIPAL DE ANÁLISIS
# ----------------------------------------------------------------------
NOMBRES_TIPO = {
    "lineal": "Ecuación/sistema LINEAL (clase A)",
    "valor_absoluto": "Ecuación |lineal| = |lineal| homogénea (clase B)",
    "general": "Condición GENERAL (clase C): análisis parcial",
}


def analizar(texto):
    """Analiza una condición y devuelve el veredicto."""
    titulo(f"Condición ingresada: {texto.strip()}")
    try:
        relaciones = leer_condiciones(texto)
    except ErrorEntrada as error:
        print(f"\n[ERROR] {error}")
        return ERROR

    print("H = { (x, y, z) ∈ R^3 : " + " y ".join(texto_rel(r) for r in relaciones) + " }")
    tipo = clasificar(relaciones)
    print(f"Tipo reconocido: {NOMBRES_TIPO[tipo]}")

    existe_cero = paso_vector_cero(relaciones)
    if existe_cero is False:
        paso("CONCLUSIÓN")
        print("   (0,0,0) ∉ H. Todo subespacio contiene al vector cero, por tanto")
        print("   H NO es un subespacio vectorial de R^3. (No hace falta revisar más.)")
        return NO_SUBESPACIO
    if existe_cero is None:
        paso("CONCLUSIÓN")
        print("   La condición no está definida en el vector cero: el programa no puede decidir.")
        return INDETERMINADO
    print("   (0,0,0) ∈ H. Esto es necesario pero NO suficiente: faltan las dos cerraduras.")

    if tipo == "lineal":
        return analizar_lineal(relaciones)
    if tipo == "valor_absoluto":
        return analizar_valor_absoluto(relaciones)
    return analizar_general(relaciones)


# ----------------------------------------------------------------------
# 8. INTERFAZ DE CONSOLA
# ----------------------------------------------------------------------
CASOS_OBLIGATORIOS = ["x+y+z=0", "x=y", "|x|=|y|", "x+y+z=1"]

AYUDA = """
Escribe SOLO la condición que define H (variables x, y, z). Ejemplos:
    x+y+z=0            ecuación lineal homogénea
    x=y                igualdad entre variables
    |x|=|y|            valor absoluto (también: abs(x)=abs(y))
    x+y+z=1            ecuación no homogénea
    x+y=0, y-z=0       sistema (separa con coma o con 'and')
    x^2=y^2            condición no lineal (análisis parcial)
Comandos:  casos (ejecuta los 4 casos obligatorios) | ayuda | salir
"""


def main():
    print("VERIFICADOR DE SUBESPACIOS VECTORIALES DE R^3")
    print("Un subconjunto H de R^3 es subespacio si: (1) 0 ∈ H, (2) u,v ∈ H => u+v ∈ H,")
    print("(3) u ∈ H, λ ∈ R => λu ∈ H.")
    print(AYUDA)

    historial = []                      # lista de (condición, veredicto)
    while True:
        try:
            texto = input("\nCondición de H > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        comando = texto.lower()
        if comando in ("salir", "exit", "q"):
            break
        if comando == "ayuda":
            print(AYUDA)
            continue
        if comando == "casos":
            for caso in CASOS_OBLIGATORIOS:
                historial.append((caso, analizar(caso)))
            continue
        if comando == "":
            print("No escribiste nada. Escribe una condición o 'ayuda'.")
            continue
        historial.append((texto, analizar(texto)))

    if historial:
        titulo("RESUMEN DE LA SESIÓN")
        for condicion, veredicto in historial:
            print(f"  {condicion:<22} ->  {veredicto}")
    print("\nHasta pronto.")


if __name__ == "__main__":
    main()
