from chess.board2 import *
from chess.utils import *
from tests.test_board import *
from tests.test_more import *
from tests.test_ia import *
from tests.test_alpha_beta_multiprocess_section import *
from tests.test_genetic_algorithm import *

from api.lichess import *
from ai.monte_carlo import *
from ai.alpha_beta import *
from ai.more import *
from ai.opening import *
from ai.alpha_beta_multi_process_section import *

import threading
import time
import os
import pickle
import random

QUICK_SLEEP_TIME = 0
ONE_SEC_SLEEP_TIME = 1

ITERATION_RECHERCHER_COUP = 50
NOMBRE_ERREUR_AVANT_ARRET_JEU = 1
ITERATION_BOUCLE_PRINCIPALE = 100

def play_against_ai():
    is_my_turn = threading.Event()
    plateau = Board2()
    # plateau.print_Board()
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
    while not api.game_started:
        time.sleep(QUICK_SLEEP_TIME)
    open_game_in_browser(api.game_id)
    while not api.is_game_finished:
    # for c in range (ITERATION_BOUCLE_PRINCIPALE):
        print(is_my_turn.is_set())
        is_my_turn.wait()
        if api.is_game_finished:
            break
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("api.moves")
        print(api.moves)
        # print("Current moves avant")
        # print(current_moves)
        moves_en_trop = elements_en_trop(current_moves, api.moves)
        current_moves.extend(moves_en_trop)
        # print("Current moves après")
        # print(current_moves)
        # print("moves en trop")
        # print(moves_en_trop)
        # print(type(moves_en_trop))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("tour est "+ str(plateau.turn))
        for m in moves_en_trop:
            # print("le move envoyé est "+m)
            plateau.getAllMovesBasedOnTurn()
            if not plateau.play_move(chess_notation_to_move(m)) :
                plateau.print_Board()
                print("Le move non trouvé est "+m)
                print(chess_notation_to_move(m))
                print("pMves ")
                # print(plateau.pMoves)
                print([move_to_chess_notation(move) for move in plateau.pMoves])
                print("pMves # ")
                print(plateau.pMoves)


                
                #Serialize object
                log_Error(plateau,best_move)
                
                os._exit(1)
            # print("tour est "+ str(plateau.turn))
        # final_chess_move = None
        best_move = next_move(plateau.turn,current_moves,api.color)
        if best_move is None:
            # best_move = mcts_rapide(plateau,ITERATION_RECHERCHER_COUP,color_to_int(api.color))
            # best_move = alpha_beta_search(plateau, color_to_int(api.color))
            best_move = alpha_beta_search_mprocess_section(plateau, color_to_int(api.color))
            print(f"API COLOR est {color_to_int(api.color)} et move est {best_move}")
            # final_chess_move = alpha_beta_search(copied_board,color_to_int( api.color))
            
        else:
            # print("best move Avant  :")
            # print(best_move)
            best_move = chess_notation_to_move(best_move)
            # final_chess_move = chess_notation_to_move(best_move)
            # print("best move :")
            # print(best_move)
        if not api.make_move( move_to_chess_notation( best_move),is_my_turn):
            # print("Le move est pas passé avec l api :")
            # print(move_to_chess_notation( best_move))
            erreur += 1
            plateau.print_Board()
            
            #Serialize object
            log_Error(plateau,best_move)

            print(best_move)
            print("*************************************")
        if erreur == NOMBRE_ERREUR_AVANT_ARRET_JEU :
            exit()
        time.sleep(ONE_SEC_SLEEP_TIME)
    print(f"MATCH FINISHED: Winner is {api.winner}")
    stream_events_thread.join()
    stream_board_thread.join()
    print(f"MATCH FINISHED: Winner is {api.winner}")

def log_Error(plateau,errorMove):
    f = open("dump","w+b")
    logFile = open("log.txt","w+")

    pickle.dump(plateau,f)
    logFile.write(f"{plateau.pMoves} \n {errorMove}")

    f.close()
    logFile.close()


def play_against_player():
    is_my_turn = threading.Event()
    plateau = Board2()
    api = Lichess()
    current_moves = []
    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    erreur = 0
    print("Waiting for a challenge ")
    while(not api.game_started):
        time.sleep(QUICK_SLEEP_TIME)
    time.sleep(2)
    stream_board_thread = threading.Thread(target=api.stream_board_state, args=(is_my_turn,))
    stream_board_thread.start()
    
    while not api.game_started:
        time.sleep(QUICK_SLEEP_TIME)
    # open_game_in_browser(api.game_id)
    while not api.is_game_finished:
    # for c in range (ITERATION_BOUCLE_PRINCIPALE):
        print(is_my_turn.is_set())
        is_my_turn.wait()
        if api.is_game_finished:
            break
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("api.moves")
        print(api.moves)
        # print("Current moves avant")
        # print(current_moves)
        moves_en_trop = elements_en_trop(current_moves, api.moves)
        current_moves.extend(moves_en_trop)
        # print("Current moves après")
        # print(current_moves)
        # print("moves en trop")
        # print(moves_en_trop)
        # print(type(moves_en_trop))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("tour est "+ str(plateau.turn))
        for m in moves_en_trop:
            # print("le move envoyé est "+m)
            plateau.getAllMovesBasedOnTurn()
            if not plateau.play_move(chess_notation_to_move(m)) :
                plateau.print_Board()
                print("Le move non trouvé est "+m)
                print(chess_notation_to_move(m))
                print("pMves ")
                # print(plateau.pMoves)
                print([move_to_chess_notation(move) for move in plateau.pMoves])
                print("pMves # ")
                print(plateau.pMoves)


                
                #Serialize object
                log_Error(plateau,best_move)
                
                os._exit(1)
            # print("tour est "+ str(plateau.turn))
        # final_chess_move = None
        best_move = next_move(plateau.turn,current_moves,api.color)
        if best_move is None:
            # best_move = mcts_rapide(plateau,ITERATION_RECHERCHER_COUP,color_to_int(api.color))
            # best_move = alpha_beta_search(plateau, color_to_int(api.color))
            best_move = alpha_beta_search_mprocess_section(plateau, color_to_int(api.color))
            print(f"API COLOR est {color_to_int(api.color)} et move est {best_move}")
            # final_chess_move = alpha_beta_search(copied_board,color_to_int( api.color))
            
        else:
            # print("best move Avant  :")
            # print(best_move)
            best_move = chess_notation_to_move(best_move)
            # final_chess_move = chess_notation_to_move(best_move)
            # print("best move :")
            # print(best_move)
        if not api.make_move( move_to_chess_notation( best_move),is_my_turn):
            # print("Le move est pas passé avec l api :")
            # print(move_to_chess_notation( best_move))
            erreur += 1
            plateau.print_Board()
            
            #Serialize object
            log_Error(plateau,best_move)

            print(best_move)
            print("*************************************")
        if erreur == NOMBRE_ERREUR_AVANT_ARRET_JEU :
            exit()
        time.sleep(ONE_SEC_SLEEP_TIME)
    print(f"MATCH FINISHED: Winner is {api.winner}")
    stream_events_thread.join()
    stream_board_thread.join()
    print(f"MATCH FINISHED: Winner is {api.winner}")
    
    stream_events_thread.join()
    stream_board_thread.join()
    
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
    #test_allMovementsAvailable()

    
if __name__ == "__main__":
    #test_dumpFile()
    #test_specificSituation()
    # play_against_ai()
    # play_against_player()
    #test()
    # test_petit_roque()
    # test_grand_roque()
    # test_promotion()
    # test_board_score_0_point()
    # test_board_score_favoring_black()
    # test_board_score_favoring_white()
    # test_board_score_mid_control_nothing_mid()
    # test_board_score_mid_control_pawn_in_mid()
    # print(f"Score : {threat_score_by_color(Board2().grille,BLANC)}")
    # test_ia()
    # test_threat_score_white_threatened()
    # test_threat_score_black_threatened()
    # test_situation2()
    # test_situation2_1()
    # test_situation3()
    # test_situation4()
    # test_situation5()
    # test_situation6()
    # test_situation7()
    # test_situation8()
    #test_situation8_alternatif()
    # test_situation9()  
    # test_dumpFile()
    # test_situation10()
    # test_situation11()
    # test_situation12()
    # test_ia_spped()
    # test_ia_speed2()
    # test_mps()
    # test_abmp_situation_1()
    test_genetic_algo()
    
    
