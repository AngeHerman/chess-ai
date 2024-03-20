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
            [Rook(BLANC), Knight(BLANC), Bishop(BLANC),  King(BLANC), Queen(BLANC), Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
            [Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC),Pawn(BLANC)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR),Pawn(NOIR)],
            [Rook(NOIR),Knight(NOIR), Bishop(NOIR),  King(NOIR), Queen(NOIR), Bishop(NOIR), Knight(NOIR), Rook(NOIR)]
        ]
        self.initializeCoordinates()
        self.turn = 1
        self.pMoves = []
        self.isGameEnded = False

    def print_Board(self):
        for ligne in range(0,len(self.grille)):
            print("[",end="")
            for colonne in range(0,len(self.grille[ligne])):
                if(isinstance(self.grille[ligne][colonne],Piece)):
                    self.grille[ligne][colonne].print()
                    if colonne < len(self.grille[ligne]) - 1:
                        print(", ",end="")
                else:
                    print(0,end="")
                    if colonne <len(self.grille[ligne]) - 1:
                        print(", ",end="")

            print("]")

    def initializeCoordinates(self):
        for y in range(0,len(self.grille)):
            for x in range(0,len(self.grille[y])):
                if(isinstance(self.grille[y][x],Piece)):
                    self.grille[y][x].setCoordinates((y,x))

    
    def force_play_move(self, coup):
        piece = getPiece(self.grille,coup[0])
        emptyCase(self.grille,coup[0])
        addPieceToCase(self.grille,coup[1],piece)
        self.turn += 1
        return True


    def play_move(self, coup):

        if coup in self.pMoves:

            piece = getPiece(self.grille,coup[0])
            piece.moveCount += 1
            emptyCase(self.grille,coup[0])
            addPieceToCase(self.grille,coup[1],piece)
            self.turn += 1
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

        color = BLANC if self.turn%2 == 1 else NOIR
        self.pMoves = self.getAllAvailableMoves(color)            

    def getAllAvailableMoves(self,color):
        
        pMoves = []
        pieces = getAllPiecesFromColor(self.grille,color)
        kingSurroundings = []
        kingPosition = (0,0)
        
        for i in range(len(pieces)):
            
            pMoves += pieceMovement(pieces[i],self.grille)

            if pieces[i].name == "Roi":
                kingSurroundings = self.getKingSurrondings(pieces[i])
                kingPosition = pieces[i].coordinates
                
        # Si le roi est directement menacé par une pièce on retourne uniquement les mouvement permettant de le protéger
        protectionList = self.getKingProtectionList(kingSurroundings)    
        if len(kingSurroundings) > 0 :
            kingSurroundingsFlattened = [kingSurroundings[i][1][j] for i in range(len(kingSurroundings)) for j in range(len(kingSurroundings[i][1]))]
            temp = [pMoves[i] for i in range(len(pMoves)) if pMoves[i][1] in kingSurroundingsFlattened and not(pMoves[i][0] in protectionList) or pMoves[i][0] == kingPosition ]

            return temp

        return pMoves
        
    def getPieceCoordinatesInBetweenPath(self,path):
        return [path[i] for i in range(len(path)) if getPiece(self.grille,path[i]) != None]


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


        kingSurroundings2 = [kingSurroundings[i] for i in range(len(kingSurroundings)) if i in threatenedPathsToRemove]
        
        for i in range(len(kingSurroundings2)):
            kingSurroundings.remove(kingSurroundings2[i])

        return protectList
            
    def getKingSurrondings(self,piece):

        dangerousCoordinates = []

        straight = straightPathsFromPiece(piece,self.grille,HEIGHT,WIDTH)
        diagonals = diagonalPathsFromPiece(piece,self.grille,WIDTH)

        straightLineEnemies = {"Tour","Dame"} 
        diagonalLineEnemies = {"Fou","Dame"}
        knightEnemy = "Cavalier"

        for i in range(len(straight)):

            """ On vérifie bien que la dernière pièce dans la direction choisi est une pièce ennemie 
            ayant la capacité de mettre en danger le roi, 
            On vérifie aussi qu'entre ses deux pièces il n'existe pas une pièce allié """
            retrievePiece = getPiece(self.grille,straight[i][len(straight[i]) - 1])
            if retrievePiece != None:
                if (retrievePiece.name in straightLineEnemies) and retrievePiece.color != piece.color :
                    dangerousCoordinates.append(("STRAIGHT",straight[i][1:]))
        

        for i in range(len(diagonals)):

            retrievePiece = getPiece(self.grille,diagonals[i][len(diagonals[i]) - 1]) 
            if retrievePiece != None:
                if retrievePiece.name  in diagonalLineEnemies and retrievePiece.color != piece.color :
                    dangerousCoordinates.append(("DIAGONAL",diagonals[i][1:]))

        simulated_Knight = Knight(piece.color)
        simulated_Knight.setCoordinates(piece.coordinates)
        knights = simulated_Knight.knight_movement(self.grille)

        threateningKnights = [knights[i][1] for i in range(len(knights)) if checkPieceName(self.grille,knights[i][1],knightEnemy)]
        
        if(len(threateningKnights)>0):
            dangerousCoordinates.append(("L",threateningKnights))

        return dangerousCoordinates
    
    
    def check_Roque(self,kingCoordinates):

        kingPiece = getPiece(self.grille,kingCoordinates)

        if(kingPiece.moveCount > 0):
            return

        straight = straightPathsFromPiece(kingPiece,self.grille,HEIGHT,WIDTH)
        threatenedPositions = getThreatenedCases(self.grille,kingPiece)
        
        for i in range(len(straight)):

            coordinates = straight[i][len(straight[i]) - 1]
            if checkPieceColor(self.grille,coordinates,kingPiece.color) and checkPieceName(self.grille,coordinates,"Tour"):
                piece = getPiece(self.grille,coordinates)

                if piece.moveCount == 0:

                    direction = -1 if piece.coordinates[1] > kingCoordinates[1] else 1
                    kingNewCoordinates = (kingCoordinates[0],kingCoordinates[1]+direction*2)
                    rookNewCoordinates = (kingNewCoordinates[0],kingNewCoordinates[1]-direction)
                    specialMovement = [("Castling",(piece.coordinates,rookNewCoordinates),(kingCoordinates,kingNewCoordinates))]

                


        

