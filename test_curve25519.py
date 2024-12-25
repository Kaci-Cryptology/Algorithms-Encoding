import unittest
from curve25519_math import *
from curve25519 import *


# Exemple de courbe elliptique (Curve25519)
p = 2**255 - 19
G = (2, 2587177637973221124604506650587198648324617568965701997790174145338249409797)
q = 2**252 + 27742317777372353535851937790883648493  
a = 57896044618658097711785492504343953926634992332820282019728791901641727051837
b = 398341948620716521344
EC = [p, a, b, G, q]
# Test de la génération des clés (keygen)
def test_keygen():
    sk, pk = ecdsa_keygen(EC)
    print("Private Key (sk):", sk)
    print("Public Key (pk):", pk)

    # Vérification que la clé privée est dans l'intervalle [1, q-1]
    assert 0 < sk < EC[4], "Clé privée invalide"
    
    # Vérification que la clé publique est un point sur la courbe
    assert len(pk) == 2, "La clé publique n'est pas un point valide"
    assert pk[0] > 0 and pk[1] > 0, "Les coordonnées de la clé publique sont invalides"
    print("Test Keygen réussi!\n")

# Test de la signature (sign)
def test_sign():
    sk, pk = ecdsa_keygen(EC)
    message = "Test message"
    signature = ecdsa_sign(EC, message, sk)
    print("Signature (b, c):", signature)
    
    # Vérification que la signature (b, c) est dans l'intervalle [1, q-1]
    assert 0 < signature[0] < EC[4], "Signature b invalide"
    assert 0 < signature[1] < EC[4], "Signature c invalide"
    print("Test Sign réussi!\n")

# Test de la vérification de la signature (verif)
def test_verif():
    sk, pk = ecdsa_keygen(EC)
    message = "Test message"
    signature = ecdsa_sign(EC, message, sk)
    
    # Vérification de la signature avec le message original
    is_valid = ecdsa_verif(EC, message, signature, pk)
    assert is_valid, "La signature n'est pas valide pour le message original"
    
    # Vérification avec un message modifié
    invalid_message = "Invalid message"
    is_valid_invalid = ecdsa_verif(EC, invalid_message, signature, pk)
    assert not is_valid_invalid, "La signature n'a pas été rejetée pour un message invalide"
    
    print("Test Verif réussi!\n")

# Test de la fonction de hachage (hash)
def test_hash_function():
    message = "Test message"
    hash_result = Sha3_256_int(message)
    print("Hash result:", hash_result)
    
    # Vérification que le résultat du hachage est un entier positif
    assert isinstance(hash_result, int), "Le résultat du hachage n'est pas un entier"
    assert hash_result > 0, "Le résultat du hachage est inférieur ou égal à zéro"
    print("Test Hash réussi!\n")

# Exécution des tests
def run_tests():
    test_keygen()
    test_sign()
    test_verif()
    test_hash_function()

if __name__ == "__main__":
    run_tests()
