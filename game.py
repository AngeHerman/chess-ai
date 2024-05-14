import threading
import os
import time
from chess.board2 import *
from chess.utils import *
from tests.test_board import *
from tests.test_more import *
from tests.test_alpha_beta import *
from tests.test_alpha_beta_multiprocess_section import *
from tests.test_genetic_algorithm import *

from api.lichess import *
from ai.monte_carlo import *
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
OUR_IA_LEVELS = ["0","1", "2", "3", "4"]
LICHESS_IA_LEVELS = ["1", "2", "3", "4","5", "6", "7", "8"]

def log_Error(plateau,errorMove):
    f = open("dump","w+b")
    logFile = open("log.txt","w+")

    pickle.dump(plateau,f)
    logFile.write(f"{plateau.pMoves} \n {errorMove}")

    f.close()
    logFile.close()

def play_against_ai_o(ia_level,lichess_level):
    is_my_turn = threading.Event()
    plateau = Board2()
    # plateau.print_Board()
    current_moves = []
    api = Lichess(lichess_level)
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
        is_my_turn.is_set()
        is_my_turn.wait()
        # print("Apres le wait")
        if api.is_game_finished:
            break
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # print("api.moves")
        # print(api.moves)
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
        # print("tour est "+ str(plateau.turn))
        # print("Avant move")    
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
        if api.is_game_finished:
            break
        # print("Apres API")
        best_move = next_move(plateau.turn,current_moves,api.color)
        if best_move is None:
            best_move = get_move_base_on_ai_level(ia_level,plateau,color_to_int(api.color))
            # print(f"API COLOR est {color_to_int(api.color)} et move est {best_move}")
            
        else:
            # print("°°°° OUVERTURE °°°°")
            best_move = chess_notation_to_move(best_move)
        if not api.make_move( move_to_chess_notation( best_move),is_my_turn):
            erreur += 1
            plateau.print_Board()
            
            #Serialize object
            log_Error(plateau,best_move)

            print(best_move)
            print("*************************************")
        if erreur == NOMBRE_ERREUR_AVANT_ARRET_JEU :
            exit()
        time.sleep(ONE_SEC_SLEEP_TIME)
        # print("SUITE")
    print(f"MATCH FINISHED: Winner is {api.winner}")
    stream_events_thread.join()
    stream_board_thread.join()

def play_against_player_o(ia_level):
    is_my_turn = threading.Event()
    plateau = Board2()
    api = Lichess()
    current_moves = []
    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    erreur = 0
    print("Waiting for a challenge !!!!")
    while(not api.game_started):
        time.sleep(QUICK_SLEEP_TIME)
    time.sleep(2)
    stream_board_thread = threading.Thread(target=api.stream_board_state, args=(is_my_turn,))
    stream_board_thread.start()
    
    while not api.game_started:
        time.sleep(QUICK_SLEEP_TIME)
    while not api.is_game_finished:
        print(is_my_turn.is_set())
        is_my_turn.wait()
        if api.is_game_finished:
            break
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # print("api.moves")
        # print(api.moves)
        moves_en_trop = elements_en_trop(current_moves, api.moves)
        current_moves.extend(moves_en_trop)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # print("tour est "+ str(plateau.turn))
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
        if api.is_game_finished:
            break
        best_move = next_move(plateau.turn,current_moves,api.color)
        if best_move is None:
            best_move = get_move_base_on_ai_level(ia_level,plateau,color_to_int(api.color))
            # print(f"API COLOR est {color_to_int(api.color)} et move est {best_move}")            
        else:
            best_move = chess_notation_to_move(best_move)
        if not api.make_move( move_to_chess_notation( best_move),is_my_turn):
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
    
def get_move_base_on_ai_level(ai_level,board,color_of_player_turn):
    match ai_level:
        case "0":
            move = mcts_rapide(board,color_of_player_turn)
        case "1":
            move = mcts(board,color_of_player_turn)
        case "2":
            move = genetic_algorithm_processus(board,color_of_player_turn)
        case "3":
            move = alpha_beta_search_mprocess_section(board,color_of_player_turn,1)
        case "4":
            move = alpha_beta_search_mprocess_section(board,color_of_player_turn,2)
    return move


