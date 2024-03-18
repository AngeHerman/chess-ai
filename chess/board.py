from chess.constants import *
from chess.utils import *

class Board:
    def __init__(self):
        self.grille = [
            [TOUR_BLANC, CAVALIER_BLANC, FOU_BLANC, ROI_BLANC, DAME_BLANCHE, FOU_BLANC, CAVALIER_BLANC, TOUR_BLANC],
            [PION_BLANC] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [PION_NOIR] * 8,
            [TOUR_NOIR, CAVALIER_NOIR, FOU_NOIR, ROI_NOIR, DAME_NOIRE, FOU_NOIR, CAVALIER_NOIR, TOUR_NOIR]
        ]
        self.turn = 1
        self.pMoves = []
        self.isGameEnded = False

    def print_Board(self):
        for ligne in self.grille:
            print(ligne)

    def play_move(self, coup):

        if coup in self.pMoves:
            piece = getPiece(self.grille,coup[0])
            emptyCase(self.grille,coup[0])
            addPieceToCase(self.grille,coup[1],piece)
            self.turn += 1
            return True
        
        return False
    
<<<<<<< HEAD
    def force_play_move(self, coup):
        piece = getPiece(self.grille,coup[0])
        emptyCase(self.grille,coup[0])
        addPieceToCase(self.grille,coup[1],piece)
        self.turn += 1
        return True
=======
    def endGame(self):

        moveBlanc = self.getAllAvailableMoves(BLANC)
        moveNoir = self.getAllAvailableMoves(NOIR)

        gagnant = 0
        ''' à vérifier les conditions pour exéquo '''
        if len(moveBlanc) == 0 :
            gagnant = NOIR
            self.isGameEnded = True
        elif len(moveNoir) == 0:
            gagnant = BLANC
            self.isGameEnded = True
        
        return gagnant

    
    


>>>>>>> eric

    

    def moves(self, coord_depart):
        pass
        # Trouver un moyen de generrer les coups 
       # pass  
    def getAllMovesBasedOnTurn(self):

        color = BLANC if self.turn%2 == 1 else NOIR
        self.pMoves = self.getAllAvailableMoves(color)            

            

    def getAllAvailableMoves(self,color):
        
        pMoves = []
        pieces = getAllPiecesCoordinatesFromColor(self.grille,color)
        kingSurroundings = []
        kingPosition = (0,0)
        
        for i in range(len(pieces)):
            
            piece = getPiece(self.grille,pieces[i])

            if piece == PION_NOIR or piece == PION_BLANC :
                pMoves += self.pawn_movement(pieces[i])
            elif piece == CAVALIER_NOIR or piece == CAVALIER_BLANC:
                pMoves += self.knight_movement(pieces[i])
            elif piece == FOU_NOIR or piece == FOU_BLANC :
                pMoves += self.bishop_movement(pieces[i],WIDTH)
            elif piece == TOUR_NOIR or piece == TOUR_BLANC:
                pMoves += self.rook_movement(pieces[i],WIDTH,HEIGHT)
            elif piece == DAME_NOIRE or piece == DAME_BLANCHE:
                pMoves += self.queen_movement(pieces[i])
            elif piece == ROI_NOIR or piece == ROI_BLANC:
                pMoves += self.king_movement(pieces[i])
                kingSurroundings = self.getKingSurrondings(pieces[i])
                kingPosition = pieces[i]
        
        # Si le roi est directement menacé par une pièce on retourne uniquement les mouvement permettant de le protéger
        protectionList = self.getKingProtectionList(kingSurroundings)     

        if len(kingSurroundings) > 0 :
            kingSurroundingsFlattened = [kingSurroundings[i][1][j] for i in range(len(kingSurroundings)) for j in range(len(kingSurroundings[i][1]))]
            return [pMoves[i] for i in range(len(pMoves)) if pMoves[i][1] in kingSurroundingsFlattened and not(pMoves[i][0] in protectionList) or pMoves[i][0] == kingPosition ]
            
        return [pMoves[i] for i in range(len(pMoves)) if not(pMoves[i][0] in protectionList)]

    def getPieceCoordinatesInBetweenPath(self,path):
        return [path[i] for i in range(len(path)) if getPiece(self.grille,path[i]) != 0]


    def getKingProtectionList(self,kingSurroundings):
        protectList = []
        threatenedPathsToRemove = []

        for i in range(len(kingSurroundings)):

            if(kingSurroundings[i][0] == "STRAIGHT" or kingSurroundings[i][0] == "DIAGONAL"):

                length = len(kingSurroundings[i][1]) - 1
                pieces = self.getPieceCoordinatesInBetweenPath(kingSurroundings[i][1][:length])

                if len(pieces) > 0:
                    threatenedPathsToRemove.append(i)
                if len(pieces) == 1:
                    protectList += pieces
    

        for j in range(len(threatenedPathsToRemove)):
            kingSurroundings.pop(threatenedPathsToRemove[j])

        return protectList
            




    def getKingSurrondings(self,coord):

        dangerousCoordinates = []

        straight = self.straightPathsFromPiece(coord,HEIGHT,WIDTH)
        diagonals = self.diagonalPathsFromPiece(coord,WIDTH)

        straightLineEnemies = {TOUR_BLANC,DAME_BLANCHE} if self.grille[coord[0]][coord[1]] < 0 else {TOUR_NOIR,DAME_NOIRE}
        diagonalLineEnemies = {FOU_BLANC,DAME_BLANCHE} if self.grille[coord[0]][coord[1]] < 0 else {FOU_NOIR,DAME_NOIRE}
        knightEnemy = CAVALIER_BLANC if self.grille[coord[0]][coord[1]] < 0 else CAVALIER_NOIR

        for i in range(len(straight)):

            """ On vérifie bien que la dernière pièce dans la direction choisi est une pièce ennemie 
            ayant la capacité de mettre en danger le roi, 
            On vérifie aussi qu'entre ses deux pièces il n'existe pas une pièce allié """

            if getPiece(self.grille,straight[i][len(straight[i]) - 1]) in straightLineEnemies:
                dangerousCoordinates.append(("STRAIGHT",straight[i][1:]))
        

        for i in range(len(diagonals)):
            
            if getPiece(self.grille,diagonals[i][len(diagonals[i]) - 1]) in diagonalLineEnemies:
                dangerousCoordinates.append(("DIAGONAL",diagonals[i][1:]))

        knights = self.knight_movement(coord)
        threateningKnights = [knights[i][1] for i in range(len(knights)) if self.grille[knights[i][1][0]][knights[i][1][1]] == knightEnemy]
        
        if(len(threateningKnights)>0):
            dangerousCoordinates.append(("L",threateningKnights))

        return dangerousCoordinates


    def straightPathsFromPiece(self,coord,height,width):

        possible_movements = [[coord] for _ in range(4)]
        y, x = coord[0], coord[1]
        add1,add2 = True,True

        for i in range(1,height):

            if(areCoordinatesBounded(y+i,x) and add1):
                if checkCanEat(self.grille,coord,(y+i,x)) :
                    add1 = False
                possible_movements[0].append((y+i,x))

            if(areCoordinatesBounded(y-i,x) and add2):
                if checkCanEat(self.grille,coord,(y-i,x)) :
                    add2 = False
                possible_movements[1].append((y-i,x))
    
        add1,add2 = True,True

        for j in range(1,width):

            if(areCoordinatesBounded(y,x+j) and add1):
                if checkCanEat(self.grille,coord,(y,x+j)) :
                    add1 = False
                possible_movements[2].append((y,x+j))

            if(areCoordinatesBounded(y,x-j) and add2):
                if checkCanEat(self.grille,coord,(y,x-j)) :
                    add2 = False
                possible_movements[3].append((y,x-j))

        return possible_movements



    def diagonalPathsFromPiece(self,coord,MAX):

        paths = [[coord] for _ in range(4)] 
        y, x= coord[0], coord[1] 
        
        add_dir1 = True
        add_dir2 = True
        add_dir3 = True
        add_dir4 = True

        for i in range(1,MAX):
            if(areCoordinatesBounded(y+i,x+i) and add_dir1):
                # On vérifie que si il y a un danger sur la diagonal
                if checkCanEat(self.grille,coord,(y+i,x+i)):
                    add_dir1 = False
                paths[0].append((y+i,x+i))

            if(areCoordinatesBounded(y-i,x-i) and add_dir2):
                if checkCanEat(self.grille,coord,(y-i,x-i)):
                    add_dir2 = False
                paths[1].append((y-i,x-i))
            
            if(areCoordinatesBounded(y+i,x-i) and add_dir3):
                if checkCanEat(self.grille,coord,(y+i,x-i)):
                    add_dir3 = False
                paths[2].append((y+i,x-i))

            if(areCoordinatesBounded(y-i,x+i) and add_dir4):
                if checkCanEat(self.grille,coord,(y-i,x+i)):
                    add_dir4 = False
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

        if(areCoordinatesBounded(coord[0] + move_value,coord[1] ) and checkCaseEmpty(self.grille,(coord[0] + move_value,coord[1]))):
            movement_list.append((coord,(coord[0] + move_value,coord[1])))

            if(coord[0] == special_position and checkCaseEmpty(self.grille,(coord[0] + move_value*2,coord[1]))) :
                movement_list.append((coord,(coord[0]+ move_value * 2,coord[1])))
        
        movement_list += self.pawn_eatPieceMovements(coord,-move_value)        
        return movement_list
                

    def pawn_ThreatenedCases(self,coord,color):
        
        move_value = 1 if color < 0 else -1
        threatenedCases = []

        pMovements = [(coord[0]+move_value,coord[1]+move_value),(coord[0]+move_value,coord[1]-move_value)]

        for i in range(0,len(pMovements)):
            if(areCoordinatesBounded(pMovements[i][0],pMovements[i][1])):
                threatenedCases.append(pMovements[i])
        
        return threatenedCases

    def pawn_eatPieceMovements(self,coord,color):

        threatenedCases = self.pawn_ThreatenedCases(coord,color)
        movement_list = []

        for i in range(0,len(threatenedCases)):
            if(checkCaseHasEdible(self.grille,coord,threatenedCases[i])):
                movement_list.append((coord,threatenedCases[i]))

        return movement_list 


    def knight_movement(self,coord):

        movement_list = []
        movements = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

        for i in range(len(movements)):

            new_y = coord[0] + movements[i][0]
            new_x = coord[1] + movements[i][1]

            if(areCoordinatesBounded(new_y,new_x)):
                if(checkCaseEmpty(self.grille,(new_y,new_x)) or checkCanEat(self.grille,coord,(new_y,new_x))):
                    movement_list.append((coord,(new_y,new_x)))

        return movement_list

    def bishop_movement(self,coord,MAX):
        
        diagonalPaths = self.diagonalPathsFromPiece(coord,MAX)
        pMovements = []

        for i in range(len(diagonalPaths)):
            for j in range(1,len(diagonalPaths[i])):
                if not(checkCaseEmpty(self.grille,diagonalPaths[i][j])) and not(checkCanEat(self.grille,coord,diagonalPaths[i][j])):
                    break
                pMovements.append((coord,diagonalPaths[i][j]))
        
        return pMovements
        

    
    def rook_movement(self,coord,width,height):

        straightPaths = self.straightPathsFromPiece(coord,height,width)
        pMovements = []

        
        for i in range(len(straightPaths)):
            for j in range(1,len(straightPaths[i])):
                if not(checkCaseEmpty(self.grille,straightPaths[i][j])) and not(checkCanEat(self.grille,coord,straightPaths[i][j])):
                    break
                pMovements.append((coord,straightPaths[i][j]))

        return pMovements


    def queen_movement(self,coord):
        return self.rook_movement(coord,WIDTH,HEIGHT) + self.bishop_movement(coord,WIDTH)
    
    def getThreatenedCases(self,board,color):

        threatenedCoordinates = []

        FOU_ADVERSE = FOU_NOIR if color > 0 else FOU_BLANC
        TOUR_ADVERSE = TOUR_NOIR if color > 0 else TOUR_BLANC
        CAVALIER_ADVERSE = CAVALIER_NOIR if color > 0 else CAVALIER_BLANC
        DAME_ADVERSE = DAME_NOIRE if color > 0 else DAME_BLANCHE
        PION_ADVERSE = PION_NOIR if color > 0 else PION_BLANC

        opponent_pieces = getPiecesCoordinates(self.grille,FOU_ADVERSE) + getPiecesCoordinates(self.grille,TOUR_ADVERSE) + getPiecesCoordinates(self.grille,DAME_ADVERSE) + getPiecesCoordinates(self.grille,CAVALIER_ADVERSE)
        opponent_pieces += getPiecesCoordinates(self.grille,PION_ADVERSE)

        for i in range(0,len(opponent_pieces)):

            piece = getPiece(board,opponent_pieces[i])

            if(piece == FOU_ADVERSE):
                threatenedCoordinates += self.bishop_movement(opponent_pieces[i],WIDTH)
            elif(piece == TOUR_ADVERSE):
                threatenedCoordinates += self.rook_movement(opponent_pieces[i],WIDTH,HEIGHT)
            elif(piece == CAVALIER_ADVERSE):
                threatenedCoordinates += self.knight_movement(opponent_pieces[i])
            elif(piece == DAME_ADVERSE):
                threatenedCoordinates += self.queen_movement(opponent_pieces[i])
            elif(piece == PION_ADVERSE):
                threatenedCoordinates += self.pawn_ThreatenedCases(opponent_pieces[i],-PION_ADVERSE)

        return threatenedCoordinates
        


    def king_movement(self,coord):

        possible_positions = self.rook_movement(coord,2,2) + self.bishop_movement(coord,2)
        king = getPiece(self.grille,coord)

        piecesToRemove = [(coord,king)]

        """ We need to know whether or not the adjacents pieces to our king are protected, in order
        to do that we remove them from the board and check if their position are in the threatened position list """

        for i in range(len(possible_positions)):
            if not(checkCaseEmpty(self.grille,possible_positions[i][1])):
                piecesToRemove.append((possible_positions[i][1],getPiece(self.grille,possible_positions[i][1])))
        
        emptyCase(self.grille,piecesToRemove[0][0])
        opponent_movements = self.getThreatenedCases(self.grille,king)


        for j in range(1,len(piecesToRemove)):
            emptyCase(self.grille,piecesToRemove[j][0])


        opponent_movements += self.getThreatenedCases(self.grille,king)

        
        for z in range(len(piecesToRemove)):
            addPieceToCase(self.grille,piecesToRemove[z][0],piecesToRemove[z][1])

        opponent_movements += self.getThreatenedCases(self.grille,king)
        
        opponent_movements_pos = [opponent_movements[i][1] for i in range(0,len(opponent_movements))]
        positions = [possible_positions[i] for i in range(0,len(possible_positions)) if not(possible_positions[i][1] in opponent_movements_pos)]

        return positions



