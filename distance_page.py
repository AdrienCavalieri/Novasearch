import numpy as np


# distance de hamming peut être utiliser seulement si les pages web sont de même longueurs.
# Si une page est plus grande que l'autre le calcul s'arrête quand il n'y a plus 2 valeurs à comparer
# S'il y a un décalage de 1 cela fausse le calcul
# Preferer hamming à levenshtein car la compléxité est beaucoup plus petite.
# Même si hamming à beaucoup de contraintes, pour savoir si 2 pages sont identiques cela est suffisant.

def dist_hamming(m1, m2, max):
    d = 0
    for a, b in zip(m1, m2):  # pour chaque couple
        if a != b:  # on test si c'est égale
            d += 1
        if (d == max):
            return d
    return d


# print(dist_hamming("close", "cloue"))

# algo levenshtein
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))  # matrice de longueur  n+1*m+1
    for x in range(size_x):  # initialisation de la matrice
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):  # pour chaque lettre on compare
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:  # si la lettre seq1 == lettre seq2
                matrix[x, y] = min(
                    # on place dans la matrice[x,y] le minimum des 3 scores (insertion/délétion/substitution)
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])
