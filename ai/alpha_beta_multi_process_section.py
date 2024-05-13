from multiprocessing import Pool
import math
import copy
from chess.board2 import *
from ai.more import *

MAX_DEPTH = 2
NUM_PROCESSES = 4

def alpha_beta_search_mprocess_section(board, color, max_depth = MAX_DEPTH):
    if color == BLANC:
        return max_value_multi_process(board, 0, -math.inf, math.inf, max_depth,color)
    else:
        return min_value_multi_process(board, 0, -math.inf, math.inf, max_depth,color)

def abmps(board, color, max_depth):
    if color == BLANC:
        return max_value_multi_process(board, 0, -math.inf, math.inf, max_depth,color)
    else:
        return min_value_multi_process(board, 0, -math.inf, math.inf, max_depth,color)

def max_value_multi_process(board, depth, alpha, beta, max_depth,my_color):
    print("ON MAXIMISE")
    
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    sections = divide_tree(board.pMoves, NUM_PROCESSES)
    # for section in sections:
    #     print("SECTION")
    #     print(len(section))
    #     print(section)

    with Pool(processes=NUM_PROCESSES) as pool:
        results = []
        for section in sections:
            result = pool.apply_async(max_value_section, args=(board, depth, alpha, beta, max_depth,section,my_color))
            results.append(result)

        for result in results:
            current_value = result.get()
            if current_value[0] > value:
                value = current_value[0]
                best_move = current_value[1]
            if value >= beta:
                break
            alpha = max(alpha, value)

    if depth == 0:
        return best_move
    else:
        return value
    
def min_value_multi_process(board, depth, alpha, beta, max_depth,my_color):
    print("ON MINIMISE")
    if depth == max_depth or board.isGameEnded:
        return evaluate_board(board)

    value = math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    sections = divide_tree(board.pMoves, NUM_PROCESSES)
    # for section in sections:
    #     print("SECTION")
    #     print(len(section))
    #     print(section)
    with Pool(processes=NUM_PROCESSES) as pool:

        results = []
        for section in sections:
            result = pool.apply_async(min_value_section, args=(board, depth, alpha, beta, max_depth,section,my_color))
            results.append(result)

        for result in results:
            current_value = result.get()
            if current_value[0] < value:
                value = current_value[0]
                best_move = current_value[1]
            if value <= alpha:
                break
            beta = min(beta, value)

    if depth == 0:
        return best_move
    else:
        return value

def max_value_section(board, depth, alpha, beta, max_depth, section,my_color):
    value = -math.inf
    best_move = None
    for move in section:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = min_value(copied_board, depth + 1, alpha, beta, max_depth,my_color)
        if current_value > value:
            value = current_value
            best_move = move
        if value >= beta:
            break
        alpha = max(alpha, value)

    return value, best_move

def min_value_section(board, depth, alpha, beta, max_depth, section,my_color):
    
    value = math.inf
    best_move = None
    # print(section)
    for move in section:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = max_value(copied_board, depth + 1, alpha, beta, max_depth,my_color)

        if current_value < value:
            value = current_value
            best_move = move
        if value <= alpha:
            break
        beta = min(beta, value)

    return value, best_move

def max_value(board, depth, alpha, beta,max_depth,my_color):
    # print("Arrivé dans max")
    if depth == max_depth or board.isGameEnded:
        if depth == 0 and board.isGameEnded:
            print(f"°°°PRESQUE FIN mais on continue")
        else:
            return evaluate_board(board)

    value = -math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()

    for move in board.pMoves:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = min_value(copied_board, depth + 1, alpha, beta,max_depth,my_color)
        if current_value > value:
            value = current_value
            best_move = move
            
        if value >= beta:
            break
        alpha = max(alpha, value)

    if depth == 0:
        return best_move
    else:
        return value

def min_value(board, depth, alpha, beta,max_depth,my_color):
    # print("Arrivé dans min")
    if depth == max_depth or board.isGameEnded:
        if depth == 0 and board.isGameEnded:
            print(f"°°°PRESQUE FIN mais on continue")
        else:
            return evaluate_board(board)

    value = math.inf
    best_move = None
    board.getAllMovesBasedOnTurn()


    for move in board.pMoves:
        copied_board = copy.deepcopy(board)
        copied_board.play_move(move)
        current_value = max_value(copied_board, depth + 1, alpha, beta,max_depth,my_color)
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

def divide_tree(moves, num_threads):
    num_moves = len(moves)
    section_size = math.ceil(num_moves / num_threads)
    sections = [moves[i:i+section_size] for i in range(0, num_moves, section_size)]
    return sections

def evaluate_board(board):
    color = BLANC if board.turn%2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board, color,board.endGame(),move_of_current_player)

def evaluate_board_v2(board,my_color):
    color = BLANC if board.turn%2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    if board.turn < TURN_NUMBER_FOR_OPENING:
        return opening_strategy(board, color,board.endGame(),move_of_current_player,my_color)
    else:
        return board_score(board, color,board.endGame(),move_of_current_player)
    # return opening_strategy(board, color,board.endGame(),move_of_current_player,my_color)
