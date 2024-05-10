from chess.constants import *
from chess.utils import *
from chess.piece import *

class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color, FOU)

    def print(self):
        if (self.color == BLANC):
            print(FOU_BLANC,end="")
        else:
            print(FOU_NOIR,end="")

    def __str__(self) -> str:

        representation = FOU_BLANC if self.color == BLANC else FOU_NOIR
        return representation


    def bishop_movement(self,tab,MAX):
        
        diagonalPaths = diagonalPathsFromPiece(self,tab,MAX)
        pMovements = []

        for i in range(len(diagonalPaths)):
            for j in range(1,len(diagonalPaths[i])):
                if not(checkCaseEmpty(tab,diagonalPaths[i][j])) and not(checkCanEat(tab,self.coordinates,diagonalPaths[i][j])):
                    break
                position = (diagonalPaths[i][j][0],diagonalPaths[i][j][1])
                pMovements.append((self.coordinates,position,""))
        
        return pMovements