from chess.constants import *
from chess.utils import *
from chess.piece import *

from chess.rook import *
from chess.knight import *
from chess.pawn import *
from chess.bishop import *
from chess.queen import *
from chess.king import *

import copy

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
        self.spMoves = []
        self.isGameEnded = False
        self.enPassantAllowed = 0

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
        piece.moveCount += 1

        if self.checkRoque(piece,coup[1]):
            self.doRoque(piece,coup[1])
            gagnant = self.endGame()
            return True
        if coup[-1] == "":
            emptyCase(self.grille,coup[0])
            addPieceToCase(self.grille,coup[1],piece)
            self.turn += 1
            gagnant = self.endGame()
            return True
        else:
            self.promotePiece(piece,coup[-1],coup[1])
            gagnant = self.endGame()
            return True

    def play_move(self, coup):
        if coup in self.pMoves:
            piece = getPiece(self.grille,coup[0])
            piece.moveCount += 1

            if(self.enPassantAllowed):
                self.forbid_enPassant(piece.color)
                if(self.check_moveEnPassant(piece,coup)):
                    self.enPassantEatPiece(coup,piece)
                    return True

            if(self.check_enPassant(piece,coup)):
                self.allow_enPassant(piece)

            if self.checkRoque(piece,coup[1]):
                self.doRoque(piece,coup[1])
                gagnant = self.endGame()
                return True
            if coup[-1] == "":
                emptyCase(self.grille,coup[0])
                addPieceToCase(self.grille,coup[1],piece)
                self.turn += 1
                gagnant = self.endGame()
                return True
            else:
                self.promotePiece(piece,coup[-1],coup[1])
                gagnant = self.endGame()
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
            # print("Fin du jeu Noir tour ",end=str(self.turn))
        elif len(moveNoir) == 0:
            gagnant = BLANC
            self.isGameEnded = True
            # print("Fin du jeu Blanc tour ",end=str(self.turn))
        # if(self.turn < 200):
        #     print("Continue jeu tour ",end=str(self.turn))
        return gagnant

    def returnAllMovesBasedOnTurn(self):
        color = BLANC if self.turn%2 == 1 else NOIR
        return self.getAllAvailableMoves(color)  
    
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

            if pieces[i].name == ROI:
                kingSurroundings = self.getKingSurrondings(pieces[i])
                kingPosition = pieces[i].coordinates
                if pieces[i].moveCount == 0:
                    pMoves += self.checkRoqueAvailability(kingPosition)


        # Si le roi est directement menacé par une pièce on retourne uniquement les mouvement permettant de le protéger
        kingSurroundingsFlattened = [kingSurroundings[i][1][j] for i in range(len(kingSurroundings)) for j in range(len(kingSurroundings[i][1]))]
        protectionList = self.getKingProtectionList(kingSurroundings)  

        if len(kingSurroundings) > 0 :
            kingSurroundingsFlattened = [kingSurroundings[i][1][j] for i in range(len(kingSurroundings)) for j in range(len(kingSurroundings[i][1]))]
            temp = [pMoves[i] for i in range(len(pMoves)) if pMoves[i][1] in kingSurroundingsFlattened and not(pMoves[i][0] in protectionList) or pMoves[i][0] == kingPosition ]
            return temp

        return [pMoves[i] for i in range(len(pMoves)) if not(pMoves[i][0] in protectionList) or pMoves[i][1] in kingSurroundingsFlattened]
        
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

        straightLineEnemies = {TOUR,DAME} 
        diagonalLineEnemies = {FOU,DAME}
        knightEnemy = CAVALIER

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
                if retrievePiece.name == PION and retrievePiece.color != piece.color and len(diagonals[i]) == 2:
                    dangerousCoordinates.append(("DIAGONAL",diagonals[i][1:]))

        simulated_Knight = Knight(piece.color)
        simulated_Knight.setCoordinates(piece.coordinates)
        knights = simulated_Knight.knight_movement(self.grille)

        threateningKnights = [knights[i][1] for i in range(len(knights)) if checkPieceName(self.grille,knights[i][1],knightEnemy)]
        
        if(len(threateningKnights)>0):
            dangerousCoordinates.append(("L",threateningKnights))

        return dangerousCoordinates

    def checkRoque(self,piece,coord2):

        if piece.name == ROI:
            if abs(coord2[1] - piece.coordinates[1]) >= 2:
                return True
        return False

    def doRoque(self,kingPiece,coup):

        rookPieceCoordinates = (coup[0],WIDTH - 1 if coup[1] > kingPiece.coordinates[1] else 0)
        rookPiece = getPiece(self.grille,rookPieceCoordinates)
        direction = 1 if rookPiece.coordinates[1] > kingPiece.coordinates[1] else -1
        
        kingNewCoordinates = (kingPiece.coordinates[0],kingPiece.coordinates[1]+direction*2)
        rookNewCoordinates = (kingNewCoordinates[0],kingNewCoordinates[1]-direction)

        emptyCase(self.grille,rookPiece.coordinates)
        emptyCase(self.grille,kingPiece.coordinates)
        addPieceToCase(self.grille,kingNewCoordinates,kingPiece)
        addPieceToCase(self.grille,rookNewCoordinates,rookPiece)

        kingPiece.moveCount += 1
        rookPiece.moveCount += 1

        self.turn += 1

    def checkRoqueAvailability(self,kingCoordinates):
        kingPiece = getPiece(self.grille,kingCoordinates)
        specialMovement = []
        if(kingPiece.moveCount > 0):
            return specialMovement

        straight = straightPathsFromPiece(kingPiece,self.grille,HEIGHT,WIDTH)
        threatenedPositions = getThreatenedCases(self.grille,kingPiece)
        
        for i in range(len(straight)):

            coordinates = straight[i][len(straight[i]) - 1]
            piecesInBetweenPath = self.getPieceCoordinatesInBetweenPath(straight[i])
            if len(piecesInBetweenPath) > 2:
                continue
            if checkPieceColor(self.grille,coordinates,kingPiece.color) and checkPieceName(self.grille,coordinates,"Tour"):
                piece = getPiece(self.grille,coordinates)

                if piece.moveCount == 0:

                    direction = -1 if piece.coordinates[1] < kingCoordinates[1] else 1
                    kingNewCoordinates = (kingCoordinates[0],kingCoordinates[1]+direction*2)
                    rookNewCoordinates = (kingNewCoordinates[0],kingNewCoordinates[1]-direction)
                    specialMovement.append((kingCoordinates,kingNewCoordinates))
        
        return specialMovement
    

    def promotePiece(self,piece,newPieceName,coord):

        newPiece = None
        
        if(newPieceName == "q"):
            newPiece = Queen(piece.color)
        elif(newPieceName == "n"):
            newPiece = Knight(piece.color)
        elif(newPieceName == "b"):
            newPiece = Bishop(piece.color)
        elif(newPieceName == "r"):
            newPiece = Rook(piece.color)

        emptyCase(self.grille,piece.coordinates)
        emptyCase(self.grille,coord)
        addPieceToCase(self.grille,coord,newPiece)
        self.turn += 1

    def checkPieceThreatened(self,color,pieceName):
        adversaryColor = getAdvesaryColor(color)
        threatenedList = getThreatenedCases(self.grille,adversaryColor)

        for i in range(len(threatenedList)):
            if checkPieceName(self.grille,threatenedList[i],pieceName):
                return True

        return False     
       
    def enPassantEatPiece(self,coup,piece):
            emptyCase(self.grille,(coup[1][0] - piece.direction,coup[1][1] ))
            emptyCase(self.grille,coup[0])
            addPieceToCase(self.grille,coup[1],piece)
            self.turn += 1
            self.endGame()

    def check_enPassant(self,piece,coup):
        if checkPieceName(self.grille,piece.coordinates,PION):
            special_position = 4
            if piece.color == BLANC :
                special_position = 3
            return piece.coordinates[0] == special_position - (piece.direction * 2) and coup[1][0] == special_position
        
    def check_moveEnPassant(self,piece,coup):
        if checkPieceName(self.grille,piece.coordinates,PION):
            diagonalMove = coup[1][1] == piece.coordinates[1] + 1 or coup[1][1] == piece.coordinates[1] - 1
            return  diagonalMove and not(checkCaseHasEdible(self.grille,piece.coordinates,coup[1]))

    def allow_enPassant(self,piece):
        self.enPassantAllowed = 1
        adversaryPawns = getAllPiecesWithNameColor(self.grille,PION,-piece.color)
        for i in range(len(adversaryPawns)):
            adversaryPawns[i].en_passant = 1

    def forbid_enPassant(self,color):
        self.enPassantAllowed = 0
        adversaryPawns = getAllPiecesWithNameColor(self.grille,PION,color)
        for i in range(len(adversaryPawns)):
            adversaryPawns[i].en_passant = 0
            
    def check_petit_roque(self, color):
        king_row = 0 if color == BLANC else 7
        king = self.grille[king_row][3]  # Pos roi
        rook = self.grille[king_row][0]  # Rook côté roi
        
        #Ckecking roque
        if king is not None and rook is not None\
        and isinstance(king, King) and isinstance(rook, Rook) \
                and king.moveCount == 0 and rook.moveCount == 0 \
                and all(self.grille[king_row][col] is None for col in range(1, 3)):
            return True
        return False

        

