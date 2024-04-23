from chess.constants import *
from chess.utils import *
from chess.piece import *

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, DAME)

    def print(self):
        if (self.color == BLANC):
            print(DAME_BLANCHE,end="")
        else:
            print(DAME_NOIRE,end="")

    def queen_movement(self,tab):
        
        differentPaths = diagonalPathsFromPiece(self,tab,WIDTH) + straightPathsFromPiece(self,tab,HEIGHT,WIDTH)
        pMovements = []

        for i in range(len(differentPaths)):
            for j in range(1,len(differentPaths[i])):
                if not(checkCaseEmpty(tab,differentPaths[i][j])) and not(checkCanEat(tab,self.coordinates,differentPaths[i][j])):
                    break
                position = (differentPaths[i][j][0],differentPaths[i][j][1],"")
                pMovements.append((self.coordinates,position))

        return pMovements