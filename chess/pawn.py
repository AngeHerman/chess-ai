from chess.constants import *
from chess.utils import *
from chess.piece import *

class Pawn(Piece):
    def __init__(self,color,direction):
        self.color = color
        self.direction = direction

    def print(self):
        if (self.color == BLANC):
            print(PION_BLANC)
        else:
            print(PION_NOIR)


    def pawn_movement(self,grille):
        movement_list = []
        special_position = HEIGHT - 2

        if self.color == BLANC :
            special_position = 1

        if(areCoordinatesBounded(self.coordinates[0] + self.direction,self.coordinates[1] ) and checkCaseEmpty(grille,(self.coordinates[0] + self.direction,self.coordinates[1]))):
            movement_list.append((self.coordinates,(self.coordinates[0] + self.direction,self.coordinates[1])))

            if(self.coordinates[0] == special_position) and  checkCaseEmpty(grille,(self.coordinates[0] + self.direction * 2,self.coordinates[1])):
                movement_list.append((self.coordinates,(self.coordinates[0]+ self.direction * 2,self.coordinates[1])))
        
        movement_list += self.pawn_eatPieceMovements()        
        return movement_list
                

    def pawn_ThreatenedCases(self):
        pMovements = [(self.coordinates[0]+self.direction,self.coordinates[1]+self.direction),(self.coordinates[0]+self.direction,self.coordinates[1]-self.direction)]
        return [pMovements[i] for i in range(0,len(pMovements)) if areCoordinatesBounded(pMovements[i][0],pMovements[i][1]) ]

    def pawn_eatPieceMovements(self,tab):
        threatenedCases = self.pawn_ThreatenedCases()
        return [(self.coordinates,threatenedCases[i]) for i in range(0,len(threatenedCases)) if checkCaseHasEdible(tab,self.coordinates,threatenedCases[i])]