from chess.board2 import *
from chess.utils import *
from ai.more import *

def test_board_score_0_point():
    plateau = Board2()
    print(board_score(plateau.grille))
    
def test_board_score_favoring_black():
    plateau = Board2()
    plateau.grille = [
        [Rook(BLANC), None, Bishop(BLANC),  None, Queen(BLANC), Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
        [Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC)],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR)],
        [Rook(NOIR),Knight(NOIR), Bishop(NOIR),  King(NOIR), Queen(NOIR), Bishop(NOIR), Knight(NOIR), Rook(NOIR)]
    ]
    print(board_score(plateau.grille))
    

def test_board_score_favoring_white():
    plateau = Board2()
    plateau.grille = [
        [Rook(BLANC), Knight(BLANC), Bishop(BLANC),  King(BLANC), Queen(BLANC), Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
        [Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC)],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR)],
        [Rook(NOIR),Knight(NOIR), None,  King(NOIR), None, Bishop(NOIR), Knight(NOIR), Rook(NOIR)]
    ]
    print(board_score(plateau.grille))
    
def test_board_score_mid_control_nothing_mid():
    plateau = Board2()
    plateau.grille = [
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None,Pawn(NOIR), None, None, None, None, None, None]
    ]
    print(board_score(plateau.grille))
    assert(board_score(plateau.grille) == PION_NOIR_POINT)
    
def test_board_score_mid_control_pawn_in_mid():
    plateau = Board2()
    plateau.grille = [
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None,Pawn(BLANC), None, None, None, None, None, None],
        [None] * 8,
        [None] * 8,
        [None] * 8,
    ]
    print(board_score(plateau.grille))
    assert(board_score(plateau.grille) == (PION_BLANC_POINT + SCORE_POINT_FOR_MID_CONTROL))


def test_threat_score_white_threatened():
    plateau = Board2()
    plateau.grille = [
        [King(BLANC),Pawn(BLANC), None, None, None, None, None, None],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None,Pawn(BLANC), None, None, None, None, None, None],
        [None] * 8,
        [None] * 8,
        [Rook(NOIR),Pawn(NOIR), None, None, None, None, None, None],

    ]
    plateau.initializeCoordinates()
    print(f"Threat score white :{threat_score_by_color(plateau.grille,BLANC)}")
    print(f"Threat score black :{threat_score_by_color(plateau.grille,NOIR)}")
    print(f"Threat score :{threat_score(plateau.grille)}")
    
    
    
def test_threat_score_black_threatened():
    plateau = Board2()
    plateau.grille = [
        [Rook(BLANC),Pawn(BLANC), None, None, None, None, None, None],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None,Pawn(BLANC), None, None, None, None, None, None],
        [None] * 8,
        [None] * 8,
        [Queen(NOIR),Pawn(BLANC), None, None, None, None, None, None],

    ]
    plateau.initializeCoordinates()
    print(f"Threat score white :{threat_score_by_color(plateau.grille,BLANC)}")
    print(f"Threat score black :{threat_score_by_color(plateau.grille,NOIR)}")
    print(f"Threat score :{threat_score(plateau.grille)}")
    