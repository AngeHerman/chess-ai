from chess.utils import *
import unittest

class TestChessFunctions(unittest.TestCase):
    def test_cell_to_chess_notation(self):
        self.assertEqual(cell_to_chess_notation(0, 0), "a8")
        self.assertEqual(cell_to_chess_notation(7, 7), "h1")

    def test_chessl_notation_to_cel(self):
        self.assertEqual(chess_notation_to_cell("a8"), (0, 0))
        self.assertEqual(chess_notation_to_cell("h1"), (7, 7))

    def test_move_to_chess_notation(self):
        self.assertEqual(move_to_chess_notation(((6, 4), (4, 4))), "e7e5")
        self.assertEqual(move_to_chess_notation(((1, 4), (3, 4))), "e2e4")

    def test_chess_notation_to_move(self):
        self.assertEqual(chess_notation_to_move("e7e5"), ((6, 4), (4, 4)))
        self.assertEqual(chess_notation_to_move("e2e4"), ((1, 4), (3, 4)))

if __name__ == '__main__':
    unittest.main()