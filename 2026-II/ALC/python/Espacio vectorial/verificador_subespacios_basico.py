# Verificar si H = {(x,y,z) : |x| = |y|} es subespacio de R^3

def cumple(v):
    """Devuelve True si el vector v=(x,y,z) cumple |x| = |y|."""
    x, y, z = v
    return abs(x) == abs(y)

print("=== H = { (x,y,z) : |x| = |y| } ===\n")

# PASO 1: ¿está el vector cero?
print("PASO 1: ¿(0,0,0) está en H?")
print("  |0| = |0| ->", cumple((0,0,0)), "(necesario, pero NO basta)\n")

# PASO 2: buscar dos vectores en H cuya suma NO esté en H
print("PASO 2: buscar contraejemplo\n")

u = (1, 1, 0)     # |1| = |1| ✓
v = (1, -1, 0)    # |1| = |-1| ✓
s = (u[0]+v[0], u[1]+v[1], u[2]+v[2])   # (2, 0, 0)

print("  u =", u, "-> |1| = |1|   ->", cumple(u), "(está en H)")
print("  v =", v, "-> |1| = |-1|  ->", cumple(v), "(está en H)")
print("  u+v =", s, "-> |2| = |0|  ->", cumple(s), "(NO está en H)\n")

# PASO 3: conclusión
print("CONCLUSIÓN:")
print("  u ∈ H, v ∈ H, pero u+v ∉ H")
print("  Falla la cerradura bajo la suma")
print("  ==> H NO es subespacio de R^3")
