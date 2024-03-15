from chess.board import *
from chess.utils import *
from api.lichess import *
from tests.test_board import *
from ai.monte_carlo import *
import threading
import time
import os

ITERATION_RECHERCHER_COUP = 400
NOMBRE_ERREUR_AVANT_ARRET_JEU = 1
ITERATION_BOUCLE_PRINCIPALE = 100
def play_against_ai():
    is_my_turn = threading.Event()
    plateau = Board()
    plateau.print_Board()
    current_moves = []
    api = Lichess()
    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    time.sleep(2)
    if not api.challenge_ai():
        os.exit(1)
    stream_board_thread = threading.Thread(target=api.stream_board_state, args=(is_my_turn,))
    stream_board_thread.start()
    time.sleep(2)
    erreur = 0
    for c in range (ITERATION_BOUCLE_PRINCIPALE):
        print(is_my_turn.is_set())
        is_my_turn.wait()
        print("Current moves avant")
        print(current_moves)
        moves_en_trop = elements_en_trop(current_moves, api.moves)
        current_moves.extend(moves_en_trop)
        print("Current moves après")
        print(current_moves)
        print("moves en trop")
        print(moves_en_trop)
        print(type(moves_en_trop))
        print("tour est "+ str(plateau.turn))
        for m in moves_en_trop:
            print("le move envoyé est "+m)
            plateau.getAllMovesBasedOnTurn()
            if not plateau.force_play_move(chess_notation_to_move(m)) :
                plateau.print_Board()
                print("Le move non trouvé est "+m)
                print(chess_notation_to_move(m))
        print("tour est "+ str(plateau.turn))
        best_move = mcts(plateau, iterations=ITERATION_RECHERCHER_COUP)
        if not api.make_move( move_to_chess_notation( best_move),is_my_turn):
            # print("Le move est pas passé avec l api :")
            # print(move_to_chess_notation( best_move))
            erreur += 1
            plateau.print_Board()
            cr = getPiecesCoordinates(plateau.grille,ROI_NOIR)
            print(cr[0])
            print(plateau.king_movement(cr[0]))
            print("*************************************")
        if erreur == NOMBRE_ERREUR_AVANT_ARRET_JEU :
            os._exit(1)
    stream_events_thread.join()
    stream_board_thread.join()
    
def play_against_player():
    api = Lichess()
    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    while(not api.game_against_player_started):
        time.sleep(0.5)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Ca a commencé")
    stream_events_thread.join()
    
def test():
    plateau = Board()
    plateau.print_Board()
    # print(plateau.getAllMovesBasedOnTurn())
    a = mcts(plateau,30)
    print(a)
    print(a[0])
    print(a[1])
    print(a[0][0])
    print(a[0][1])
    print(a[1][0])
    print(a[1][1])
    b = move_to_chess_notation(a)
    print(b)
    print("**********TEST PLAY MOVE***************")
    plateau.play_move(a)
    plateau.print_Board()
    print("**********TEST NOTATION***************")
    print(chess_notation_to_move(b))
    print(chess_notation_to_move( move_to_chess_notation( ((7,7),(2,5)) ) ) )
    print("**********TEST******************************************")
    print(chess_notation_to_move('e8g6'))
    print(chess_notation_to_move('e8g6'))
    
    # print(move_to_chess_notation(2,5))
    # print(move_to_chess_notation(4,4))
    # plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    # print("*************************")
    # plateau.turn += 1
    # plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    #test_knightMovement((4,4))
    #test_bishopMovement((4,4))
    #test_rookMovement((4,4))
    #test_kingMovement(())
    #test_kingMovement((4,4))
    
if __name__ == "__main__":
    play_against_ai()
    #play_against_player()
    #test()
    
    
