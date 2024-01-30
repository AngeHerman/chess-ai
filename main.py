from chess.board import *
from chess.utils import *
from api.events import *
import threading
import time
import os


if __name__ == "__main__":
    is_my_turn = threading.Event()
    moves = ["a7a6", "b7b6", "c7c6", "d7d6", "e7e6", "f7f6", "g7g6", "h7h6"]
    plateau = Board()
    plateau.print_Board()
    print(get_coord("f4"))
    stream_events_thread = threading.Thread(target=stream_events)
    stream_events_thread.start()
    time.sleep(2)
    if not challenge_ai():
        os.exit(1)
    stream_board_thread = threading.Thread(target=stream_board_state, args=(is_my_turn,))
    stream_board_thread.start()
    time.sleep(2)
    for m in moves:
        print(is_my_turn.is_set())
        is_my_turn.wait()
        if not make_move(m,is_my_turn):
            print("...")
    stream_events_thread.join()
    stream_board_thread.join()