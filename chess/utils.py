
def get_coord(case):
    # Retourne les vrais coordonnées à partir d'une string de type e4.
    #Cette foonction n'utilise pas vraiment le plateau du coup peut-etre on devra la déplacer dans une classe statique
    colonne, ligne = ord(case[0]) - ord('a'), int(case[1]) - 1
    return ligne, colonne