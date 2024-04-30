from chess.board2 import *
from ai.more import *

import random
import math
import copy

MAX_DEPTH = 2

def alpha_beta_search(board, color):
    if color == BLANC:
        return max_value(board, 0, -math.inf, math.inf,MAX_DEPTH)
    else:
        return min_value(board, 0, -math.inf, math.inf,MAX_DEPTH)

def ab(board, color, max_depth):
    if color == BLANC:
        return max_value(board, 0, -math.inf, math.inf,max_depth)
    else:
        return min_value(board, 0, -math.inf, math.inf,max_depth)

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
            # print("Elagué")
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
        # if move == ((4, 1), (2, 2)):
        #         print(f"(4, 1), (2, 2) trouvé avec value :{value}")
        if value <= alpha:
            break
        beta = min(beta, value)
        # if depth == max_depth - 1:
        #     print(f"Depth: {depth}, Move: {move}, Value: {value}")
        # if alpha >= beta:
        #     break
    

    if depth == 0:
        # print(f"Le best move est :{best_move}")
        return best_move
    else:
        # print(f"Le best value est :{value}")
        return value

def evaluate_board(board):
    color = BLANC if board.turn%2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board.grille, color,board.endGame(),move_of_current_player)






