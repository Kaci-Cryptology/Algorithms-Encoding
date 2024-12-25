# Curve25519 Signature Scheme

Ce projet implémente un schéma de signature elliptique utilisant la courbe Curve25519. La courbe Curve25519 est une courbe elliptique bien connue et utilisée principalement dans les systèmes de cryptographie modernes, notamment pour les signatures et les échanges de clés sécurisées.

Ce projet contient une implémentation de la génération de clés, de la signature et de la vérification des signatures en utilisant cette courbe, avec des fonctions mathématiques associées dans un fichier séparé.

## Structure du projet

Le projet est organisé de la manière suivante :

- **`curve25519_math.py`** : Implémente les algorithmes mathématiques nécessaires pour effectuer des opérations sur la courbe elliptique (multiplication scalaire, addition de points, etc.).
- **`tests-curve-math.py`** : Contient les tests pour valider les fonctions mathématiques définies dans `curve25519_math.py`.
- **`curve25519.py`** : Contient l'implémentation de la génération de clés, de la signature et de la vérification des signatures.
- **`test_curve25519.py`** : Teste toutes les fonctionnalités définies dans `curve25519.py` (keygen, signature, vérification et hachage).

## Installation des dépendances

Avant de pouvoir utiliser le code, vous devez installer les bibliothèques Python nécessaires.

### Prérequis

1. **Python 3** - Assurez-vous que Python 3 est installé sur votre machine.
2. **PyCryptodome** - Cette bibliothèque est utilisée pour la fonction de hachage SHA3-256.
   
   Installez PyCryptodome avec pip :
   ```bash
   pip install pycryptodome
