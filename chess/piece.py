from chess.constants import *
from chess.utils import *

class Piece:
    def __init__(self,color,name = ""):
        self.color = color
        self.name = name
        self.coordinates = None
        self.moveCount = 0
        
        
    def get_movement(self,board):
        pass

    def setCoordinates(self,coord):
        self.coordinates = coord