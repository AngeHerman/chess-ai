from chess.constants import *
from chess.utils import *
from chess.piece import *

class Queen(Piece):
    def __init__(self,color):
        pass

    def print(self):
        if (self.color == BLANC):
            print(DAME_BLANCHE)
        else:
            print(DAME_NOIRE)

    def queen_movement(self,tab):
        
        differentPaths = diagonalPathsFromPiece(self,tab,WIDTH) + straightPathsFromPiece(self,tab,HEIGHT,WIDTH)
        pMovements = []

        for i in range(len(differentPaths)):
            for j in range(1,len(differentPaths[i])):
                if not(checkCaseEmpty(tab,differentPaths[i][j])) and not(checkCanEat(tab,self.coordinates,differentPaths[i][j])):
                    break
                pMovements.append((self.coordinates,differentPaths[i][j]))

        return pMovements