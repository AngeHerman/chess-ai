from ai.opening import *
from chess.constants import *
from chess.utils import *

SCORE_POINT_FOR_KING_PROTECTION = 1
SCORE_POINT_FOR_MID_CONTROL = 2
THREAT_MULTIPLICATOR = 1/3

PION_BLANC_POINT = 1
TOUR_BLANC_POINT = 50
CAVALIER_BLANC_POINT = 37
FOU_BLANC_POINT = 50
DAME_BLANCHE_POINT = 70
ROI_BLANC_POINT = 100

PION_NOIR_POINT = -1
TOUR_NOIR_POINT = -50
CAVALIER_NOIR_POINT = -37
FOU_NOIR_POINT= -50
DAME_NOIRE_POINT = -70
ROI_NOIR_POINT = -100

scores_pieces = {
    PION: {BLANC: PION_BLANC_POINT, NOIR: PION_NOIR_POINT},
    CAVALIER: {BLANC: CAVALIER_BLANC_POINT, NOIR: CAVALIER_NOIR_POINT},
    FOU: {BLANC: FOU_BLANC_POINT, NOIR: FOU_NOIR_POINT},
    TOUR: {BLANC: TOUR_BLANC_POINT, NOIR: TOUR_NOIR_POINT},
    DAME: {BLANC: DAME_BLANCHE_POINT, NOIR: DAME_NOIRE_POINT},
    ROI: {BLANC: ROI_BLANC_POINT, NOIR: ROI_NOIR_POINT }
}


def bonus_center_control(row_index, color):
    center_rows = [3, 4]
    score_bonus = 0
    if row_index in center_rows:
        if color == BLANC:
            score_bonus += SCORE_POINT_FOR_MID_CONTROL
        else:
            score_bonus -= SCORE_POINT_FOR_MID_CONTROL
    return score_bonus

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
    
    #####
    score_total = 0
    for row_index, row in enumerate(board):
        for col_index, piece in enumerate(row):
            if piece is not None:
                score_total += scores_pieces[piece.name][piece.color]
                if piece.name == ROI:
                    score_total += bonus_kings_protection(board, row_index, col_index, piece.color)
                score_total += bonus_center_control(row_index,piece.color)
    # print("Fin Evaluation")
    
    return score_total

def threat_score(board):
    return threat_score_by_color(board,BLANC)+threat_score_by_color(board,NOIR)

def threat_score_by_color(board,color):
    score_threat = 0
    my_threatened_cases =  getThreatenedCases(board, color)
    for case in my_threatened_cases:
        piece = getPiece(board,case[1])
        if piece is not None and piece.color == color:
            score_threat += int(scores_pieces[piece.name][piece.color]*THREAT_MULTIPLICATOR)
            
    # The white want to maximise the score and the score for their threatened case needs to be negative cause its bad for them. The opposite for black.  
    return -score_threat