from chess.constants import *
from chess.utils import *
from chess.piece import *

from chess.rook import *
from chess.knight import *
from chess.pawn import *
from chess.bishop import *
from chess.queen import *
from chess.king import *



class Board2:
    def __init__(self):
        self.grille = [
            [Rook(BLANC), Knight(BLANC), Bishop(BLANC), Queen(BLANC),  King(BLANC), Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
            [Pawn(BLANC)]* 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn(NOIR)] * 8,
            [Rook(NOIR),CAVALIER_NOIR, Bishop(NOIR),  Queen(NOIR), King(NOIR), Bishop(NOIR), Knight(NOIR), Rook(NOIR)]
        ]
        self.turn = 0
        self.pMoves = []
        self.isGameEnded = False

    def print_Board(self):
        for ligne in self.grille:
            for colonne in self.grille[ligne]:
                if(self.grille[ligne][colonne] != None):
                    self.grille[ligne][colonne].print()
                else:
                    print(0)

    def initializeCoordinates(self):
        for y in self.grille:
            for x in self.grille[y]:
                if(self.grille[y][x] != None):
                    self.grille[y][x].coordinates((y,x))
            
    def play_move(self, coup):

        if coup in self.pMoves:

            piece = getPiece(self.grille,coup[0])
            emptyCase(self.grille,coup[0])
            addPieceToCase(self.grille,coup[1],piece)
            piece.setCoordinates(coup[1])
            return True
        
        return False
    
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

    def moves(self, coord_depart):
        pass
        # Trouver un moyen de generrer les coups 
       # pass  
    def getAllMovesBasedOnTurn(self):

        self.turn += 1
        color = BLANC if self.turn%2 == 1 else NOIR
        self.pMoves = self.getAllAvailableMoves(color)            

    def getAllAvailableMoves(self,color):
        
        pMoves = []
        pieces = getAllPiecesCoordinatesFromColor(self.grille,color)
        kingSurroundings = []
        kingPosition = (0,0)
        
        for i in range(len(pieces)):
            
            pMoves.append(pieceMovement(pieces[i]))

            if pieces[i].name == "ROI":
                kingSurroundings = self.getKingSurrondings(pieces[i])
                kingPosition = pieces[i].coordinates
        
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
            
    def getKingSurrondings(self,piece):

        dangerousCoordinates = []

        straight = straightPathsFromPiece(piece,self.grille,HEIGHT,WIDTH)
        diagonals = diagonalPathsFromPiece(piece,self.grille,WIDTH)

        straightLineEnemies = {TOUR_BLANC,DAME_BLANCHE} if self.grille[piece.coordinates[0]][piece.coordinates[1]] < 0 else {TOUR_NOIR,DAME_NOIRE}
        diagonalLineEnemies = {FOU_BLANC,DAME_BLANCHE} if self.grille[piece.coordinates[0]][piece.coordinates[1]] < 0 else {FOU_NOIR,DAME_NOIRE}
        knightEnemy = CAVALIER_BLANC if self.grille[piece.coordinates[0]][piece.coordinates[1]] < 0 else CAVALIER_NOIR

        for i in range(len(straight)):

            """ On vérifie bien que la dernière pièce dans la direction choisi est une pièce ennemie 
            ayant la capacité de mettre en danger le roi, 
            On vérifie aussi qu'entre ses deux pièces il n'existe pas une pièce allié """

            if getPiece(self.grille,straight[i][len(straight[i]) - 1]) in straightLineEnemies:
                dangerousCoordinates.append(("STRAIGHT",straight[i][1:]))
        

        for i in range(len(diagonals)):
            
            if getPiece(self.grille,diagonals[i][len(diagonals[i]) - 1]) in diagonalLineEnemies:
                dangerousCoordinates.append(("DIAGONAL",diagonals[i][1:]))

        knights = self.knight_movement(piece.coordinates)
        threateningKnights = [knights[i][1] for i in range(len(knights)) if self.grille[knights[i][1][0]][knights[i][1][1]] == knightEnemy]
        
        if(len(threateningKnights)>0):
            dangerousCoordinates.append(("L",threateningKnights))

        return dangerousCoordinates