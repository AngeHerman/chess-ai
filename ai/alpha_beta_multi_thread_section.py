from concurrent.futures import ThreadPoolExecutor
import math
import copy
from chess.board2 import *
from ai.more import *

MAX_DEPTH = 2
NUM_THREADS = 6  # Nombre de threads à utiliser

def alpha_beta_search_mt_section(board, color):
    if color == BLANC:
        return max_value_multiThread(board, 0, -math.inf, math.inf, MAX_DEPTH)
    else:
        return min_value_multiThread(board, 0, -math.inf, math.inf, MAX_DEPTH)

def max_value_multiThread(board, depth, alpha, beta, max_depth):
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    # Divise l'arbre de recherche en sections
    sections = divide_tree(board.pMoves, NUM_THREADS)

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for section in sections:
            future = executor.submit(max_value_section, board, depth, alpha, beta, max_depth, section)
            futures.append(future)

        # Récupère les résultats de chaque section
        for future in futures:
            result = future.result()
            if result[0] > value:
                value = result[0]
                best_move = result[1]
            if value >= beta:
                break
            alpha = max(alpha, value)

    if depth == 0:
        return best_move
    else:
        return value
    
def min_value_multiThread(board, depth, alpha, beta, max_depth):
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    # Divise l'arbre de recherche en sections
    sections = divide_tree(board.pMoves, NUM_THREADS)

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for section in sections:
            future = executor.submit(min_value_section, board, depth, alpha, beta, max_depth, section)
            futures.append(future)

        # Récupère les résultats de chaque section
        for future in futures:
            result = future.result()
            if result[0] < value:
                value = result[0]
                best_move = result[1]
            if value >= beta:
                break
            beta = min(beta, value)

    if depth == 0:
        return best_move
    else:
        return value

def max_value_section(board, depth, alpha, beta, max_depth, section):
    value = -math.inf
    best_move = None
    for move in section:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = min_value(copied_board, depth + 1, alpha, beta, max_depth)
        if current_value > value:
            value = current_value
            best_move = move
        if value >= beta:
            break
        alpha = max(alpha, value)

    return value, best_move

def min_value_section(board, depth, alpha, beta, max_depth, section):
    value = -math.inf
    best_move = None

    for move in section:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = max_value(copied_board, depth + 1, alpha, beta, max_depth)
        if current_value < value:
            value = current_value
            best_move = move
        
        if value >= beta:
            break
        beta = min(beta, value)

    return value, best_move

def max_value(board, depth, alpha, beta,max_depth):
    # print("Arrivé dans max")
    if depth == max_depth or board.isGameEnded:
        # if board.isGameEnded:
        #     print(f"FIN :{evaluate_board(board)}")
        if depth == 0 and board.isGameEnded:
            print(f"°°°PRESQUE FIN mais on continue")
        else:
            # print(f"°°°°°°°°°°°°FIN depth est :{depth} et max depth est {max_depth}")
            return evaluate_board(board)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    for move in board.pMoves:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = min_value(copied_board, depth + 1, alpha, beta,max_depth)
        if current_value > value:
            value = current_value
            best_move = move
        # if move == ((5, 0), (3, 0)) and depth == 0:
        #     print(f"Vers 3,0 Move avec value :{value}")
        # if move == ((5, 0), (5, 2)) and depth == 0:
        #     print(f"Vers 5,2 Move avec value :{value}")
        if value >= beta:
            # if move == ((2, 2), (4, 3)):
            #     print(f"Elagué avec value :{value}")
            # if best_move == ((2, 1), (1, 2)):
            #     print(f"Elagué avec value :{value}")
            print("Elagué")
            break
        alpha = max(alpha, value)
        # if depth == max_depth -1:
        #     print(f"Depth: {depth}, Move: {move}, Value: {value}")
        # if alpha >= beta:
        #     break

    if depth == 0:
        # print(f"Le best move est :{best_move}")
        # board.print_Board()
        return best_move
    else:
        # print(f"Le best value est :{value}")
        return value

def min_value(board, depth, alpha, beta,max_depth):
    # print("Arrivé dans min")
    if depth == max_depth or board.isGameEnded:
        # if board.isGameEnded:
        #     print(f"FIN :{evaluate_board(board)}")
        if depth == 0 and board.isGameEnded:
            print(f"°°°PRESQUE FIN mais on continue")
        else:
            # print(f"°°°°°°°°°°°°FIN depth est :{depth} et max depth est {max_depth}")
            return evaluate_board(board)

    value = math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()


    for move in board.pMoves:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = max_value(copied_board, depth + 1, alpha, beta,max_depth)
        if current_value < value:
            value = current_value
            best_move = move
        if value <= alpha:
            break
        beta = min(beta, value)    

    if depth == 0:
        return best_move
    else:
        return value

# Fonction pour diviser les mouvements en sections
def divide_tree(moves, num_threads):
    num_moves = len(moves)
    section_size = math.ceil(num_moves / num_threads)
    sections = [moves[i:i+section_size] for i in range(0, num_moves, section_size)]
    return sections

# Les autres fonctions restent les mêmes que dans l'implémentation de base de l'algorithme alpha-beta

def evaluate_board(board):
    color = BLANC if board.turn%2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board.grille, color,board.endGame(),move_of_current_player)
