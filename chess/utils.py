
from chess.constants import *

def get_coord(case):
    # Retourne les vrais coordonnées à partir d'une string de type e4.
    #Cette foonction n'utilise pas vraiment le plateau du coup peut-etre on devra la déplacer dans une classe statique
    colonne, ligne = ord(case[0]) - ord('a'), int(case[1]) - 1
    return ligne, colonne

def isValueBounded(val,bound):
    return val <= bound and val >= 0

def areCoordinatesBounded(x,y):
    return isValueBounded(x,WIDTH - 1) and isValueBounded(y,HEIGHT-1)

def checkCaseEmpty(board,coord):
    return board[coord[0]][coord[1]] == 0

def checkCanEat(board,coord,coord2):

    piece = getPiece(board,coord)
    targetPiece = getPiece(board,coord2)

    return (piece > 0 and targetPiece < 0) or (piece < 0 and targetPiece > 0)


def checkCaseHasEdible(board,coord,coord2):
    return not(checkCaseEmpty(board,coord2)) and checkCanEat(board,coord,coord2)

def getPiece(board,coord):

    if(areCoordinatesBounded(coord[0],coord[1])):
        return board[coord[0]][coord[1]]
    return 0

def getPiecesCoordinates(board,piece):

    coords = []

    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            if(board[i][j] == piece): coords.append((i,j))
    
    return coords

    

