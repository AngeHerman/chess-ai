from chess.constants import *
from chess.utils import *
from chess.piece import *


class King(Piece):
    def __init__(self,color):
        self.isThreatened = False
        self.moves = []
        pass

    def print(self):
        if (self.color == BLANC):
            print(ROI_BLANC)
        else:
            print(ROI_NOIR)
        


    def king_movement(self,tab):
        
        differentPaths = diagonalPathsFromPiece(self,tab,2) + straightPathsFromPiece(self,tab,2,2)
        possible_positions  = []

        for i in range(len(differentPaths)):
            for j in range(1,len(differentPaths[i])):
                if not(checkCaseEmpty(tab,differentPaths[i][j])) and not(checkCanEat(tab,self.coordinates,differentPaths[i][j])):
                    break
                possible_positions.append((self.coordinates,differentPaths[i][j]))
            
        piecesToRemove = [self]

        """ We need to know whether or not the adjacents pieces to our king are protected, in order
        to do that we remove them from the board and check if their position are in the threatened position list """

        for i in range(len(possible_positions)):
            if not(checkCaseEmpty(tab,possible_positions[i][1])):
                piecesToRemove.append(getPiece(tab,possible_positions[i][1]))
        
        emptyCase(tab,piecesToRemove[0])
        opponent_movements = getThreatenedCases(self.color)

        for j in range(1,len(piecesToRemove)):
            emptyCase(tab,piecesToRemove[j])


        opponent_movements += getThreatenedCases(self.color)

        for z in range(len(piecesToRemove)):
            addPieceToCase(tab,piecesToRemove[z][0],piecesToRemove[z][1])

        opponent_movements += self.getThreatenedCases(self.color)
        
        opponent_movements_pos = [opponent_movements[i][1] for i in range(0,len(opponent_movements))]
        positions = [possible_positions[i] for i in range(0,len(possible_positions)) if not(possible_positions[i][1] in opponent_movements_pos)]

        return positions



