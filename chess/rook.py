from chess.constants import *
from chess.utils import *
from chess.piece import *


class Rook(Piece):
    def __init__(self,color):
        pass

    def print(self):
        if (self.color == BLANC):
            print(TOUR_BLANC)
        else:
            print(TOUR_NOIR)

    def rook_movement(self,tab,width,height):

        straightPaths = straightPathsFromPiece(self,tab,height,width)
        pMovements = []

        
        for i in range(len(straightPaths)):
            for j in range(1,len(straightPaths[i])):
                if not(checkCaseEmpty(tab,straightPaths[i][j])) and not(checkCanEat(tab,self.coordinates,straightPaths[i][j])):
                    break
                pMovements.append((self.coordinates,straightPaths[i][j]))

        return pMovements