from concurrent.futures import ThreadPoolExecutor
import math
import copy
from chess.board2 import *
from ai.more import *

import math
import copy

MAX_DEPTH = 2
NUM_THREADS = 6

def alpha_beta_multithread_no_copy(board, color):
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

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            future = executor.submit(min_value, copied_board, depth + 1, alpha, beta, max_depth)
            futures.append((move, future))

        for move, future in futures:
            current_value = future.result()
            # print(f"Resultat arrivé {move_to_chess_notation(move)}: {current_value}")
            if current_value > value:
                value = current_value
                best_move = move
            if value >= beta:
                print("Elagué")
                break
            alpha = max(alpha, value)

    if depth == 0:
        return best_move
    else:
        return value

def min_value_multiThread(board, depth, alpha, beta, max_depth):
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for move in board.pMoves:
            copied_board = Board2()
            play_all_moves(copied_board,board.moves_until_now)
            copied_board.force_play_move(move)
            future = executor.submit(max_value, copied_board, depth + 1, alpha, beta, max_depth)
            futures.append((move, future))

        for move, future in futures:
            current_value = future.result()
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
        copied_board = Board2()
        play_all_moves(copied_board,board.moves_until_now)
        copied_board.force_play_move(move)
        current_value = min_value(copied_board, depth + 1, alpha, beta,max_depth)
        if current_value > value:
            value = current_value
            best_move = move
        if value >= beta:
            break
        alpha = max(alpha, value)


    if depth == 0:
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
        copied_board = Board2()
        play_all_moves(copied_board,board.moves_until_now)
        copied_board.force_play_move(move)
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

def evaluate_board(board):
    color = BLANC if board.turn % 2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board.grille, color, board.endGame(), move_of_current_player)

def play_all_moves(board,moves):
    for move in moves:
        board.force_play_move(move)