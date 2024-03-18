from chess.constants import *
from chess.utils import *
from chess.piece import *

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, CAVALIER)

    def print(self):
        if (self.color == BLANC):
            print(CAVALIER_BLANC,end="")
        else:
            print(CAVALIER_NOIR,end="")

    def knight_movement(self,tab):

        movement_list = []
        movements = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

        for i in range(len(movements)):

            new_y = self.coordinates[0] + movements[i][0]
            new_x = self.coordinates[1] + movements[i][1]

            if(areCoordinatesBounded(new_y,new_x)):
                if(checkCaseEmpty(tab,(new_y,new_x)) or checkCanEat(tab,self.coordinates,(new_y,new_x))):
                    movement_list.append((self.coordinates,(new_y,new_x)))

        return movement_list