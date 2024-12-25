from curve25519_math import curve_add, curve_double, curve_fast_mult, curve_zero

# Définition des paramètres de Curve25519
p = 2**255 - 19
a = 486662
b = 1
G = (9, 14781619447589544791020593568409986887264606134611226301374015720010141009897)
q = 2**252 + 27742317777372353535851937790883648493
Curve = (p, a, b, G, q)

# Tests
if __name__ == "__main__":
    print("=== Tests pour Curve25519 ===")
    print("Point G :", G)
    print("Doublement de G :", curve_double(Curve, G))
    print("Addition G + G :", curve_add(Curve, G, G) == curve_double(Curve, G) )
    print("3 * G :", curve_fast_mult(Curve, G, 3) == curve_add(Curve,curve_double(Curve, G), G))
    print("q * G (doit être ZERO) :", curve_fast_mult(Curve, G, q) == curve_zero())
    print("q + 5 * G (équivalent à 5 * G) :", curve_fast_mult(Curve, G, q + 5) == curve_fast_mult(Curve, G, 5))
