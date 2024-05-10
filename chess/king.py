from chess.constants import *
from chess.utils import *
from chess.piece import *


class King(Piece):
    def __init__(self,color):
        super().__init__(color,ROI)
        self.isThreatened = False
        self.moves = []

    def print(self):
        if (self.color == BLANC):
            print(ROI_BLANC,end="")
        else:
            print(ROI_NOIR,end="")
        


    def king_movement(self,tab):
        
        differentPaths = diagonalPathsFromPiece(self,tab,2) + straightPathsFromPiece(self,tab,2,2)
        possible_positions  = []

        for i in range(len(differentPaths)):

            for j in range(1,len(differentPaths[i])):
                if not(checkCaseEmpty(tab,differentPaths[i][j])) and not(checkCanEat(tab,self.coordinates,differentPaths[i][j])):
                    break
                position = (differentPaths[i][j][0],differentPaths[i][j][1])
                possible_positions.append((self.coordinates,position,""))
                

        piecesToRemove = [self]

        """ We need to know whether or not the adjacents pieces to our king are protected, in order
        to do that we remove them from the board and check if their position are in the threatened position list """

        for i in range(len(possible_positions)):
            if not(checkCaseEmpty(tab,possible_positions[i][1])):
                piecesToRemove.append(getPiece(tab,possible_positions[i][1]))
        
        emptyCase(tab,piecesToRemove[0].coordinates)
        opponent_movements = set()
        opponent_movements.update(getThreatenedCases(tab,self.color))

        for j in range(1,len(piecesToRemove)):
            emptyCase(tab,piecesToRemove[j].coordinates)
            threatenedCases = getThreatenedCases(tab,self.color)
            pieceProtectedCoordinates = [threatenedCases[ind] for ind in range(0,len(threatenedCases)) if threatenedCases[ind][1] == piecesToRemove[j].coordinates]
            opponent_movements.update(pieceProtectedCoordinates)
            addPieceToCase(tab,piecesToRemove[j].coordinates,piecesToRemove[j])

        addPieceToCase(tab,piecesToRemove[0].coordinates,piecesToRemove[0])
        opponent_movements.update(getThreatenedCases(tab,self.color))
        opponent_movements_pos = [i[1] for i in (opponent_movements)]
        positions = [possible_positions[i] for i in range(0,len(possible_positions)) if not(possible_positions[i][1] in opponent_movements_pos)]
        return positions



        