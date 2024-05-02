import random
import copy
from chess.board2 import *
from ai.more import *
import time
import math

SEQUENCE_LENGTH = 3 # How many moves on a sequence
POPULATION_SIZE = 50
SELECTION_RATE = 0.2 # 20 % des bests
MUTATION_RATE = 0.1
MAX_GENERATION = 5

def generate_random_move():
    random.seed(time.time())
    start_position = (random.randint(0, HEIGHT-1), random.randint(0, WIDTH - 1))
    end_position = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
    return start_position, end_position

def generate_individual(board):
    sequence = []
    sequence.append(random.choice(board.pMoves))
    for i in range(SEQUENCE_LENGTH-1):
        sequence.append(generate_random_move())
    return sequence

def generate_population(board, color_of_player_turn):
    board.getAllMovesBasedOnTurn()
    return [(evaluate_fitness(board, color_of_player_turn, sequence), sequence) for sequence in [generate_individual(board) for i in range(POPULATION_SIZE)]]

def evaluate_fitness(board,color_of_player_turn, sequence):
    board_copy = copy.deepcopy(board)
    moves_passed = True
    for move in sequence:
        board_copy.getAllMovesBasedOnTurn()
        moves_passed = board_copy.play_move(move)
        if not moves_passed:
            break
    if moves_passed:
        return evaluate_board(board_copy)
    else:
        if color_of_player_turn == BLANC:
            return -math.inf
        else:
            return math.inf

def select_parents(population, color_of_player_turn):
    if color_of_player_turn == BLANC:
        sorted_population = sorted(population, key=lambda x: x[0],reverse=True)
    else:
        sorted_population = sorted(population, key=lambda x: x[0])

    selected_count = int(SELECTION_RATE * len(population))    
    return sorted_population[:selected_count]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

def get_mutation_point(board, sequence):
    board_copy = copy.deepcopy(board)
    mutation_point = 0
    for move in sequence:
        board_copy.getAllMovesBasedOnTurn()
        moves_passed = board_copy.play_move(move)
        if not moves_passed:
            break
        mutation_point += 1
    return mutation_point
    
        
def mutate(sequence, board):
    # print("Mutation")
    mutation_point = get_mutation_point(board,sequence)
    if  mutation_point < len(sequence):
        turn = board.turn + mutation_point
        color = BLANC if turn%2 == 1 else NOIR
        moves = board.getAllAvailableMoves(color) # Can skip good moves, maybe need to be randomize
        random.seed(time.time())
        new_move = random.choice(moves)
        sequence_list = list(sequence)
        sequence_list[mutation_point] = new_move
        res = tuple(sequence_list)
        return res
    return sequence

def evaluate_board(board):
    color = BLANC if board.turn%2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board.grille, color,board.endGame(),move_of_current_player)

def select_best_individuals(population,color_of_player_turn):
    if color_of_player_turn == BLANC:
        sorted_population = sorted(population, key=lambda x: x[0], reverse=True)
    else:
        sorted_population = sorted(population, key=lambda x: x[0])
    return sorted_population[:POPULATION_SIZE]

def genetic_algorithm(board, color_of_player_turn):
    population = generate_population(board,color_of_player_turn)
    fitness_fn = lambda sequence: evaluate_fitness(board,color_of_player_turn, sequence)

    for generation in range(MAX_GENERATION):
        print("GENERATION")
        parents = select_parents(population,color_of_player_turn)
        offspring = []
        # POPULATION_SIZE instead of len(population) because len(population) is going exponential
        while len(offspring) < POPULATION_SIZE:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1[1], parent2[1])
            child = mutate(child, board)
            offspring.append((fitness_fn(child), child))

        population += offspring
        population = select_best_individuals(population,color_of_player_turn)

    best_sequence = max(population, key=lambda x: x[0])[1]
    return best_sequence


# Utilisation de l'algorithme génétique pour trouver la meilleure séquence de coups
# board = Board2()
# genetic_algorithm = GeneticAlgorithmChess(board)
# best_sequence = genetic_algorithm.run_genetic_algorithm()
# print("Meilleure séquence de coups trouvée par l'algorithme génétique:", best_sequence)
