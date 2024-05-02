from chess.board2 import *
from chess.utils import *
from chess.king import *
from ai.alpha_beta_multi_process_section import *
from ai.alpha_beta import *
import pickle

def test_abmp_situation_1():
    # https://lichess.org/OwrcrsOB/black#11 tour 6 (11 moves)
    plateau = Board2()
    moves = ['e2e4', 'e7e6', 'd2d3', 'f8b4', 'c1d2', 'b4f8', 'b1c3', 'f8b4', 'a2a3', 'b4c3', 'd1c1']

    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search_mprocess_section(plateau,NOIR)
    print("Le move trouvé est")
    print(m)
    plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    
    m = alpha_beta_search_mprocess_section(plateau,BLANC,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    # m = alpha_beta_search(plateau,BLANC)
    # print(m)
    # print(move_to_chess_notation(m))