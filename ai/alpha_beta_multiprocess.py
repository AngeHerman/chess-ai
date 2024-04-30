import math
import copy
from multiprocessing import Pool
from chess.board2 import *
from ai.more import *

MAX_DEPTH = 2
NUM_PROCESSES = 6

def alpha_beta_search_mp(board, color):
    if color == BLANC:
        return max_value_multiProcess(board, 0, -math.inf, math.inf, MAX_DEPTH)
    else:
        return min_value_multiProcess(board, 0, -math.inf, math.inf, MAX_DEPTH)

def max_value_multiProcess(board, depth, alpha, beta, max_depth):
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    with Pool(processes=NUM_PROCESSES) as pool:
        results = []
        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            result = pool.apply_async(min_value, args=(copied_board, depth + 1, alpha, beta, max_depth))
            results.append((move, result))

        for move, result in results:
            current_value = result.get()
            if current_value > value:
                value = current_value
                best_move = move
            if value >= beta:
                # print("Elagué")
                break
            alpha = max(alpha, value)

    if depth == 0:
        return best_move
    else:
        return value

def min_value_multiProcess(board, depth, alpha, beta, max_depth):
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    with Pool(processes=NUM_PROCESSES) as pool:
        results = []
        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            result = pool.apply_async(max_value, args=(copied_board, depth + 1, alpha, beta, max_depth))
            results.append((move, result))

        for move, result in results:
            current_value = result.get()
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
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
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

def evaluate_board(board):
    color = BLANC if board.turn % 2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board.grille, color, board.endGame(), move_of_current_player)
