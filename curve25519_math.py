# Implémentation mathématique optimisée pour Curve25519

# Point neutre de la courbe
def curve_zero():
    """
    Retourne le point neutre (point à l'infini) pour Curve25519.
    """
    return "ZERO"

def curve_is_zero(P):
    """
    Vérifie si le point P est le point neutre.
    :param P: Point elliptique sous forme (x, y) ou 'ZERO'.
    :return: True si P est ZERO, sinon False.
    """
    return P == curve_zero()

# Calcul du point opposé
def curve_opp(Curve, P):
    """
    Retourne le point opposé de P sur Curve25519.
    :param Curve: Paramètres de la courbe (p, a, b).
    :param P: Point elliptique sous forme (x, y).
    :return: Point opposé de P.
    """
    p = Curve[0]
    if curve_is_zero(P):
        return curve_zero()
    x, y = P
    return (x, -y % p)

# Doublement d'un point
def curve_double(Curve, P):
    """
    Double un point sur Curve25519.
    :param Curve: Paramètres de la courbe (p, a, b).
    :param P: Point elliptique sous forme (x, y).
    :return: 2 * P sur la courbe.
    """
    p, a = Curve[0], Curve[1]
    if curve_is_zero(P):
        return P
    x, y = P
    if y == 0:  # Cas particulier où le point est sur l'axe x
        return curve_zero()
    
    # Calcul optimisé du slope (u) et des nouvelles coordonnées
    u = (3 * pow(x, 2, p) + a) * pow(2 * y, -1, p) % p
    x3 = (pow(u, 2, p) - 2 * x) % p
    y3 = (u * (x - x3) - y) % p
    return (x3, y3)

# Addition de deux points
def curve_add(Curve, P, Q):
    """
    Additionne deux points sur Curve25519.
    :param Curve: Paramètres de la courbe (p, a, b).
    :param P: Premier point elliptique.
    :param Q: Second point elliptique.
    :return: P + Q sur la courbe.
    """
    p = Curve[0]
    if curve_is_zero(P):
        return Q
    if curve_is_zero(Q):
        return P
    if P == Q:
        return curve_double(Curve, P)
    if P == curve_opp(Curve, Q):
        return curve_zero()

    x1, y1 = P
    x2, y2 = Q
    
    # Calcul optimisé du slope (u) et des nouvelles coordonnées
    u = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (pow(u, 2, p) - x1 - x2) % p
    y3 = (u * (x1 - x3) - y1) % p
    return (x3, y3)

# Multiplication scalaire rapide
def curve_fast_mult(Curve, P, k):
    """
    Effectue une multiplication scalaire rapide (k * P) sur Curve25519.
    :param Curve: Paramètres de la courbe (p, a, b, q).
    :param P: Point elliptique.
    :param k: Scalaire entier.
    :return: k * P sur la courbe.
    """
    q = Curve[4]  # Ordre du sous-groupe
    k = k % q  # Réduction mod q pour s'assurer que k est dans le sous-groupe
    if k == 0:
        return curve_zero()

    R = curve_zero()  # Initialisation du résultat
    Q = P  # Copie du point pour les doublages successifs
    while k > 0:
        if k & 1:  # Si le bit courant est 1
            R = curve_add(Curve, R, Q)
        Q = curve_double(Curve, Q)  # Doublement à chaque itération
        k >>= 1  # Décalage à droite (division par 2)
    return R
