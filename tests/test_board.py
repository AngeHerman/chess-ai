from chess.board2 import *
from chess.utils import *
from chess.king import *
import pickle


def test_knightMovement(coord):
    plateau = Board2()
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
    plateau = Board2()
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
    plateau = Board2()
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
    
    plateau = Board2()

    """Test des mouvements du roi lorsque pièce est protégé"""
    queenCoordinates = (coord[0]-1,coord[1])

    addPieceToCase(plateau.grille,coord,ROI_NOIR)
    addPieceToCase(plateau.grille,(coord[0]-2,coord[1]),TOUR_BLANC)
    addPieceToCase(plateau.grille,queenCoordinates,DAME_BLANCHE)

    movementList = plateau.king_movement(coord)
    movementList = [movementList[i][1] for i in range(len(movementList))]    

    assert(not queenCoordinates in movementList)

def test_allMovementsAvailable():

    plateau = Board2()

    print(plateau.getAllAvailableMoves(NOIR))
    plateau.print_Board()



def test_specificSituation():
    
    plateau = Board2()
    """plateau.force_play_move(((7,1),(5,2)))
    plateau.force_play_move(((6,4),(5,4)))
    plateau.force_play_move(((1,3),(3,3)))
    plateau.force_play_move(((1,4),(3,4)))
    plateau.force_play_move(((0,6),(2,5)))
    
    print(plateau.grille[7][3].king_movement(plateau.grille))
    emptyCase(plateau.grille,(7,1))
    plateau.force_play_move(((0,4),(3,5)))
    plateau.force_play_move(((7,6),(4,5)))
    plateau.force_play_move(((7,3),(6,5)))"""

    plateau.force_play_move(((7,3),(6,3)))
    plateau.force_play_move(((1,3),(4,3)))
   
    plateau.print_Board()

    print(plateau.getAllAvailableMoves(NOIR))


def test_dumpFile():
    plateau = Board2()

    f = open("dump","r+b")
    pla = pickle.load(f)
    f.close()

    print(pla.getAllAvailableMoves(NOIR))
    pla.print_Board()

def test_petit_roque():
    print("###### TEST PETIT ROQUE ######")
    plateau = Board2()
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "d2d3", "g8f6", "c1e3", "f8e7", "b1c3", "d7d6", "f1e2", "e8g8", "e1g1"]

    plateau.print_Board()
    for m in moves:
        print(m)
        plateau.getAllMovesBasedOnTurn()
        ans = plateau.play_move(chess_notation_to_move(m))
        if ans :
            print("TRUE")
        else:
            print("FALSE")
        plateau.print_Board()

def test_grand_roque():
    print("###### TEST GRAND ROQUE ######")
    plateau = Board2()
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "d2d3", "g8f6", "c1e3", "f8e7", "b1c3", "d7d6", "f1e2", "c8e6","d1d2","d8d7","e1c1","e8c8"]



    plateau.print_Board()
    for m in moves:
        print(m)
        plateau.getAllMovesBasedOnTurn()
        ans = plateau.play_move(chess_notation_to_move(m))
        if ans :
            print("TRUE")
        else:
            print("FALSE")
        plateau.print_Board()
    
    
    
def test_promotion():
    print("###### TEST PROMOTION ######")
    plateau = Board2()
    moves = ["e2e4", "d7d5", "e4d5", "d8d6", "d2d4", "c7c5", "d4c5", "b7b6", "c5b6", "a7a5", "b6b7", "b8a6", "b7b8q"]
    
    # moves_prom_prise = ["e2e4", "d7d5", "e4d5", "d8d6", "d2d4", "c7c5", "d4c5", "b7b6", "c5b6", "a7a5", "b6b7", "a5a4", "b7a8q"]

    print(chess_notation_to_move("b7b8q"))
    print(len(chess_notation_to_move("b7b8q"))) 
    plateau.print_Board()
    for m in moves:
        print(m)
        plateau.getAllMovesBasedOnTurn()
        ans = plateau.play_move(chess_notation_to_move(m))
        if ans :
            print("TRUE")
        else:
            print("FALSE")
            print(plateau.pMoves)
        plateau.print_Board()