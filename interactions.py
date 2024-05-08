import threading
import os
import time
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
OUR_IA_LEVELS = ["0","1", "2", "3", "4"]
LICHESS_IA_LEVELS = ["1", "2", "3", "4","5", "6", "7", "8"]

def log_Error(plateau,errorMove):
    f = open("dump","w+b")
    logFile = open("log.txt","w+")

    pickle.dump(plateau,f)
    logFile.write(f"{plateau.pMoves} \n {errorMove}")

    f.close()
    logFile.close()

def play_game(is_my_turn, plateau, api, current_moves,ia_level):
    erreur = 0
    while not api.is_game_finished:
        is_my_turn.wait()
        if api.is_game_finished:
            break

        print("Current moves:")
        print(api.moves)

        moves_en_trop = elements_en_trop(current_moves, api.moves)
        current_moves.extend(moves_en_trop)

        for move in moves_en_trop:
            plateau.getAllMovesBasedOnTurn()
            if not plateau.play_move(chess_notation_to_move(move)):
                plateau.print_Board()
                print(f"The move {move} was not found.")
                print("Available moves:")
                print([move_to_chess_notation(move) for move in plateau.pMoves])
                log_Error(plateau, best_move)
                os._exit(1)

        best_move = next_move(plateau.turn, current_moves, api.color)
        if best_move is None:
            # best_move = alpha_beta_search_mprocess_section(plateau, color_to_int(api.color))
            best_move = get_move_base_on_ai_level(ia_level,plateau,color_to_int(api.color))

        else:
            best_move = chess_notation_to_move(best_move)

        if not api.make_move(move_to_chess_notation(best_move), is_my_turn):
            erreur += 1
            plateau.print_Board()
            log_Error(plateau, best_move)
            print(best_move)
            print("*************************************")

        if erreur == NOMBRE_ERREUR_AVANT_ARRET_JEU:
            exit()

        time.sleep(ONE_SEC_SLEEP_TIME)

    print(f"MATCH FINISHED: Winner is {api.winner}")

def play_against_ai(ia_level, lichess_level):
    is_my_turn = threading.Event()
    plateau = Board2()
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

    while not api.game_started:
        time.sleep(QUICK_SLEEP_TIME)

    open_game_in_browser(api.game_id)
    play_game(is_my_turn, plateau, api, current_moves,ia_level)

    stream_events_thread.join()
    stream_board_thread.join()

def play_against_player(ia_level):
    is_my_turn = threading.Event()
    plateau = Board2()
    api = Lichess()
    current_moves = []

    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    time.sleep(2)
    print("Waiting for a challenge ")
    while not api.game_started:
        time.sleep(QUICK_SLEEP_TIME)

    time.sleep(2)

    stream_board_thread = threading.Thread(target=api.stream_board_state, args=(is_my_turn,))
    stream_board_thread.start()

    while not api.game_started:
        time.sleep(QUICK_SLEEP_TIME)

    play_game(is_my_turn, plateau, api, current_moves,ia_level)
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

def choice_our_ai_againt_lichess_ai():
    print("Vous avez choisi de lancer notre IA contre celle de Lichess.")
    while True:
        ia_level = input(f"Entrez le niveau de notre IA {OUR_IA_LEVELS} : ")
        lichess_level = input(f"Entrez le niveau de Lichess {LICHESS_IA_LEVELS} : ")
        
        if ia_level in OUR_IA_LEVELS and lichess_level in LICHESS_IA_LEVELS:
            return ia_level, lichess_level
        else:
            print(f"Niveau invalide. Veuillez entrer {OUR_IA_LEVELS} pour le niveau de notre IA et {LICHESS_IA_LEVELS} pour le niveau de Lichess.")
            
def choice_play_againt_our_ai():
    print("Vous avez choisi de jouer contre notre IA.")    
    while True:
        ia_level = input(f"Entrez le niveau de notre IA {OUR_IA_LEVELS} : ")
        
        if ia_level in OUR_IA_LEVELS:
            return ia_level
        else:
            print(f"Niveau invalide. Veuillez entrer {OUR_IA_LEVELS} pour le niveau de notre IA")

def menu():
    while True:
        print("Menu:")
        print("1. Jouer contre notre IA")
        print("2. Lancer notre IA contre celle de Lichess")
        print("3. Lancer des tests")
        print("4. Quitter")
        choice = input("Entrez votre choix (1, 2, 3 ou 4) : ")

        if choice == "1":
            ia_level = choice_play_againt_our_ai()
            play_against_player(ia_level)
            break
        elif choice == "2":
            ia_level, lichess_level = choice_our_ai_againt_lichess_ai()
            play_against_ai(ia_level, lichess_level)
            break
        elif choice == "3":
            print("Vous avez choisi de lancer des tests.")
            break
        elif choice == "4":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")

