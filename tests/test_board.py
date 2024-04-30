from chess.board2 import *
from chess.utils import *
from chess.king import *
from ai.alpha_beta import *
import pickle


def test_knightMovement(coord):
    plateau = Board2()
    addPieceToCase(plateau.grille,coord,CAVALIER_NOIR)

    movements = [(coord[0] + 2,coord[1] + 1),(coord[0]+2,coord[1]-1),(coord[0]-2,1),(coord[0]-2,coord[1]-1),(coord[0]+1,coord[1] + 2),(coord[0]+1,coord[1]-2),(coord[0]-1,coord[1]+2),(coord[0]-1,coord[1]-2)]
    movementList = plateau.knight_movement(coord)
    movementList = [movementList[i][1] for i in range(len(movementList))]

    check = True

    for i in range(len(movements)):
        if not (movements[i] in movements):
            check = False

    assert(check)


def test_bishopMovement(coord):
    plateau = Board2()
    addPieceToCase(plateau.grille,coord,FOU_NOIR)

    movements = [(coord[0] + 1, coord [1] + 1),(coord[0] - 1, coord [1] - 1),(coord[0]- 1, coord [1] + 1),(coord[0] + 1, coord [1] - 1)]

    movementList = plateau.bishop_movement(coord,2)
    movementList = [movementList[i][1] for i in range(len(movementList))]

    print(movementList)
    check = True

    for i in range(len(movements)):
        if not (movements[i] in movements):
            check = False

    assert(check)


def test_rookMovement(coord):
    plateau = Board2()
    addPieceToCase(plateau.grille,coord,TOUR_NOIR)

    movements = [(coord[0] + 1, coord [1]),(coord[0] - 1, coord [1]),(coord[0], coord [1] + 1),(coord[0], coord [1] - 1)]

    movementList = plateau.rook_movement(coord,2,2)
    movementList = [movementList[i][1] for i in range(len(movementList))]

    print(movementList)
    check = True

    for i in range(len(movements)):
        if not (movements[i] in movements):
            check = False

    assert(check)

    
def test_queenMovement(coord):
    pass

"""D'autres tests sont à rajoutés pour le roi ..."""
def test_kingMovement(coord):
    
    plateau = Board2()

    """Test des mouvements du roi lorsque pièce est protégé"""
    queenCoordinates = (coord[0]-1,coord[1])

    addPieceToCase(plateau.grille,coord,ROI_NOIR)
    addPieceToCase(plateau.grille,(coord[0]-2,coord[1]),TOUR_BLANC)
    addPieceToCase(plateau.grille,queenCoordinates,DAME_BLANCHE)

    movementList = plateau.king_movement(coord)
    movementList = [movementList[i][1] for i in range(len(movementList))]    

    assert(not queenCoordinates in movementList)

def test_allMovementsAvailable():

    plateau = Board2()

    print(plateau.getAllAvailableMoves(NOIR))
    plateau.print_Board()



def test_specificSituation():
    
    plateau = Board2()
    """plateau.force_play_move(((7,1),(5,2)))
    plateau.force_play_move(((6,4),(5,4)))
    plateau.force_play_move(((1,3),(3,3)))
    plateau.force_play_move(((1,4),(3,4)))
    plateau.force_play_move(((0,6),(2,5)))
    
    print(plateau.grille[7][3].king_movement(plateau.grille))
    emptyCase(plateau.grille,(7,1))
    plateau.force_play_move(((0,4),(3,5)))
    plateau.force_play_move(((7,6),(4,5)))
    plateau.force_play_move(((7,3),(6,5)))"""

    plateau.force_play_move(((7,3),(6,3)))
    plateau.force_play_move(((1,3),(4,3)))
   
    plateau.print_Board()

    print(plateau.getAllAvailableMoves(NOIR))


def test_dumpFile():
    plateau = Board2()

    f = open("dump","r+b")
    pla = pickle.load(f)
    f.close()

    print(pla.getAllAvailableMoves(NOIR))
    pla.print_Board()

def test_petit_roque():
    print("###### TEST PETIT ROQUE ######")
    plateau = Board2()
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "d2d3", "g8f6", "c1e3", "f8e7", "b1c3", "d7d6", "f1e2", "e8g8", "e1g1"]

    plateau.print_Board()
    for m in moves:
        print(m)
        plateau.getAllMovesBasedOnTurn()
        ans = plateau.play_move(chess_notation_to_move(m))
        if ans :
            print("TRUE")
        else:
            print("FALSE")
        plateau.print_Board()

def test_grand_roque():
    print("###### TEST GRAND ROQUE ######")
    plateau = Board2()
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "d2d3", "g8f6", "c1e3", "f8e7", "b1c3", "d7d6", "f1e2", "c8e6","d1d2","d8d7","e1c1","e8c8"]



    plateau.print_Board()
    for m in moves:
        print(m)
        plateau.getAllMovesBasedOnTurn()
        ans = plateau.play_move(chess_notation_to_move(m))
        if ans :
            print("TRUE")
        else:
            print("FALSE")
        plateau.print_Board()
    
    
    
def test_promotion():
    print("###### TEST PROMOTION ######")
    plateau = Board2()
    moves = ["e2e4", "d7d5", "e4d5", "d8d6", "d2d4", "c7c5", "d4c5", "b7b6", "c5b6", "a7a5", "b6b7", "b8a6", "b7b8q"]
    
    # moves_prom_prise = ["e2e4", "d7d5", "e4d5", "d8d6", "d2d4", "c7c5", "d4c5", "b7b6", "c5b6", "a7a5", "b6b7", "a5a4", "b7a8q"]

    print(chess_notation_to_move("b7b8q"))
    print(len(chess_notation_to_move("b7b8q"))) 
    plateau.print_Board()
    for m in moves:
        print(m)
        plateau.getAllMovesBasedOnTurn()
        ans = plateau.play_move(chess_notation_to_move(m))
        if ans :
            print("TRUE")
        else:
            print("FALSE")
            print(plateau.pMoves)
        plateau.print_Board()
def test_endGame():
    plateau = Board2()
    plateau.grille = [[ Rook(NOIR), None, None , King(BLANC), None ,None , None , None],
        [Rook(NOIR), None, None, None, None,None,None,None],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [Pawn(NOIR),None,Pawn(NOIR),Pawn(NOIR),None,Pawn(NOIR),None,Pawn(NOIR)],
        [None,Knight(NOIR), None,  King(NOIR), Queen(NOIR), None, Knight(NOIR), None]]
    plateau.initializeCoordinates()
    print(f"Fin : {plateau.endGame()}")


def test_ia():
    print("###### TEST IA ######")
    plateau = Board2()
    plateau.grille = [
        [Rook(BLANC), Knight(BLANC), Bishop(BLANC),  None, Queen(BLANC), Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None,King(BLANC),None,None,None,None,None,None],
        [Pawn(NOIR),None,Pawn(NOIR),Pawn(NOIR),None,Pawn(NOIR),None,Pawn(NOIR)],
        [Rook(NOIR),Knight(NOIR), None,  King(NOIR), Queen(NOIR), None, Knight(NOIR), None]
    ]
    plateau.initializeCoordinates()
    plateau.getAllMovesBasedOnTurn()
    plateau.turn += 1
    plateau.print_Board()
    move = alpha_beta_search(plateau,NOIR)
    print(f"Move : {move}")
    print(f"Fin : {plateau.isGameEnded}")
    plateau.play_move(move)
    plateau.print_Board()
    print(f"Fin : {plateau.isGameEnded}")
    
def test_situation():
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'g8f6', 'f1b5', 'f8d6', 'b5d7', 'f6d7', 'b1a3', 'd7f6', 'f3e5', 'f6e4', 'd1h5', 'e8g8','h5h7']
    
    for m in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( m))
    plateau.print_Board()
    print(f"Score : {board_score(plateau.grille)}")
    plateau.getAllMovesBasedOnTurn()
    print(plateau.pMoves)
    print("Après avoir chopé la reine")
    plateau.play_move(chess_notation_to_move('g8h7'))
    plateau.print_Board()
    print(f"Score : {board_score(plateau.grille)}")
    
def test_situation2():
    # https://lichess.org/t38xyv6Y#14
    # https://lichess.org/ZVKmtd6A
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'g8f6', 'f1b5', 'f8d6', 'b5d7', 'f6d7', 'b1a3', 'd7f6', 'f3e5', 'f6e4', 'd1h5', 'e8g8']
    
    for m in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( m))
    plateau.print_Board()
    print(f"Score : {board_score(plateau.grille)}")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {board_score(plateau.grille)}")
    # print("Case blanches menacés")
    # my_threatened_cases =  getThreatenedCases(plateau.grille, BLANC)
    # for case in my_threatened_cases:
    #     print(case[1])
    # print("Case noires menacés")
    # other_threatened_cases =  getThreatenedCases(plateau.grille, NOIR)
    # for case in other_threatened_cases:
    #     print(case[1])
    # print(f"Threat score blanc :{threat_score_by_color(plateau.grille,BLANC)}")
    # print(f"Threat score noire :{threat_score_by_color(plateau.grille,NOIR)}")
    
    
    m = alpha_beta_search(plateau,NOIR)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move( m) )
    plateau.print_Board()
    print(f"Score : {board_score(plateau.grille)}")
    
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move( m) )
    plateau.print_Board()
    print(f"Score : {board_score(plateau.grille)}")
    
    
def test_situation2_1():
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'g8f6', 'f1b5', 'f8d6', 'b5d7', 'f6d7', 'b1a3', 'd7f6', 'f3e5', 'f6e4', 'd1h5', 'e8g8']
    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,2)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,BLANC,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
        





# ['e2e4', 'd7d5', 'g1h3', 'b8c6', 'h1g1', 'h7h5', 'g1h1', 'g7g6', 'h1g1', 'g8f6', 'g1h1', 'e7e5', 'b1a3', 'f8a3', 'h1g1', 'a3d6', 'a2a3', 'f6e4', 'h3f4', 'd6c5', 'f4e2', 'c6b4', 'a3a4', 'd8h4', 'g1h1', 'c8g4', 'h1g1', 'a7a5', 'g1h1', 'e8g8', 'h1g1', 'b7b5', 'g1h1', 'b5a4', 'h1g1', 'a4a3', 'g1h1', 'a5a4', 'h1g1', 'c7c6', 'g1h1', 'c5e3', 'h1g1', 'e4d2', 'g1h1', 'e5e4', 'h1g1', 'd5d4', 'g1h1', 'd4d3', 'h1g1', 'c6c5', 'g1h1', 'f7f6', 'h1g1', 'f8d8', 'g1h1', 'g4f3', 'g2g4', 'g8h7', 'h1g1', 'g6g5', 'g1g2', 'e3f2', 'e1d2', 'a3b2', 'g2g1', 'f2e1', 'd2e3', 'f6f5', 'g1g2', 'h5g4', 'a1a2', 'f5f4', 'e2f4', 'a4a3', 'f4e2', 'd8f8', 'd1d3', 'f8d8']

# ['c2c4', 'e7e5', 'b1a3', 'b8c6', 'd1c2', 'g8f6', 'g1f3', 'b7b6', 'h1g1', 'e5e4']

def test_situation3():
    # https://lichess.org/MjO5rn0A/white#10
    plateau = Board2()
    moves = ['c2c4', 'e7e5', 'b1a3', 'b8c6', 'd1c2', 'g8f6', 'g1f3', 'b7b6', 'h1g1', 'e5e4']
    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    # m = ab(plateau,BLANC,1)
    # print(m)
    # print(move_to_chess_notation(m))
    # print(plateau.play_move(m) )
    # plateau.print_Board()
    # print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    
    
def test_situation4():
    # https://lichess.org/yGrWy1er/white#22
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5d3', 'd7d6', 'f3g1', 'g8f6', 'g1h3', 'h7h6', 'h1g1', 'g7g6', 'g1f1', 'c8e6', 'b2b3', 'd6d5', 'b1a3', 'e6g4', 'd3e2', 'g4e2']

    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))


def test_situation5():
    # https://lichess.org/aN9lxruU/white#72
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'd7d6', 'f3g1', 'b8c6', 'h2h3', 'd8h4', 'h1h2', 'h4e4', 'g1e2', 'd6d5', 'b1a3', 'f8c5', 'a1b1', 'e4f5', 'b1a1', 'e5e4', 'g2g3', 'g8e7', 'a1b1', 'e8g8', 'b1a1', 'b7b6', 'a1b1', 'a7a6', 'b1a1', 'c8e6', 'a1b1', 'b6b5', 'b1a1', 'c6b4', 'a1b1', 'f5f3', 'b1a1', 'g7g6', 'a1b1', 'g8g7', 'b1a1', 'h7h5', 'a1b1', 'a8d8', 'b1a1', 'g6g5', 'a1b1', 'c7c6', 'b1a1', 'e7f5', 'a1b1', 'f8e8', 'b1a1', 'c5b6', 'a1b1', 'e6d7', 'b1a1', 'h5h4', 'a1b1', 'a6a5', 'b1a1', 'f7f6', 'a1b1', 'g7f7', 'b1a1', 'f5d4', 'a1b1', 'h4g3', 'b1a1', 'd4b3', 'a1b1', 'f3f2', 'h2f2', 'd7g4']

    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    # print(f"Score : {evaluate_board(plateau)}")
    # color = BLANC if plateau.turn%2 == 1 else NOIR
    # print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    # print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    # print("Case noires menacés")
    # other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    # for case in other_threatened_cases:
    #     piece = getPiece(plateau.grille,case[1])
    #     if piece is not None and piece.color == NOIR:
    #         print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    # plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    
    # exit()
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivanttt")
    last_move = alpha_beta_search(plateau,BLANC)
    print(last_move)
    # print(move_to_chess_notation(m))
    
    
def test_situation6():
    # https://lichess.org/OftrJ4Vr/white#8
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'd7d6', 'f3g1', 'f8e7', 'g1h3', 'c8h3']

    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))

def test_situation7():
    # https://lichess.org/v7ZArZ3C/white#4
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'd8f6']
    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    copied_board = copy.deepcopy(plateau)
    m = alpha_beta_search(copied_board,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    plateau.getAllMovesBasedOnTurn()
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))





def test_situation8():
    # https://lichess.org/mG6hE8Ra/white#38
    plateau = Board2()
    moves = ['e2e4', 'c7c6', 'g1e2', 'd7d5', 'h2h3', 'g8f6', 'h1h2', 'd8d6', 'b1a3', 'e7e6', 'e2g3', 'd6c5', 'f1e2', 'd5e4', 'e1f1', 'b7b5', 'f1e1', 'f8d6', 'e1f1', 'b8d7', 'f1e1', 'h7h5', 'e1f1', 'e8g8', 'f1e1', 'd7e5', 'e1f1', 'a7a5', 'f1e1', 'f8d8', 'e1f1', 'e5g6', 'f1e1', 'd6f4', 'e1f1', 'h5h4', 'f1e1', 'f4g3']
    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    copied_board = copy.deepcopy(plateau)
    m = alpha_beta_search(copied_board,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    plateau.getAllMovesBasedOnTurn()
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    
def test_situation8_alternatif():
    # https://lichess.org/mG6hE8Ra/white#38
    plateau = Board2()
    moves = ['e2e4', 'c7c6', 'g1e2', 'd7d5', 'h2h3', 'g8f6', 'h1h2', 'd8d6', 'b1a3', 'e7e6', 'e2g3', 'd6c5', 'f1e2', 'd5e4', 'e1f1', 'b7b5', 'f1e1', 'f8d6', 'e1f1', 'b8d7', 'f1e1', 'h7h5', 'e1f1', 'e8g8', 'f1e1', 'd7e5', 'e1f1', 'a7a5', 'f1e1', 'f8d8', 'e1f1', 'e5g6', 'f1e1', 'd6f4', 'e1f1', 'h5h4', 'f1e1', 'f4g3']
    
    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    # plateau.print_Board()
    alt_1 = ['f2g3','c5g1']
    # print ("Apres alt")
    # for mm in alt_1:
    #     plateau.getAllMovesBasedOnTurn()
    #     print(plateau.play_move(chess_notation_to_move( mm)))
    #     print([move_to_chess_notation(move) for move in plateau.pMoves])
    #     print(plateau.pMoves)
    plateau.print_Board()
    plateau.getAllMovesBasedOnTurn()
    print(plateau.pMoves)
    # print(f"Score : {evaluate_board(plateau)}")
    
    # piece = getPiece(plateau.grille,(1,2))
    # print(f"Piece {piece}")
    # print(pieceMovement(piece,plateau.grille))
    # pieces = getAllPiecesFromColor(plateau.grille,BLANC)
    # for p in pieces:
    #     print(p.coordinates)
    # allmove = plateau.getAllAvailableMoves(BLANC)
    # print(allmove)
    
def test_situation9():
    # https://lichess.org/88oH9ntF
    plateau = Board2()
    plateau.grille = [
        [Rook(BLANC), None, None,  King(BLANC), Queen(BLANC), Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
        [None,Pawn(BLANC),Pawn(BLANC),None,None,None,Pawn(BLANC),Pawn(BLANC)],
        [None,None,Knight(BLANC),None,None,Pawn(BLANC),None,None],
        [Pawn(BLANC),Bishop(NOIR),None,Pawn(BLANC),None,Bishop(BLANC),None,None],
        [None,None,None,Pawn(NOIR),Pawn(NOIR),Pawn(BLANC),None,None],
        [Knight(NOIR),None,None,None,None,Knight(NOIR),None,None],
        [Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),None,None,Pawn(NOIR),Pawn(NOIR),Pawn(NOIR)],
        [Rook(NOIR),None, None,  King(NOIR), Queen(NOIR), None, None, Rook(NOIR)]
    ]
    plateau.initializeCoordinates()
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    

def test_situation10():
    # https://lichess.org/JEafAHcd
    plateau = Board2()
    moves = ['e2e4', 'e7e6', 'f1c4', 'd7d5', 'c4b5', 'c7c6', 'b5a4', 'b7b5', 'a4b3', 'd5e4', 'd1g4', 'f7f5', 'g4h5', 'e8d7', 'h5f7', 'f8e7', 'b3e6', 'd7c7', 'e6c8', 'd8c8', 'f7g7', 'b8d7', 'g7h8', 'g8f6', 'h8g7', 'c7d6', 'h2h4', 'b5b4', 'g2g4', 'd7e5', 'f2f4', 'e5g4', 'd2d4', 'f6d5', 'c2c4', 'g4e3', 'c4d5', 'e3g4', 'a2a4', 'c6d5', 'c1d2', 'd6d7', 'h1h3', 'c8c4', 'b2b3', 'c4c2', 'd2b4', 'c2c1', 'e1e2', 'c1b2', 'b1d2', 'd7c6', 'b4e7', 'c6b7', 'e7a3', 'b7c8', 'a3b2', 'h7h5', 'g7g8', 'c8c7', 'g8a8', 'e4e3', 'a8a7', 'c7c6', 'a7c5', 'c6b7', 'c5d5', 'b7a7', 'd2c4', 'g4f2', 'h3g3', 'a7b8', 'e2e3', 'f2e4', 'g3g6', 'e4d2', 'e3d2', 'b8c8', 'g6g8', 'c8c7']

    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print("Le move trouvé est")
    print(m)
    plateau.getAllMovesBasedOnTurn()
    print(plateau.pMoves)
    
    print(move_to_chess_notation(m))
    plateau.getAllMovesBasedOnTurn()
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    # exit()
    
    m = ab(plateau,NOIR,1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    
    
    # echecs trop rapide pour nous ['e2e4', 'e7e5', 'g1f3', 'd8f6', 'f3g1', 'f8c5', 'd1g4', 'f6f2', 'e1d1', 'f2f1']
    # https://lichess.org/SUslmNjf#43 tester a 22
    
def test_situation11():
    # # https://lichess.org/SUslmNjf#43 tester a 22
    plateau = Board2()
    plateau.grille = [
        [Rook(BLANC), None, None,  King(BLANC), None, None,Knight(BLANC) , Rook(BLANC)],
        [None,None,None,Knight(BLANC),None,Pawn(BLANC),Pawn(BLANC),Pawn(BLANC)],
        [None,None,None,None,None,None,Bishop(BLANC),None],
        [None,Pawn(BLANC),None,None,Pawn(BLANC),None,None,None],
        [None,Knight(NOIR),None,None,Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),None],
        [Queen(BLANC),None,Queen(NOIR),Pawn(NOIR),None,None,None,None],
        [None,None,Pawn(NOIR),None,Knight(NOIR),None,None,Pawn(NOIR)],
        [None,King(NOIR), Rook(NOIR),None,None, Bishop(NOIR), None, Rook(NOIR)]
    ]
    plateau.initializeCoordinates()
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    # exit()
    m = ab(plateau,NOIR,MAX_DEPTH - 1)
    print(m)
    print(move_to_chess_notation(m))
    #g5f3
    # print(plateau.play_move(chess_notation_to_move("g5f3")) )
    print(plateau.play_move(m) )
    
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case Noires menacés")
    temp = []
    move_of_current_player = plateau.getAllAvailableMoves(BLANC)
    print(move_of_current_player)
    for move in move_of_current_player:
        if move[1] not in temp:
            piece = getPiece(plateau.grille,move[1])
            if piece is not None and piece.color == NOIR:
                print(move[1])
            temp.append(move[1])
    temp = []
    print("Ancienne Version : Case noires menacés")
    temp = []
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        if case[1] not in temp:
            piece = getPiece(plateau.grille,case[1])
            if piece is not None and piece.color == NOIR:
                print(case[1])
            temp.append(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    # print("Move suivant")
    # m = alpha_beta_search(plateau,BLANC)
    # print(m)
    # print(move_to_chess_notation(m))


def test_situation12():
    # https://lichess.org/JEafAHcd
    plateau = Board2()
    moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f3g1', 'g8f6', 'h2h4', 'h7h5', 'g2g4', 'h5g4', 'f1g2', 'd8e7', 'c2c4', 'c6b4', 'e1e2', 'f6h5', 'e2f1', 'e7c5', 'b1a3', 'd7d6', 'd1a4', 'c7c6', 'h1h2', 'b7b5', 'a4a5', 'h5f4', 'g2h1', 'f4d3', 'a1b1', 'h8h4', 'g1h3', 'f8e7', 'a5c7', 'b5c4', 'a3c4', 'c5c4', 'c7c8', 'e7d8', 'c8a8', 'd3e1', 'f1e1', 'g4g3', 'f2g3', 'b4d3', 'e1d1', 'h4h7']

    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat score {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    m = alpha_beta_search(plateau,BLANC)
    print("Le move trouvé est")
    print(m)
    plateau.getAllMovesBasedOnTurn()
    print(move_to_chess_notation(m))
    plateau.getAllMovesBasedOnTurn()
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    # exit()
    
    m = ab(plateau,NOIR,MAX_DEPTH - 1)
    print(m)
    print(move_to_chess_notation(m))
    print(plateau.play_move(m) )
    plateau.print_Board()
    print(f"Score : {evaluate_board(plateau)}")
    
    print("Case blanches menacés")
    my_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, BLANC)
    for case in my_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == BLANC:
            print(case[1])
    
    print("Case noires menacés")
    other_threatened_cases =  getThreatenedCasesWithKing(plateau.grille, NOIR)
    for case in other_threatened_cases:
        piece = getPiece(plateau.grille,case[1])
        if piece is not None and piece.color == NOIR:
            print(case[1])
    
    color = BLANC if plateau.turn%2 == 1 else NOIR
    print(f"couleur {color}  adv {getAdvesaryColor(color)}")
    # print(f"threat {threat_score_by_color(plateau.grille,getAdvesaryColor(color))}" )
    print(f"score without threat {board_score_without_threat(plateau.grille)}" )
    
    print("Move suivant")
    # m = alpha_beta_search(plateau,BLANC)
    # print(m)
    # print(move_to_chess_notation(m))