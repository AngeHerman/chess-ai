from chess.board import *
from chess.utils import *


def test_knightMovement(coord):
    plateau = Board()
    addPieceToCase(plateau.grille,coord,CAVALIER_NOIR)

    movements = [(coord[0] + 2,coord[1] + 1),(coord[0]+2,coord[1]-1),(coord[0]-2,1),(coord[0]-2,coord[1]-1),(coord[0]+1,coord[1] + 2),(coord[0]+1,coord[1]-2),(coord[0]-1,coord[1]+2),(coord[0]-1,coord[1]-2)]
    movementList = plateau.knight_movement(coord)
    movementList = [movementList[i][1] for i in range(len(movementList))]

    check = True

    for i in range(len(movements)):
        if not (movements[i] in movements):
            check = False

    assert(check)


def test_bishopMovement(coord):
    plateau = Board()
    addPieceToCase(plateau.grille,coord,FOU_NOIR)

    movements = [(coord[0] + 1, coord [1] + 1),(coord[0] - 1, coord [1] - 1),(coord[0]- 1, coord [1] + 1),(coord[0] + 1, coord [1] - 1)]

    movementList = plateau.bishop_movement(coord,2)
    movementList = [movementList[i][1] for i in range(len(movementList))]

    print(movementList)
    check = True

    for i in range(len(movements)):
        if not (movements[i] in movements):
            check = False

    assert(check)


def test_rookMovement(coord):
    plateau = Board()
    addPieceToCase(plateau.grille,coord,TOUR_NOIR)

    movements = [(coord[0] + 1, coord [1]),(coord[0] - 1, coord [1]),(coord[0], coord [1] + 1),(coord[0], coord [1] - 1)]

    movementList = plateau.rook_movement(coord,2,2)
    movementList = [movementList[i][1] for i in range(len(movementList))]

    print(movementList)
    check = True

    for i in range(len(movements)):
        if not (movements[i] in movements):
            check = False

    assert(check)

    
def test_queenMovement(coord):
    pass

"""D'autres tests sont à rajoutés pour le roi ..."""
def test_kingMovement(coord):
    
    plateau = Board()

    """Test des mouvements du roi lorsque pièce est protégé"""
    queenCoordinates = (coord[0]-1,coord[1])

    addPieceToCase(plateau.grille,coord,ROI_NOIR)
    addPieceToCase(plateau.grille,(coord[0]-2,coord[1]),TOUR_BLANC)
    addPieceToCase(plateau.grille,queenCoordinates,DAME_BLANCHE)

    movementList = plateau.king_movement(coord)
    movementList = [movementList[i][1] for i in range(len(movementList))]    

    assert(not queenCoordinates in movementList)




