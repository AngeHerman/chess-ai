from ai.opening import *
from chess.constants import *
from chess.utils import *
from chess.pawn import *
from chess.knight import *

SCORE_POINT_FOR_KING_PROTECTION = 2
SCORE_POINT_FOR_MID_CONTROL = 1
PWAN_SCORE_POINT_FOR_MID_CONTROL = 1
THREAT_MULTIPLICATOR = 1/3
THREAT_MULTIPLICATOR_FOR_MY_PIECE_OPPONENT_CAN_POTENTILLY_CATCH = 1/8

SCORE_MULTIPLICATOR_FOR_WINNER = 100000000

TURN_NUMBER_FOR_OPENING = 10
SCORE_POINT_FOR_ROQUE_POSSIBLILITY = 15
SCORE_POINT_FOR_KNIGHT_OUT = 9

DEVELOPPEMENT_MULTIPLICATOR = 1/2

PION_BLANC_POINT = 1
TOUR_BLANC_POINT = 50
CAVALIER_BLANC_POINT = 37
FOU_BLANC_POINT = 50
DAME_BLANCHE_POINT = 90
ROI_BLANC_POINT = 160

PION_NOIR_POINT = -1
TOUR_NOIR_POINT = -50
CAVALIER_NOIR_POINT = -37
FOU_NOIR_POINT= -50
DAME_NOIRE_POINT = -90
ROI_NOIR_POINT = -160

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

def bonus_kings_protection(board, king_piece):
    surrounding = board.getKingSurrondings(king_piece)
    protection_list = board.getKingProtectionList(surrounding)
    score_bonus = len(protection_list)* SCORE_POINT_FOR_KING_PROTECTION
    if king_piece.color == NOIR:
        score_bonus = -score_bonus
    return score_bonus

def development_score(board,my_color):
    dev_score = 0
    # Move is all our moves
    moves = board.getAllAvailableMoves(my_color)
    dev_score += (len(moves) * DEVELOPPEMENT_MULTIPLICATOR)
    return dev_score

# Mid et end-game strategy
def board_score(board, color_of_player_turn,gagnant,move_of_current_player):
    # print("Debut Evaluation")
    
    #####
    score_total = 0
    for row_index, row in enumerate(board.grille):
        for col_index, piece in enumerate(row):
            if piece is not None:
                score_total += scores_pieces[piece.name][piece.color]
                if piece.name == ROI:
                    score_total += bonus_kings_protection(board, piece)
                score_total += bonus_center_control(row_index,piece.color)
    # print("Fin Evaluation")
    #We add the threat score for all case the actual player is threatning
    # score_total += threat_score_by_color(board,getAdvesaryColor(color_of_player_turn),move_of_current_player) 
    
    score_total += threat_score(board.grille,color_of_player_turn,move_of_current_player)
    if gagnant != 0:
        score_total += (gagnant * SCORE_MULTIPLICATOR_FOR_WINNER)
    return score_total

def board_score_without_threat(board):
    score_total = 0
    for row_index, row in enumerate(board.grille):
        for col_index, piece in enumerate(row):
            if piece is not None:
                score_total += scores_pieces[piece.name][piece.color]
                if piece.name == ROI:
                    score_total += bonus_kings_protection(board, piece)
                score_total += bonus_center_control(row_index,piece.color)
    return score_total
    

def threat_score(board,color_of_player_turn,move_of_current_player):
    return threat_score_by_color(board,getAdvesaryColor(color_of_player_turn),move_of_current_player) + threat_score_opponent(board,color_of_player_turn)

# Return the score of how the actual player can threat the opponent case
def threat_score_by_color(board,color_of_opponent,move_of_current_player):
    score_threat = 0
    # A list of already seen case
    temp = []
    for move in move_of_current_player:
        if move[1] not in temp:
            piece = getPiece(board,move[1])
            if piece is not None and piece.color == color_of_opponent:
                score_threat += int(scores_pieces[piece.name][piece.color]*THREAT_MULTIPLICATOR)
            temp.append(move[1])
            
    # The white want to maximise the score and the score for their threatened case needs to be negative cause its bad for them. The opposite for black.  
    return -score_threat

# Return the potential threat score of opponent knowing it's not the opponent turn so we are actually guessing. We are saying it's the turn of the other player but it's not
def threat_score_opponent(board,color_of_player_turn):
    score_threat = 0
    # A list of already seen case
    temp = []
    # The potential opponent moves that threat my piece
    opponent_moves_that_threat_my_case =  getThreatenedCasesWithKing(board,color_of_player_turn)
    for move in opponent_moves_that_threat_my_case:
        # if move in move_of_current_player
        if move[1] not in temp:
            piece = getPiece(board,move[1])
            if piece is not None and piece.color == color_of_player_turn:
                score_threat += int(scores_pieces[piece.name][piece.color]*THREAT_MULTIPLICATOR_FOR_MY_PIECE_OPPONENT_CAN_POTENTILLY_CATCH)
            temp.append(move[1])
    return -score_threat

def roque_score(board,my_color):
    if not board.check_petit_roque(my_color):
        return 0
    if my_color == BLANC:
        return SCORE_POINT_FOR_ROQUE_POSSIBLILITY
    else:
        return - SCORE_POINT_FOR_ROQUE_POSSIBLILITY

def central_pawn_defense_score(board):
    row_d4,col_d4 = chess_notation_to_cell("d4")
    row_e4,col_e4 = chess_notation_to_cell("e4")
    row_d5,col_d5 = chess_notation_to_cell("d5")
    row_e5,col_e5 = chess_notation_to_cell("e5")
    total_score = 0
    for row_index, row in enumerate(board.grille):
        for col_index, piece in enumerate(row):
            if piece is not None and isinstance(piece, Pawn):
                # pion Blanc en d4 ou e4
                if piece.color == BLANC and (col_index == col_d4 or col_index == col_e4) and row_index == row_d4:
                    total_score += PWAN_SCORE_POINT_FOR_MID_CONTROL
                # pion Noir en d5 ou e5
                elif piece.color == NOIR and (col_index == col_d5 or col_index == col_e5) and row_index == row_d5:
                    total_score -= PWAN_SCORE_POINT_FOR_MID_CONTROL
    return total_score

def knight_out_score(board, my_color):
    score = 0
    for row_index, row in enumerate(board.grille):
        for col_index, piece in enumerate(row):
            if piece is not None and isinstance(piece, Knight) and piece.color == my_color:
                if piece.moveCount > 0:
                    score += SCORE_POINT_FOR_KNIGHT_OUT
    if my_color == NOIR:
        score = -score
    return score
    
def opening_strategy(board, color_of_player_turn,gagnant,move_of_current_player,my_color):
    score = 0
    score += board_score_without_threat(board)
    # score += board_score(board,color_of_player_turn,gagnant,move_of_current_player)
    score += roque_score(board,my_color)
    score += central_pawn_defense_score(board)
    score += knight_out_score(board,my_color)
    return score