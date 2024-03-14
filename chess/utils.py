
from chess.constants import *


"""
Tout réadapter pour objet, ex vérif des empty et vider les cases 
"""
def get_coord(case):
    # Retourne les vrais coordonnées à partir d'une string de type e4.
    #Cette foonction n'utilise pas vraiment le plateau du coup peut-etre on devra la déplacer dans une classe statique
    colonne, ligne = ord(case[0]) - ord('a'), int(case[1]) - 1
    return ligne, colonne

def isValueBounded(val,bound):
    return val <= bound and val >= 0

def areCoordinatesBounded(x,y):
    return isValueBounded(x,WIDTH - 1) and isValueBounded(y,HEIGHT-1)



def checkCanEat(board,coord,coord2):

    piece = getPiece(board,coord)
    targetPiece = getPiece(board,coord2)

    if piece == None or targetPiece == None:
        return False

    return (piece.color != targetPiece.color)

def emptyCase(board,coord):
    board[coord[0]][coord[1]] = None

def addPieceToCase(board,coord,piece):
    board[coord[0]][coord[1]] = piece
    
    

def checkCaseHasEdible(board,coord,coord2):
    return not(checkCaseEmpty(board,coord2)) and checkCanEat(board,coord,coord2)
"""
def getPiece(board,coord):

    if(areCoordinatesBounded(coord[0],coord[1])):
        return board[coord[0]][coord[1]]
    return 0
"""
def getPiecesCoordinates(board,piece):

    coords = []

    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            if(board[i][j] == piece): coords.append((i,j))
    
    return coords


def getAllPiecesCoordinatesFromColor(board,color):

    pieces = []

    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            if color > 0  and board[i][j] > 0 or color < 0 and board[i][j] < 0 : 
                pieces.append((i,j))

    return pieces

def getPiece(tab,coord):

    if(areCoordinatesBounded(coord[0],coord[1])):
        return tab[coord[0]][coord[1]]
    return None

def getAllPieces(tab,color):        
    return [getPiece(tab,(i,j)) for i in range (0, WIDTH) for j in range(0,HEIGHT) if checkPieceColor(tab,(i,j),color) and checkPieceName(tab,(i,j),piece)]

def getAllPiecesFromColor(tab,color):
    return [getPiece(tab,(i,j)) for i in range (0, WIDTH) for j in range(0,HEIGHT) if checkPieceColor(tab,(i,j),color) ]

def checkPieceColor(tab,coord,color):
    if checkCaseEmpty(tab,coord): return False
    return getPiece(tab,coord).color == color

def checkPieceName(tab,coord,name):
    if checkCaseEmpty(coord): return False
    return getPiece(tab,coord).name == name

def checkCaseEmpty(tab,coord):
    return getPiece(tab,coord) == None

def getAdvesaryColor(color):    
    adversaryColor = BLANC if color == NOIR else NOIR
    return adversaryColor


def pieceMovement(piece,tab):
    if piece.name == FOU:
        return piece.bishop_movement(tab,WIDTH)
    elif piece.name == TOUR:
        return piece.rook_movement(tab,WIDTH,HEIGHT)
    elif piece.name == CAVALIER:
        return piece.knight_movement(tab)
    elif piece.name == DAME:
        return piece.queen_movement(tab)
    elif piece.name == PION:
        return piece.pawn_movement(tab) 
    elif piece.name == ROI:
        return piece.king_movement(tab) 
    return []


def getThreatenedCases(tab,color):

    adversaryColor = getAdvesaryColor(color)
    allPieces = getAllPiecesFromColor(tab,adversaryColor)
    threatenedCoordinates = []

    for i in range(0,len(allPieces)):
        if allPieces[i].name == PION:
            threatenedCoordinates += allPieces[i].pawn_ThreatenedCases()
        elif allPieces[i].name != ROI:
            threatenedCoordinates += (pieceMovement(allPieces[i],tab))

    return threatenedCoordinates


    
def straightPathsFromPiece(piece,tab,height,width):

    possible_movements = [[piece.coordinates] for _ in range(4)]
    y, x = piece.coordinates[0], piece.coordinates[1]
    add1,add2 = True,True

    for i in range(1,height):

        if(areCoordinatesBounded(y+i,x) and add1):
            if checkCanEat(tab,(y,x),(y+i,x)) :
                add1 = False
            possible_movements[0].append((y+i,x))

        if(areCoordinatesBounded(y-i,x) and add2):
            if checkCanEat(tab,(y,x),(y-i,x)) :
                add2 = False
            possible_movements[1].append((y-i,x))

    add1,add2 = True,True

    for j in range(1,width):

        if(areCoordinatesBounded(y,x+j) and add1):
            if checkCanEat(tab,(y,x),(y,x+j)) :
                add1 = False
            possible_movements[2].append((y,x+j))

        if(areCoordinatesBounded(y,x-j) and add2):
            if checkCanEat(tab,(y,x),(y,x-j)) :
                add2 = False
            possible_movements[3].append((y,x-j))

    return possible_movements



def diagonalPathsFromPiece(piece,tab,MAX):

    paths = [[piece.coordinates] for _ in range(4)] 
    y, x= piece.coordinates[0], piece.coordinates[1] 
    
    add_dir1 = True
    add_dir2 = True
    add_dir3 = True
    add_dir4 = True

    for i in range(1,MAX):
        if(areCoordinatesBounded(y+i,x+i) and add_dir1):
            if checkCanEat(tab,(y,x),(y+i,x+i)):
                add_dir1 = False
            paths[0].append((y+i,x+i))

        if(areCoordinatesBounded(y-i,x-i) and add_dir2):
            if checkCanEat(tab,(y,x),(y-i,x-i)):
                add_dir2 = False
            paths[1].append((y-i,x-i))
        
        if(areCoordinatesBounded(y+i,x-i) and add_dir3):
            if checkCanEat(tab,(y,x),(y+i,x-i)):
                add_dir3 = False
            paths[2].append((y+i,x-i))

        if(areCoordinatesBounded(y-i,x+i) and add_dir4):
            if checkCanEat(tab,(y,x),(y-i,x+i)):
                add_dir4 = False
            paths[3].append((y-i,x+i))
        
    return paths