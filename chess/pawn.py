from chess.constants import *
from chess.utils import *
from chess.piece import *

class Pawn(Piece):

    def __init__(self, color):
        super().__init__(color, PION)
        self.direction = -1 if color == NOIR else 1
        en_passant = 0
        
    def __str__(self) -> str:
        representation = PION_BLANC if self.color == BLANC else PION_NOIR
        return str(representation)
    def print(self):
        if (self.color == BLANC):
            print(PION_BLANC,end="")
        else:
            print(PION_NOIR,end="")


    def pawn_movement(self,grille):
        movement_list = []
        promotion_position = 0
        special_position = HEIGHT - 2
        en_passant_pos = 4

        if self.color == BLANC :
            special_position = 1
            promotion_position = HEIGHT - 1
            en_passant_pos = 5

        newCoordinates = self.coordinates[0] + self.direction


        if(areCoordinatesBounded(newCoordinates,self.coordinates[1] ) and checkCaseEmpty(grille,(newCoordinates,self.coordinates[1]))):
                
            if(newCoordinates == promotion_position):
                available_promotions = ["q","n","b","r"]
                for i in range(0,len(available_promotions)):
                    movement_list.append((self.coordinates,(newCoordinates,self.coordinates[1]),available_promotions[i]))
            else:
                movement_list.append((self.coordinates,(newCoordinates,self.coordinates[1]),""))

            if(self.coordinates[0] == special_position) and  checkCaseEmpty(grille,(self.coordinates[0] + self.direction * 2,self.coordinates[1])):
                movement_list.append((self.coordinates,(self.coordinates[0]+ self.direction * 2,self.coordinates[1]),""))
                
        if(self.en_passant == 1 and self.coordinates[0] == en_passant_pos):
            movement_list += self.pawn_enPassantMovements(grille)

        movement_list += self.pawn_eatPieceMovements(grille)   
        return movement_list
                

    def pawn_ThreatenedCases(self):
        pMovements = [(self.coordinates[0]+self.direction,self.coordinates[1]+self.direction),(self.coordinates[0]+self.direction,self.coordinates[1]-self.direction)]
        return [pMovements[i] for i in range(0,len(pMovements)) if areCoordinatesBounded(pMovements[i][0],pMovements[i][1]) ]
    
    def pawn_ThreatenedCasesBis(self):
        pMovements = [(self.coordinates[0]+self.direction,self.coordinates[1]+self.direction),(self.coordinates[0]+self.direction,self.coordinates[1]-self.direction)]
        return [(self.coordinates,pMovements[i],"") for i in range(0,len(pMovements)) if areCoordinatesBounded(pMovements[i][0],pMovements[i][1]) ]
    
    def pawn_eatPieceMovements(self,tab):
        threatenedCases = self.pawn_ThreatenedCases()
        return [(self.coordinates,threatenedCases[i],"") for i in range(0,len(threatenedCases)) if checkCaseHasEdible(tab,self.coordinates,threatenedCases[i])]
    
    def pawn_enPassantMovements(self,tab):
        ediblePos = [(self.coordinates[0],(self.coordinates[1] - 1)),(self.coordinates[0],(self.coordinates[1] + 1))]
        movingPos = [((self.coordinates[0] + self.direction),(self.coordinates[1] - 1)),((self.coordinates[0] + self.direction),(self.coordinates[1] + 1))]

        return [movingPos[i] for i in range(0,len(ediblePos)) if checkCaseHasEdible(tab,self.coordinates,ediblePos[i]) and areCoordinatesBounded(movingPos[i][0],movingPos[i][1])]