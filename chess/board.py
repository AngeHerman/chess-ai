from chess.constants import *

class Board:
    def __init__(self):
        self.grille = [
            [TOUR_NOIR, CAVALIER_NOIR, FOU_NOIR, DAME_NOIRE, ROI_NOIR, FOU_NOIR, CAVALIER_NOIR, TOUR_NOIR],
            [PION_NOIR] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [PION_BLANC] * 8,
            [TOUR_BLANC, CAVALIER_BLANC, FOU_BLANC, DAME_BLANCHE, ROI_BLANC, FOU_BLANC, CAVALIER_BLANC, TOUR_BLANC]
        ]

    def print_Board(self):
        for ligne in self.grille:
            print(ligne)

    def play_move(self, coup):
        # Creeeer coup apres
        pass

    def moves(self, coord_depart):
        # Trouver un moyen de generrer les coups 
        pass
