from chess.board2 import *
from ai.more import *

import random
import math
import copy

MAX_DEPTH = 3

def alpha_beta_search(board, color):
    if color == BLANC:
        return max_value(board, MAX_DEPTH, -math.inf, math.inf)
    else:
        return min_value(board, MAX_DEPTH, -math.inf, math.inf)

def max_value(board, depth, alpha, beta):
    # print("Arrivé dans max")
    if depth == 0 or board.isGameEnded:
        return evaluate_board(board.grille)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    for move in board.pMoves:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = min_value(copied_board, depth - 1, alpha, beta)
        if current_value > value:
            value = current_value
            best_move = move
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    if depth == MAX_DEPTH:
        return best_move
    else:
        return value

def min_value(board, depth, alpha, beta):
    # print("Arrivé dans min")
    if depth == 0 or board.isGameEnded:
        return evaluate_board(board.grille)

    value = math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()


    for move in board.pMoves:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = max_value(copied_board, depth - 1, alpha, beta)
        if current_value < value:
            value = current_value
            best_move = move
        beta = min(beta, value)
        if alpha >= beta:
            break

    if depth == MAX_DEPTH:
        return best_move
    else:
        return value

def evaluate_board(board):
    return board_score(board)
