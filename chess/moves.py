from chess.constants import *
from chess.utils import *


def pawn_movement(board,coord):

    movement_list = []

    if(value_bounded(coord[1],HEIGHT-1) and value_bounded(coord[0],WIDTH - 1)):
        movement_list.append((coord[0],coord[1]+1))
        if(coord[1] == 1) :
            movement_list.append((coord[0],coord[1]+2))

    return movement_list

def knight_movement(board,coord):

    movement_list = []

    movements = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

    for i in range(len(movements)):

        new_x = coord[0] + movements[i][0]
        new_y = coord[1] + movements[i][1]

        if(value_bounded(new_x,WIDTH - 1) and value_bounded(new_y,HEIGHT -1)):
            movements.append((new_x,new_y))

    return movement_list



def bishop_movement(board,coord,MAX):
    
    movement_list = []

    x = coord[0] 
    y = coord[1] 

    add_dir1 = True
    add_dir2 = True
    add_dir3 = True
    add_dir4 = True

    for i in range(1,MAX):
       
        if(areCoordinatesBounded(x+i,y+i)):
          
            if(add_dir1) : movement_list.append((x+i,y+i))
            if(board[x+i][y+i] != 0):
                add_dir1 = False

        if(areCoordinatesBounded(x-i,y-i)):
            
            if(add_dir2) : movement_list.append((x-i,y-i))
            if(board[x-i][y-i] != 0):
                add_dir2 = False
        
        if(areCoordinatesBounded(x+i,y-i)):

            if(add_dir3) : movement_list.append((x+i,y-i))
            if(board[x+i][y-i] != 0):
                add_dir3 = False

        if(areCoordinatesBounded(x-i,y+i)):

            if(add_dir4) : movement_list.append((x-i,y+i))
            if(board[x-i][y+i] != 0):
                add_dir4 = False

    return movement_list


def tower_movement(board,coord,width,height):
    
    possible_movements = []

    x = coord[0]
    y = coord[1]

    add1 = True
    add2 = True

    for i in range(1,width):
        if(areCoordinatesBounded(x+i,y)):
            if(add1):
                possible_movements.append(x+i,y)
            if(board[x+i][y] != 0) : add1 = False
        if(areCoordinatesBounded(x-i,y)):
            if(add2):
                possible_movements.append(x-i,y)
            if(board[x-i][y] != 0) : add2 = False
    
    add1 = True
    add2 = True

    for j in range(1,height):
        if(areCoordinatesBounded(x,y+j)):
            if(add1):
                possible_movements.append(x,y+j)
            if(board[x][y+j] != 0) : add1 = False
        if(areCoordinatesBounded(x,y-j)):
            if(add2):
                possible_movements.append(x-j,y)
            if(board[x][y-j] != 0) : add2 = False


    return possible_movements


def queen_movement(board,coord):
    return tower_movement(board,coord,WIDTH,HEIGHT) + bishop_movement(board,coord,WIDTH)

def king_movement(board,coord):
    return tower_movement(board,coord,2,2) + bishop_movement(board,coord,2)
