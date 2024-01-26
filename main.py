from chess.board import *
from chess.utils import *
from api.events import *


if __name__ == "__main__":
    plateau = Board()
    plateau.print_Board()
    print(get_coord("f4"))
    stream_events()