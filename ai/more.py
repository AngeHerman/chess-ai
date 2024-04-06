from ai.opening import *
import random
from chess.constants import *
from chess.utils import *

SCORE_POINT_FOR_KING_PROTECTION = 1
def random_between_a_and_min_bc(a, b, c):
    min_bc = min(b, c)
    return random.randint(a, min_bc)

def can_pick_a_move(turn, current_moves,color):
    if turn == 1:
        return True
    else:
        if(color == "white"):
            return next_moves_exists_in_openings(current_moves,white_openings)
        else: return next_moves_exists_in_openings(current_moves,black_openings)

def next_moves_exists_in_openings(moves, openings):
    for opening in openings:
        if len(moves) >= len(opening):
            continue
        i = 0
        while(i < len(moves)):
            if moves[i] != opening[i]:
                return False
            i += 1
    return True

def next_move(turn,current_moves,color):
    openings = white_openings
    next_mv = None
    if color == "black":
        openings = black_openings
    if turn == 1 and color == "white":
        opn = openings[random_between_a_and_min_bc(0,len(white_openings),len(black_openings))]
        return opn[0]
    for opening in openings:
        if len(current_moves) >= len(opening):
            continue
        i = 0
        while(i < len(current_moves)):
            if current_moves[i] != opening[i]:
                break
            i += 1
        if i == len(current_moves):
            next_mv = opening[i]
            break
    return next_mv

def bonus_kings_protection(board, row_index, col_index, king_color):
    score_bonus = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dy == 0 and dx == 0:
                continue  # Skip la king case
            new_row_index = row_index + dy
            new_col_index = col_index + dx
            if areCoordinatesBounded(new_row_index, new_col_index):
                adjacent_piece = board[new_row_index][new_col_index]
                if adjacent_piece is not None and adjacent_piece.color == king_color:
                    if king_color == BLANC:
                        score_bonus += SCORE_POINT_FOR_KING_PROTECTION
                    else : score_bonus += (-SCORE_POINT_FOR_KING_PROTECTION)
    return score_bonus

def board_score(board):
    # print("Debut Evaluation")
    scores_pieces = {
        PION: {BLANC: PION_BLANC, NOIR: PION_NOIR},
        CAVALIER: {BLANC: CAVALIER_BLANC, NOIR: CAVALIER_NOIR},
        FOU: {BLANC: FOU_BLANC, NOIR: FOU_NOIR},
        TOUR: {BLANC: TOUR_BLANC, NOIR: TOUR_NOIR},
        DAME: {BLANC: DAME_BLANCHE, NOIR: DAME_NOIRE},
        ROI: {BLANC: 100, NOIR: -100}
    }
    #####
    score_total = 0
    for row_index, row in enumerate(board):
        for col_index, piece in enumerate(row):
            if piece is not None:
                score_total += scores_pieces[piece.name][piece.color]
                if piece.name == ROI:
                    score_total += bonus_kings_protection(board, row_index, col_index, piece.color)
    # print("Fin Evaluation")
    
    return score_total