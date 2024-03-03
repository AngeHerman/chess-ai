from chess.board import *
from chess.utils import *
from api.lichess import *
from tests.test_board import *
from ai.monte_carlo import *
import threading
import time
import os

def play_against_ai():
    # all_moves = [""]
    is_my_turn = threading.Event()
    moves = ["a7a6", "b7b6", "c7c6", "d7d6", "e7e6", "f7f6", "g7g6", "h7h6"]
    plateau = Board()
    plateau.print_Board()
    # print(get_coord("f4"))
    api = Lichess()
    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    time.sleep(2)
    if not api.challenge_ai():
        os.exit(1)
    stream_board_thread = threading.Thread(target=api.stream_board_state, args=(is_my_turn,))
    stream_board_thread.start()
    time.sleep(2)
    for m in moves:
        print(is_my_turn.is_set())
        is_my_turn.wait()
        if not api.make_move(m,is_my_turn):
            print("...")
        time.sleep(1)
        # print("*************************************m est "+all_moves[0])
        print("*************************************leTruc est "+api.moves)
        
        # print("************************************* mm est ".join(map(str, mm)))
        # best_move = mcts(mon_board_initial, iterations=1000)
        # print("Meilleur coup calculé par MCTS :", best_move)
    stream_events_thread.join()
    stream_board_thread.join()
    
def play_against_player():
    api = Lichess()
    stream_events_thread = threading.Thread(target=api.stream_events)
    stream_events_thread.start()
    while(not api.game_against_player_started):
        time.sleep(0.5)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Ca a commencé")
    stream_events_thread.join()
    
def test():
    plateau = Board()
    plateau.print_Board()
    # print(plateau.getAllMovesBasedOnTurn())
    a = mcts(plateau,30)
    print(a)
    print(a[0])
    print(a[1])
    print(a[0][0])
    print(a[0][1])
    print(a[1][0])
    print(a[1][1])
    b = move_to_chess_notation(a)
    print(b)
    print("**********TEST PLAY MOVE***************")
    plateau.play_move(a)
    plateau.print_Board()
    print("**********TEST NOTATION***************")
    print(chess_notation_to_move(b))
    print(chess_notation_to_move( move_to_chess_notation( ((7,7),(2,5)) ) ) )
    
    # print(move_to_chess_notation(2,5))
    # print(move_to_chess_notation(4,4))
    # plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    # print("*************************")
    # plateau.turn += 1
    # plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    #test_knightMovement((4,4))
    #test_bishopMovement((4,4))
    #test_rookMovement((4,4))
    #test_kingMovement(())
    #test_kingMovement((4,4))
    
if __name__ == "__main__":
    # play_against_ai()
    #play_against_player()
    test()
    
    
