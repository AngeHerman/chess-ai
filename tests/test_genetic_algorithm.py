from chess.board2 import *
from chess.utils import *
from chess.king import *
from ai.genetic_algorithm import *
import pickle
import time

def test_genetic_algo():
    # test_generate_population()
    # test_genetic_situation_1()
    test_speed()

def test_generate_population():
    plateau = Board2()
    population = generate_population(plateau)
    print(f"Taille : {len(population)}")
    print(population)
    
    
def test_genetic_situation_1():
    # https://lichess.org/OwrcrsOB/black#11 tour 6 (11 moves)
    plateau = Board2()
    moves = ['e2e4', 'e7e6', 'd2d3', 'f8b4', 'c1d2', 'b4f8', 'b1c3', 'f8b4', 'a2a3', 'b4c3', 'd1c1']

    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    print(genetic_algorithm(plateau,BLANC))

    
def test_speed():
    # https://lichess.org/OwrcrsOB/black#11 tour 6 (11 moves)
    plateau = Board2()
    moves = ['e2e4', 'e7e6', 'd2d3', 'f8b4', 'c1d2', 'b4f8', 'b1c3', 'f8b4', 'a2a3', 'b4c3', 'd1c1']

    for mm in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move( mm))
    plateau.print_Board()
    start_time = time.time()
    print(genetic_algorithm(plateau,BLANC))
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de genetic: ", execution_time, "secondes")
    
    start_time = time.time()
    print(genetic_algorithm_threads(plateau,BLANC))
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de genetic threads: ", execution_time, "secondes")
    
    start_time = time.time()
    print(genetic_algorithm_processus(plateau,BLANC))
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de genetic processus: ", execution_time, "secondes")