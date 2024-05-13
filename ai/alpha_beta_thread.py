import threading
import math
import copy
from chess.board2 import *
from ai.more import *

MAX_DEPTH = 2
NUM_THREADS = 6

class AlphaBetaThread(threading.Thread):
    def __init__(self, board, color, depth, alpha, beta, max_depth, result):
        super().__init__()
        self.board = board
        self.color = color
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.max_depth = max_depth
        self.result = result

    def run(self):
        if self.color == BLANC:
            value = self.max_value(self.board, self.depth, self.alpha, self.beta, self.max_depth)
        else:
            value = self.min_value(self.board, self.depth, self.alpha, self.beta, self.max_depth)
        self.result.append(value)

    def max_value(self, board, depth, alpha, beta, max_depth):
        if depth == max_depth or board.isGameEnded:
            return evaluate_board(board)

        value = -math.inf
        board.getAllMovesBasedOnTurn()

        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            current_value = self.min_value(copied_board, depth + 1, alpha, beta, max_depth)
            value = max(value, current_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value

    def min_value(self, board, depth, alpha, beta, max_depth):
        if depth == max_depth or board.isGameEnded:
            return evaluate_board(board)

        value = math.inf
        board.getAllMovesBasedOnTurn()

        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            current_value = self.max_value(copied_board, depth + 1, alpha, beta, max_depth)
            value = min(value, current_value)
            beta = min(beta, value)
            if alpha >= beta:
                break

        return value

def alpha_beta_search_mt_manual(board, color):
    result = []
    threads = []
    if color == BLANC:
        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            thread = AlphaBetaThread(copied_board, color, 0, -math.inf, math.inf, MAX_DEPTH, result)
            threads.append(thread)
    else:
        for move in board.pMoves:
            copied_board = copy.deepcopy(board)
            copied_board.play_move(move)
            thread = AlphaBetaThread(copied_board, color, 0, -math.inf, math.inf, MAX_DEPTH, result)
            threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def evaluate_board(board):
    color = BLANC if board.turn % 2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board, color, board.endGame(), move_of_current_player)

