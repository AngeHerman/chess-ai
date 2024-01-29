from chess.board import *
from chess.utils import *
from api.events import *
import threading
import time
import os


if __name__ == "__main__":
    plateau = Board()
    plateau.print_Board()
    print(get_coord("f4"))
    stream_thread = threading.Thread(target=stream_events)
    stream_thread.start()
    # time.sleep(6)
    # if not challenge_ai():
    #     os.exit(1)
    # time.sleep(4)
    # if not make_move("e7e5"):
    #     print("...")
    stream_thread.join()