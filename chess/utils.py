
from chess.constants import *

def get_coord(case):
    # Retourne les vrais coordonnées à partir d'une string de type e4.
    #Cette foonction n'utilise pas vraiment le plateau du coup peut-etre on devra la déplacer dans une classe statique
    colonne, ligne = ord(case[0]) - ord('a'), int(case[1]) - 1
    return ligne, colonne

def value_bounded(val,bound):
    return val <= bound and val >= 0

def areCoordinatesBounded(x,y):
        
    if(value_bounded(x,WIDTH - 1) and value_bounded(y,HEIGHT-1)):
        return True

    return False