from chess.constants import *
from chess.utils import *

class Board:
    def __init__(self):
        self.grille = [
            [TOUR_BLANC, CAVALIER_BLANC, FOU_BLANC, DAME_BLANCHE, ROI_BLANC, FOU_BLANC, CAVALIER_BLANC, TOUR_BLANC],
            [PION_BLANC] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [PION_NOIR] * 8,
            [TOUR_NOIR, CAVALIER_NOIR, FOU_NOIR, DAME_NOIRE, ROI_NOIR, FOU_NOIR, CAVALIER_NOIR, TOUR_NOIR]
        ]
        self.turn = 0

    def print_Board(self):
        for ligne in self.grille:
            print(ligne)

    def play_move(self, coup):
        # Creeeer coup apres
        pass

    def moves(self, coord_depart):
        pieces = self.getAllPlayerPieces()



        return 

        # Trouver un moyen de generrer les coups 
       # pass
    def getAllAvailableMoves(self,color):
        
        pMoves = []
        pieces = getAllPiecesCoordinatesFromColor(self.grille,color)
        kingSurroundings = []
        
        for i in range(len(pieces)):
            piece = getPiece(self.grille,pieces[i])

            if piece == PION_NOIR or piece == PION_BLANC :
                pMoves.append(self.pawn_movement(pieces[i]))
            elif piece == CAVALIER_NOIR or piece == CAVALIER_BLANC:
                pMoves.append(self.knight_movement(pieces[i]))
            elif piece == FOU_NOIR or piece == FOU_BLANC :
                pMoves.append(self.bishop_movement(pieces[i],WIDTH))
            elif piece == TOUR_NOIR or piece == TOUR_BLANC:
                pMoves.append(self.rook_movement(pieces[i],WIDTH,HEIGHT))
            elif piece == DAME_NOIRE or piece == DAME_BLANCHE:
                pMoves.append(self.queen_movement(pieces[i]))
            elif piece == ROI_NOIR or piece == ROI_BLANC:
                pMoves.append(self.king_movement(pieces[i]))
                kingSurroundings = self.getKingSurrondings(pieces[i])
        #Si le roi est directement menacé par un pièce on retourne uniquement les mouvement permettant de le protéger
        if len(kingSurroundings) > 0 : 
            return [pMoves[i] for i in range(len(pMoves)) if pMoves[i][1] in kingSurroundings]
            
        return pMoves



    def getKingSurrondings(self,coord):

        dangerousCoordinates = []

        straight = self.straightPathsFromPiece(coord,HEIGHT,WIDTH)
        diagonals = self.diagonalPathsFromPiece(coord,WIDTH)

        straightLineEnemies = {TOUR_BLANC,DAME_BLANCHE} if self.grille[coord[0]][coord[1]] < 0 else {TOUR_NOIR,DAME_NOIRE}
        diagonalLineEnemies = {FOU_BLANC,DAME_BLANCHE} if self.grille[coord[0]][coord[1]] < 0 else {FOU_NOIR,DAME_NOIRE}
        knightEnemy = CAVALIER_BLANC if self.grille[coord[0]][coord[1]] < 0 else CAVALIER_NOIR

        """ On sait que le roi ne peut être mis en danger que d'une direction
        On tente toute les directions pour savoir laquelle crée un chemin jusqu'à une menace"""
        for i in range(len(straight)):
            if straight[i][len(straight[i]) - 1] in straightLineEnemies:
                dangerousCoordinates += straight[i]
        
        for i in range(len(diagonals)):
            if diagonals[i][len(diagonals[i]) - 1] in diagonalLineEnemies:
                dangerousCoordinates += diagonals[i]

        knights = self.knight_movement(coord)
        threateningKnights = [knights[i][1] for i in range(knights) if self.grille[knights[i][1][0]][knights[i][1][1]] == knightEnemy]
        dangerousCoordinates += threateningKnights

        return dangerousCoordinates


    def straightPathsFromPiece(self,coord,height,width):

        possible_movements = [[coord] * 4]
        y, x = coord[0], coord[1]
        add1,add2 = True,True

        for i in range(1,height):

            if(areCoordinatesBounded(y+i,x) and add1):
                if checkCaseEmpty(self.grille,(y+i,x)):
                    possible_movements[0].append((y+i,x))
                else : 
                    add1 = False
                    if checkCanEat(self.grille,coord,(y+i,x)) :
                        possible_movements[0].append((y+i,x))

            if(areCoordinatesBounded(y-i,x) and add2):
                if checkCaseEmpty(self.grille,(y-i,x)):
                    possible_movements[1].append((y-i,x))
                else : 
                    add2 = False
                    if checkCanEat(self.grille,coord,(y-i,x)) :
                        possible_movements[1].append((y-i,x))
        
        add1,add2 = True,True

        for j in range(1,width):

            if(areCoordinatesBounded(y,x+i) and add1):
                if checkCaseEmpty(self.grille,(y,x+i)):
                    possible_movements[2].append((y,x+i))
                else : 
                    add1 = False
                    if checkCanEat(self.grille,coord,(y,x+i)) :
                        possible_movements[2].append((y,x+i))

            if(areCoordinatesBounded(y,x-i) and add2):
                if checkCaseEmpty(self.grille,(y,x-i)):
                    possible_movements[3].append((y,x-i))
                else : 
                    add2 = False
                    if checkCanEat(self.grille,coord,(y,x-i)) :
                        possible_movements[3].append((y,x-i))

        return possible_movements



    def diagonalPathsFromPiece(self,coord,MAX):

        paths = [[coord] * 4]
        y, x= coord[0], coord[1] 
        
        add_dir1 = True
        add_dir2 = True
        add_dir3 = True
        add_dir4 = True

        for i in range(MAX):
            if(areCoordinatesBounded(y+i,x+i) and add_dir1):
                if checkCaseEmpty(self.grille,(y+i,x+i)) : 
                    paths[0].append((y+i,x+i))
                else:
                    add_dir1 = False
                    # On vérifie que si il y a un danger sur la diagonal
                    if checkCanEat(self.grille,coord,(y+i,x+i)):
                        paths[0].append((y+i,x+i))

            if(areCoordinatesBounded(y-i,x-i) and add_dir2):
                if checkCaseEmpty(self.grille,(y-i,x-i)) : 
                    paths[1].append((y-i,x-i))
                else:
                    add_dir2 = False
                    if checkCanEat(self.grille,coord,(y-i,x-i)):
                        paths[1].append((y-i,x-i))
            
            if(areCoordinatesBounded(y+i,x-i) and add_dir3):
                if checkCaseEmpty(self.grille,(y+i,x-i)) : 
                    paths[2].append((y+i,x-i))
                else:
                    add_dir3 = False
                    if checkCanEat(self.grille,coord,(y+i,x-i)):
                        paths[2].append((y+i,x-i))
            
            if(areCoordinatesBounded(y-i,x+i) and add_dir4):

                if checkCaseEmpty(self.grille,(y-i,x+i)) : 
                    paths[3].append((y-i,x+i))
                else:
                    add_dir4 = False
                    if checkCanEat(self.grille,coord,(y-i,x+i)):
                        paths[3].append((y-i,x+i))
            
        return paths


        
    def pawn_movement(self,coord):

        movement_list = []
        pawn = getPiece(self.grille,coord)
        move_value = 1
        special_position = 1

        if(pawn < 0):
            move_value = -1
            special_position = HEIGHT - 2

        if(areCoordinatesBounded(coord[0] + move_value,coord[1] )):
            movement_list.append(coord,(coord[0] + move_value,coord[1]))

            if(coord[0] == special_position) :
                movement_list.append(coord,(coord[0]+ move_value * 2,coord[1]))
        
        movement_list += self.pawn_eatPieceMovements(self.grille,coord,-move_value)        
        return movement_list
                

    def pawn_ThreatenedCases(self,coord,color):
        
        move_value = 1 if color < 0 else -1
        movement_list = []

        pMovements = [(coord[0]+move_value,coord[1]+move_value),(coord[0]+move_value,coord[1]-move_value)]

        for i in range(0,len(pMovements)):
            if(areCoordinatesBounded(pMovements[i][0],pMovements[i][1])):
                movement_list.append(coord,pMovements[i])
        
        return movement_list

    def pawn_eatPieceMovements(self,coord,color):

        threatenedCases = self.pawn_ThreatenedCases(self,coord,color)
        movement_list = []

        for i in range(0,len(threatenedCases)):
            if(checkCaseHasEdible(self.grille,coord,threatenedCases[i])):
                movement_list.append(coord,threatenedCases[i])

        return movement_list
    


    def knight_movement(self,coord):

        movement_list = []
        movements = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

        for i in range(len(movements)):

            new_y = coord[0] + movements[i][0]
            new_x = coord[1] + movements[i][1]

            if(areCoordinatesBounded(new_y,new_x)):
                if(checkCaseEmpty(self.grille,(new_y,new_x)) or checkCanEat(self.grille,coord,(new_y,new_x))):
                    movements.append(coord,(new_y,new_x))

        return movement_list

    def bishop_movement(self,coord,MAX):
        
        diagonalPaths = self.diagonalPathsFromPiece(coord,MAX)
        return [(coord,path[i]) for path in diagonalPaths for i in range(1,len(path))]
    
        """movement_list = []


        y = coord[0] 
        x = coord[1] 

        add_dir1 = True
        add_dir2 = True
        add_dir3 = True
        add_dir4 = True

        for i in range(1,MAX):
        
            if(areCoordinatesBounded(y+i,x+i) and add_dir1):

                if(checkCanEat(self.grille,coord,(y+i,x+i)) or checkCaseEmpty(self.grille,(y+i,x+i))) : 
                    movement_list.append(coord,(y+i,x+i))
                else:
                    add_dir1 = False

            if(areCoordinatesBounded(y-i,x-i) and add_dir2):
                
                if(checkCanEat(self.grille,coord,(y-i,x-i)) or checkCaseEmpty(self.grille,(y-i,x-i))) : 
                    movement_list.append(coord,(y-i,x-i))
                else:
                    add_dir2 = False
            
            if(areCoordinatesBounded(y+i,x-i) and add_dir3):

                if(checkCanEat(self.grille,coord,(y+i,x-i)) or checkCaseEmpty(self.grille,(y+i,x-i))) : 
                    movement_list.append(coord,(y+i,x-i))
                else:
                    add_dir3 = False

            if(areCoordinatesBounded(y-i,x+i) and add_dir4):
                
                if(checkCanEat(self.grille,coord,(y-i,x+i)) or checkCaseEmpty(self.grille,(y-i,x+i))) :
                    movement_list.append(coord,(y-i,x+i))
                else:
                    add_dir4 = False

        return movement_list"""


    def rook_movement(self,coord,width,height):

        straightPaths = self.straightPathsFromPiece(coord,height,width)
        return [(coord,path[i]) for path in straightPaths for i in range(1,len(path))]
        """y = coord[0]
        x = coord[1]

        add1 = True
        add2 = True

        for i in range(1,height):

            if(areCoordinatesBounded(y+i,x) and add1):
                if(checkCanEat(self.grille,coord,(y+i,x)) or checkCaseEmpty(self.grille,(y+i,x))):
                    possible_movements.append(coord,(y+i,x))
                else : add1 = False

            if(areCoordinatesBounded(y-i,x) and add2):
                if(checkCanEat(self.grille,coord,(y-i,x)) or checkCaseEmpty(self.grille,(y-i,x))):
                    possible_movements.append(coord,(y-i,x))
                else : add2 = False
        
        add1 = True
        add2 = True

        for j in range(1,width):

            if(areCoordinatesBounded(y,x+j) and add1):
                if(checkCanEat(self.grille,coord,(y,x+j)) or checkCaseEmpty(self.grille,(y,x+j))):
                    possible_movements.append(coord,(y,x+j))
                else : add1 = False

            if(areCoordinatesBounded(y,x-j) and add2):
                if(checkCanEat(self.grille,coord,(y,x-j)) or checkCaseEmpty(self.grille,(y,x-j))):
                    possible_movements.append(coord,(y,x-j))
                else : add2 = False

        return possible_movements"""


    def queen_movement(self,coord):
        return self.rook_movement(coord,WIDTH,HEIGHT) + self.bishop_movement(coord,WIDTH)

    def king_movement(self,coord):

        possible_positions = self.rook_movement(coord,2,2) + self.bishop_movement(coord,2)
        opponent_movements = []

        king = getPiece(self.grille,coord)

        FOU_ADVERSE = FOU_NOIR if king == ROI_BLANC else FOU_BLANC
        TOUR_ADVERSE = TOUR_NOIR if king == ROI_BLANC else TOUR_BLANC
        CAVALIER_ADVERSE = CAVALIER_NOIR if king == ROI_BLANC else CAVALIER_BLANC
        DAME_ADVERSE = DAME_NOIRE if king == ROI_BLANC else DAME_BLANCHE
        PION_ADVERSE = PION_NOIR if king == ROI_BLANC else PION_BLANC

        opponent_pieces = getPiecesCoordinates(self.grille,FOU_ADVERSE) + getPiecesCoordinates(self.grille,TOUR_ADVERSE) + getPiecesCoordinates(self.grille,DAME_ADVERSE) + getPiecesCoordinates(self.grille,CAVALIER_ADVERSE)
        opponent_pieces += getPiecesCoordinates(self.grille,PION_ADVERSE)

        for i in range(0,len(opponent_pieces)):

            piece = getPiece(self.grille,opponent_pieces[i])

            if(piece == FOU_ADVERSE):
                opponent_movements += self.bishop_movement(opponent_pieces[i],WIDTH)
            elif(piece == TOUR_ADVERSE):
                opponent_movements += self.rook_movement(opponent_pieces[i],WIDTH,HEIGHT)
            elif(piece == CAVALIER_ADVERSE):
                opponent_movements += self.knight_movement(opponent_pieces[i])
            elif(piece == DAME_ADVERSE):
                opponent_movements += self.queen_movement(opponent_pieces[i])
            elif(piece == PION_ADVERSE):
                opponent_movements += self.pawn_ThreatenedCases(opponent_pieces[i],-PION_ADVERSE)
        

        opponent_movements_pos = [opponent_movements[i][1] for i in range(0,len(opponent_movements))]
        positions = [possible_positions[i] for i in range(0,len(possible_positions)) if not(possible_positions[i][1] in opponent_movements_pos)]

        return positions



