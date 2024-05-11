import threading
import os
import time
from chess.board2 import *
from chess.utils import *
from tests.test_board import *
from tests.test_more import *
from tests.test_alpha_beta import *
from tests.test_alpha_beta_multiprocess_section import *
from tests.test_genetic_algorithm import *

from api.lichess import *
from ai.monte_carlo import *
from ai.alpha_beta import *
from ai.more import *
from ai.opening import *
from ai.alpha_beta_multi_process_section import *
from game import *

import threading
import time
import os
import pickle
import random

QUICK_SLEEP_TIME = 0
ONE_SEC_SLEEP_TIME = 1

ITERATION_RECHERCHER_COUP = 50
NOMBRE_ERREUR_AVANT_ARRET_JEU = 1
ITERATION_BOUCLE_PRINCIPALE = 100
OUR_IA_LEVELS = ["0","1", "2", "3", "4"]
LICHESS_IA_LEVELS = ["1", "2", "3", "4","5", "6", "7", "8"]

def choice_our_ai_againt_lichess_ai():
    print("Vous avez choisi de lancer notre IA contre celle de Lichess. Voici les nivea de notre IA")
    print("Niveau 0: Move hasardeux, surtout pour les tests")
    print("Niveau 1: Mobte Carlo  (Prends beaucoup trop de temps)")
    print("Niveau 2: Algorythme Genétique  (Prends beaucoup trop de temps aussi)")
    print("Niveau 3: Alpha-Beta de profondeur 1  (1 seconde max)")
    print("Niveau 4: Alpha-Beta de profondeur 2  (5 secondes max)")

    while True:
        ia_level = input(f"Entrez le niveau de notre IA {OUR_IA_LEVELS} : ")
        lichess_level = input(f"Entrez le niveau de Lichess {LICHESS_IA_LEVELS} : ")
        
        if ia_level in OUR_IA_LEVELS and lichess_level in LICHESS_IA_LEVELS:
            return ia_level, lichess_level
        else:
            print(f"Niveau invalide. Veuillez entrer {OUR_IA_LEVELS} pour le niveau de notre IA et {LICHESS_IA_LEVELS} pour le niveau de Lichess.")
            
def choice_play_againt_our_ai():
    print("Vous avez choisi de jouer contre notre IA.")
    print("Niveau 0: Move hasardeux, surtout pour les tests")
    print("Niveau 1: Mobte Carlo  (Prends beaucoup trop de temps)")
    print("Niveau 2: Algorythme Genétique  (Prends beaucoup trop de temps aussi)")
    print("Niveau 3: Alpha-Beta de profondeur 1  (1 seconde max)")
    print("Niveau 4: Alpha-Beta de profondeur 2  (5 secondes max)")
    while True:
        ia_level = input(f"Entrez le niveau de notre IA {OUR_IA_LEVELS} : ")
        
        if ia_level in OUR_IA_LEVELS:
            return ia_level
        else:
            print(f"Niveau invalide. Veuillez entrer {OUR_IA_LEVELS} pour le niveau de notre IA")

def menu():
    while True:
        print("Menu:")
        print("1. Jouer contre notre IA")
        print("2. Lancer notre IA contre celle de Lichess")
        print("3. Lancer des tests")
        print("4. Quitter")
        choice = input("Entrez votre choix (1, 2, 3 ou 4) : ")

        if choice == "1":
            ia_level = choice_play_againt_our_ai()
            play_against_player_o(ia_level)
            break
        elif choice == "2":
            ia_level, lichess_level = choice_our_ai_againt_lichess_ai()
            play_against_ai_o(ia_level, lichess_level)
            break
        elif choice == "3":
            print("Vous avez choisi de lancer des tests.")
            test_alpha_beta()
            break
        elif choice == "4":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")

