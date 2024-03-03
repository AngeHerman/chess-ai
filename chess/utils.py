
from chess.constants import *

def cell_to_chess_notation(row, col):
    # Retourne les vrais coordonnées à partir d'une string de type e4.
    lettre = chr(ord('h') - col)
    nombre = str(row+1)
    return lettre + nombre

def move_to_chess_notation(move):
    return cell_to_chess_notation(move[0][0],move[0][1])+cell_to_chess_notation(move[1][0],move[1][1])

def chess_notation_to_cell(coord):
    lettre = coord[0]
    nombre = int(coord[1])
    col = ord('h') - ord(lettre)
    row = nombre - 1
    return row, col

def chess_notation_to_move(notation):
    start_coord = chess_notation_to_cell(notation[:2])
    end_coord = chess_notation_to_cell(notation[2:])
    return start_coord, end_coord

def moves_en_trop(my_moves, all_moves):
    set_my_moves = set(my_moves)
    set_all_moves = set(all_moves)
    mouvements_en_trop = set_all_moves - set_my_moves
    return list(mouvements_en_trop)

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

def emptyCase(board,coord):
    board[coord[0]][coord[1]] = 0

def addPieceToCase(board,coord,piece):
    board[coord[0]][coord[1]] = piece


    
    

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


def getAllPiecesCoordinatesFromColor(board,color):

    pieces = []

    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            if color > 0  and board[i][j] > 0 or color < 0 and board[i][j] < 0 : 
                pieces.append((i,j))

    return pieces


