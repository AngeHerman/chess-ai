from chess.constants import *
from chess.utils import *
from chess.piece import *

class Bishop(Piece):

    def print(self):
        if (self.color == BLANC):
            print(FOU_BLANC)
        else:
            print(FOU_NOIR)


    def bishop_movement(self,tab,MAX):
        
        diagonalPaths = diagonalPathsFromPiece(self,tab,MAX)
        pMovements = []

        for i in range(len(diagonalPaths)):
            for j in range(1,len(diagonalPaths[i])):
                if not(checkCaseEmpty(tab,diagonalPaths[i][j])) and not(checkCanEat(tab,self.coordinates,diagonalPaths[i][j])):
                    break
                pMovements.append((self.coordinates,diagonalPaths[i][j]))
        
        return pMovements