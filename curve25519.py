# curve25519.py
# Ce fichier implémente les principales fonctions liées à la courbe elliptique Curve25519 pour la signature ECDSA.
# Il contient des fonctions pour générer des clés, signer des messages et vérifier des signatures.
# Les opérations de courbe elliptique utilisées sont définies dans le fichier curve25519_math.py.

from random import randint  # Importation de randint pour générer des nombres aléatoires dans des plages spécifiques
from Crypto.Hash import SHA3_256  # Importation de SHA3_256 pour le hachage des messages
from curve25519_math import *  # Importation des fonctions mathématiques nécessaires pour les opérations de courbe elliptique

# Fonction de hachage SHA3-256 qui retourne le résultat sous forme d'entier.
def Sha3_256_int(message):
    """
    Cette fonction applique le hachage SHA3-256 sur un message et retourne le résultat sous forme d'entier.
    
    Args:
        message (str): Le message à hacher.
        
    Returns:
        int: Le résultat du hachage SHA3-256 sous forme d'entier.
    """
    return int(SHA3_256.new(bytes(message, "utf-8")).hexdigest(), 16)

# Fonction de génération de clés pour l'algorithme ECDSA.
def ecdsa_keygen(EC):
    """
    Cette fonction génère une paire de clés (clé privée, clé publique) pour l'algorithme ECDSA sur la courbe elliptique spécifiée.
    
    Args:
        EC (list): La courbe elliptique définie sous la forme [p, a, b, G, q].
            - p : Le premier paramètre de la courbe
            - a, b : Paramètres de la courbe
            - G : Le point générateur de la courbe
            - q : L'ordre du groupe généré par G
            
    Returns:
        tuple: Un tuple contenant la clé privée (sk) et la clé publique (pk).
            - sk : La clé privée (un entier)
            - pk : La clé publique (un tuple de coordonnées (x, y) de la courbe elliptique)
    """
    q = EC[4]  # L'ordre de la courbe elliptique
    G = EC[3]  # Le point générateur de la courbe
    a = randint(1, q-1)  # Génération d'un nombre aléatoire pour la clé privée
    A = curve_fast_mult(EC, G, a)  # Calcul de la clé publique : A = a * G

    sk, pk = a, A  # La clé privée est 'a', la clé publique est 'A'
    return (sk, pk)

# Fonction de signature ECDSA : crée une signature pour un message donné.
def ecdsa_sign(EC, message, sk):
    """
    Cette fonction signe un message avec une clé privée donnée en utilisant l'algorithme ECDSA.
    
    Args:
        EC (list): La courbe elliptique utilisée pour la signature.
        message (str): Le message à signer.
        sk (int): La clé privée utilisée pour la signature.
        
    Returns:
        tuple: La signature sous forme de tuple (b, c) où :
            - b : Une coordonnée du point sur la courbe
            - c : Le second paramètre de la signature
    """
    q = EC[4]  # L'ordre de la courbe elliptique
    G = EC[3]  # Le point générateur de la courbe
    h = Sha3_256_int(message) % q  # Calcul du hachage du message modifié par l'ordre de la courbe
    Condition = True  # Condition pour répéter la génération de la signature jusqu'à ce qu'elle soit valide
    
    while Condition:
        k = randint(1, q-1)  # Génération d'un nombre aléatoire pour 'k'
        B = curve_fast_mult(EC, G, k)  # Calcul du point B = k * G
        b = B[0] % q  # Coordonnée x du point B
        c = ((h + sk * b) * pow(k, -1, q)) % q  # Calcul de la signature : c = (h + sk * b) * k^(-1) mod q
        
        # Si b ou c sont nuls, on génère une nouvelle signature
        if b == 0 or c == 0:
            continue
        
        Condition = False  # Condition remplie, signature valide générée
    s = (b, c)  # Signature sous la forme d'un tuple (b, c)
    return s

# Fonction de vérification de la signature ECDSA.
def ecdsa_verif(EC, message, signature, pk):
    """
    Cette fonction vérifie la validité d'une signature ECDSA pour un message donné et une clé publique.
    
    Args:
        EC (list): La courbe elliptique utilisée pour la vérification.
        message (str): Le message dont la signature doit être vérifiée.
        signature (tuple): La signature à vérifier, sous forme de tuple (b, c).
        pk (tuple): La clé publique sous forme de coordonnées (x, y).
        
    Returns:
        bool: True si la signature est valide, False sinon.
    """
    q = EC[4]  # L'ordre de la courbe elliptique
    G = EC[3]  # Le point générateur de la courbe
    b, c = signature[0], signature[1]  # Paramètres de la signature
    h = Sha3_256_int(message) % q  # Hachage du message modifié par l'ordre de la courbe
    alpha = (h * pow(c, -1, q)) % q  # Calcul de alpha = h * c^(-1) mod q
    P = curve_fast_mult(EC, G, alpha)  # Calcul du point P = alpha * G
    beta = (b * pow(c, -1, q)) % q  # Calcul de beta = b * c^(-1) mod q
    Q = curve_fast_mult(EC, pk, beta)  # Calcul du point Q = beta * pk
    R = curve_add(EC, P, Q)  # Calcul de R = P + Q
    
    # La signature est valide si b == R[0] mod q
    return b == R[0] % q
