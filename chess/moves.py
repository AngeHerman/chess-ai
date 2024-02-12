from chess.constants import *
from chess.utils import *

"""
def pawn_movement(board,coord):

    movement_list = []
    pawn = getPiece(board,coord)
    move_value = 1
    special_position = 1

    if(pawn < 0):
        move_value = -1
        special_position = HEIGHT - 2

    if(areCoordinatesBounded(coord[0] + move_value,coord[1] )):
        movement_list.append((coord[0] + move_value,coord[1]))

        if(coord[0] == special_position) :
            movement_list.append((coord[0]+ move_value * 2,coord[1]))
    
    movement_list += pawn_eatPieceMovements(board,coord,-move_value)        
    return movement_list
            
def pawn_ThreatenedCases(board,coord,color):
    
    move_value = 1 if color < 0 else -1
    movement_list = []

    pMovements = [(coord[0]+move_value,coord[1]+move_value),(coord[0]+move_value,coord[1]-move_value)]

    for i in range(0,len(pMovements)):
        if(areCoordinatesBounded(pMovements[i][0],pMovements[i][1])):
            movement_list.append(pMovements[i])
    
    return movement_list


def pawn_eatPieceMovements(board,coord,color):

    threatenedCases = pawn_ThreatenedCases(board,coord,color)
    movement_list = []

    for i in range(0,len(threatenedCases)):
        if(checkCaseHasEdible(board,coord,threatenedCases[i])):
            movement_list.append(threatenedCases[i])

    return movement_list

def knight_movement(board,coord):

    movement_list = []
    movements = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

    for i in range(len(movements)):

        new_y = coord[0] + movements[i][0]
        new_x = coord[1] + movements[i][1]

        if(areCoordinatesBounded(new_y,new_x)):
            movements.append((new_y,new_x))

    return movement_list

def bishop_movement(board,coord,MAX):
    
    movement_list = []

    y = coord[0] 
    x = coord[1] 

    add_dir1 = True
    add_dir2 = True
    add_dir3 = True
    add_dir4 = True

    for i in range(1,MAX):
       
        if(areCoordinatesBounded(y+i,x+i) and add_dir1):
          
            if(checkCanEat(board,coord,(y+i,x+i)) or checkCaseEmpty(board,(y+i,x+i))) : 
                movement_list.append((y+i,x+i))
            if(not(checkCaseEmpty(board,(y+i,x+i)))):
                add_dir1 = False

        if(areCoordinatesBounded(y-i,x-i) and add_dir2):
            
            if(checkCanEat(board,coord,(y-i,x-i)) or checkCaseEmpty(board,(y-i,x-i))) : 
                movement_list.append((y-i,x-i))
            if(not(checkCaseEmpty(board,(y-i,x-i)))):
                add_dir2 = False
        
        if(areCoordinatesBounded(y+i,x-i) and add_dir3):

            if(checkCanEat(board,coord,(y+i,x-i)) or checkCaseEmpty(board,(y+i,x-i))) : 
                movement_list.append((y+i,x-i))
            if(not(checkCaseEmpty(board,(y+i,x-i)))):
                add_dir3 = False

        if(areCoordinatesBounded(y-i,x+i) and add_dir4):

            if(checkCanEat(board,coord,(y-i,x+i)) or checkCaseEmpty(board,(y-i,x+i))) :
                movement_list.append((y-i,x+i))
            if(not(checkCaseEmpty(board,(y-i,x+i)))):
                add_dir4 = False

    return movement_list


def rook_movement(board,coord,width,height):
    
    possible_movements = []
    y = coord[0]
    x = coord[1]

    add1 = True
    add2 = True

    for i in range(1,height):

        if(areCoordinatesBounded(y+i,x) and add1):
            if(checkCanEat(board,coord,(y+i,x)) or checkCaseEmpty(board,(y+i,x))):
                possible_movements.append((y+i,x))
            if(not(checkCaseEmpty(board,(y+i,x)))) : add1 = False

        if(areCoordinatesBounded(y-i,x) and add2):
            if(checkCanEat(board,coord,(y-i,x)) or checkCaseEmpty(board,(y-i,x))):
                possible_movements.append((y-i,x))
            if(not(checkCaseEmpty(board,(y-i,x)))) : add2 = False
    
    add1 = True
    add2 = True

    for j in range(1,width):

        if(areCoordinatesBounded(y,x+j) and add1):
            if(checkCanEat(board,coord,(y,x+j)) or checkCaseEmpty(board,(y,x+j))):
                possible_movements.append((y,x+j))
            if(not(checkCaseEmpty(board,(y,x+j)))): add1 = False

        if(areCoordinatesBounded(y,x-j) and add2):
            if(checkCanEat(board,coord,(y,x-j)) or checkCaseEmpty(board,(y,x-j))):
                possible_movements.append((y,x-j))
            if(not(checkCaseEmpty(board,(y,x-j)))) : add2 = False

    return possible_movements


def queen_movement(board,coord):
    return rook_movement(board,coord,WIDTH,HEIGHT) + bishop_movement(board,coord,WIDTH)

def king_movement(board,coord):

    possible_positions = rook_movement(board,coord,2,2) + bishop_movement(board,coord,2)
    opponent_movements = []

    king = getPiece(board,coord)

    FOU_ADVERSE = FOU_NOIR if king == ROI_BLANC else FOU_BLANC
    TOUR_ADVERSE = TOUR_NOIR if king == ROI_BLANC else TOUR_BLANC
    CAVALIER_ADVERSE = CAVALIER_NOIR if king == ROI_BLANC else CAVALIER_BLANC
    DAME_ADVERSE = DAME_NOIRE if king == ROI_BLANC else DAME_BLANCHE
    PION_ADVERSE = PION_NOIR if king == ROI_BLANC else PION_BLANC

    opponent_pieces = getPiecesCoordinates(board,FOU_ADVERSE) + getPiecesCoordinates(board,TOUR_ADVERSE) + getPiecesCoordinates(board,DAME_ADVERSE) + getPiecesCoordinates(board,CAVALIER_ADVERSE)
    opponent_pieces += getPiecesCoordinates(board,PION_ADVERSE)

    for i in range(0,len(opponent_pieces)):

        piece = getPiece(board,opponent_pieces[i])

        if(piece == FOU_ADVERSE):
            opponent_movements += bishop_movement(board,opponent_pieces[i],WIDTH)
        elif(piece == TOUR_ADVERSE):
            opponent_movements += rook_movement(board,opponent_pieces[i],WIDTH,HEIGHT)
        elif(piece == CAVALIER_ADVERSE):
            opponent_movements += knight_movement(board,opponent_pieces[i])
        elif(piece == DAME_ADVERSE):
            opponent_movements += queen_movement(board,opponent_pieces[i])
        elif(piece == PION_ADVERSE):
            opponent_movements += pawn_ThreatenedCases(board,opponent_pieces[i],-PION_ADVERSE)
    
    positions = [possible_positions[i] for i in range(0,len(possible_positions)) if not(possible_positions[i] in opponent_movements)]

    return positions"""







            

    
