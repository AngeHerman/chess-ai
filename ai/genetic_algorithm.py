import random
import copy
from chess.board2 import *
from ai.more import *
import time
import math
import threading
import multiprocessing



SEQUENCE_LENGTH = 3 # How many moves on a sequence
POPULATION_SIZE = 40
SELECTION_RATE = 0.2 # 20 % des bests
MUTATION_RATE = 0.1
MAX_GENERATION = 5

def generate_random_move():
    """Generate random move using board height and length
    """
    random.seed(time.time())
    start_position = (random.randint(0, HEIGHT-1), random.randint(0, WIDTH - 1))
    end_position = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
    return start_position, end_position

def generate_individual(board):
    """ Generate random moves of sequence length
    """
    sequence = []
    sequence.append(random.choice(board.pMoves))
    for i in range(SEQUENCE_LENGTH-1):
        sequence.append(generate_random_move())
    return sequence

def generate_existing_individual(board):
    """Generate individual/sequence but not random, using existing ones
        every sequence is mathced with its evaluation 
    """
    sequence = []
    copied_board = copy.deepcopy(board)
    for i in range(SEQUENCE_LENGTH):
        move = random.choice(copied_board.pMoves)
        sequence.append(move)
        copied_board.play_move(move)
        copied_board.getAllMovesBasedOnTurn()
    return sequence

def generate_existing_population(board, color_of_player_turn):
    """Generate population we are sure exists
    """
    board.getAllMovesBasedOnTurn()
    population = []
    for i in range(POPULATION_SIZE):
        sequence = generate_existing_individual(board)
        fitness = evaluate_fitness(board, color_of_player_turn, sequence)
        population.append((fitness, sequence))
    return population

def generate_population(board, color_of_player_turn):
    """Genrate random population of random move, most likely not possible moves
    """
    board.getAllMovesBasedOnTurn()
    population = []
    for i in range(POPULATION_SIZE):
        sequence = generate_individual(board)
        fitness = evaluate_fitness(board, color_of_player_turn, sequence)
        population.append((fitness, sequence))
    return population

def evaluate_fitness(board,color_of_player_turn, sequence):
    """Return evaluation of baord after a sequence of moves
        infinite for impossible sequence 
    """
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
    """Select best sequence that will serve as parents

    """
    selected_population = []
    for individual in population:
        if isinstance(individual[1], list):
            selected_population.append(individual)
    if color_of_player_turn == BLANC:
        # The white want to maximise score so their population is sorted from high to low
        sorted_population = sorted(selected_population, key=lambda x: x[0], reverse=True)
    else:
        sorted_population = sorted(selected_population, key=lambda x: x[0])

    selected_count = int(SELECTION_RATE * len(selected_population))    
    return sorted_population[:selected_count]

def crossover(parent1, parent2):
    """return new child of parents
    """
    crossover_point = random.randint(1, len(parent1) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

def get_mutation_point(board, sequence):
    """Return the index of the not allowed move
    """
    board_copy = copy.deepcopy(board)
    mutation_point = 0
    for move in sequence:
        board_copy.getAllMovesBasedOnTurn()
        moves_passed = board_copy.play_move(move)
        if not moves_passed:
            break
        mutation_point += 1
    return mutation_point
    
def get_replacement_move(board,sequence,mutatio_point):
    """Return the move that will replace the one at replacement point
        in the sequence
    """
    copied_board = copy.deepcopy(board)
    for i in range(mutatio_point):
        copied_board.getAllMovesBasedOnTurn()
        copied_board.play_move(sequence[i])
    copied_board.getAllMovesBasedOnTurn()
    new_move = random.choice(copied_board.pMoves)
    return new_move

def mutate(sequence, board):
    """Mutate the sequence if needed
    """
    # print("Mutation")
    mutation_point = get_mutation_point(board,sequence)
    if  mutation_point < len(sequence):
        # print("$$$$$$$$$$$$$$$ SHIT MUTATION")
        # turn = board.turn + mutation_point
        # color = BLANC if turn%2 == 1 else NOIR
        # moves = board.getAllAvailableMoves(color) # Can skip good moves, maybe need to be randomize
        # random.seed(time.time())
        # new_move = random.choice(moves)
        new_move = get_replacement_move(board,sequence,mutation_point)
        sequence_list = list(sequence)
        sequence_list[mutation_point] = new_move
        res = tuple(sequence_list)
        return res
    # print("YESSSSSSSSSSSSSSSSS NO MUTATION")
    return sequence

def evaluate_board(board):
    color = BLANC if board.turn%2 == 1 else NOIR
    move_of_current_player = board.getAllAvailableMoves(color)
    return board_score(board, color,board.endGame(),move_of_current_player)

def select_best_individuals(population,color_of_player_turn):
    """Select best sequence that will serve as parents
    """
    if color_of_player_turn == BLANC:
        sorted_population = sorted(population, key=lambda x: x[0], reverse=True)
    else:
        sorted_population = sorted(population, key=lambda x: x[0])
    return sorted_population[:POPULATION_SIZE]

def check_population_type(population):
    """Check  mal-formed individuls/sequence
    """
    for individual in population:
        if not isinstance(individual[1], list):
            # print(f"Je suis un mauvais individu : Me voici : {individual}")
            pass

def genetic_algorithm(board, color_of_player_turn):
    """Return best move

    Args:
        board (Board): board
        color_of_player_turn (int): color of the player that has to play

    Returns:
        move: Best move
    """
    population = generate_existing_population(board,color_of_player_turn)
    fitness_fn = lambda sequence: evaluate_fitness(board,color_of_player_turn, sequence)


    for generation in range(MAX_GENERATION):
        parents = select_parents(population,color_of_player_turn)
        new_gen = []
        # POPULATION_SIZE instead of len(population) because len(population) is going exponential
        while len(new_gen) < POPULATION_SIZE:
            random.seed(time.time())
            # parent1 = random.choice(parents)
            # random.seed(time.time())
            # parent2 = random.choice(parents)
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1[1], parent2[1])
            # while evaluate_fitness(board,color_of_player_turn,child) == math.inf or evaluate_fitness(board,color_of_player_turn,child) == -math.inf:
            #     child = mutate(child, board)
            
            # Only SEQUENCE_LENGTH - 1 moves need to be changed in the mutation
            for i in range(SEQUENCE_LENGTH-1):
                child = mutate(child, board)
            new_gen.append((fitness_fn(child), child))

        population += new_gen
        population = select_best_individuals(population,color_of_player_turn)

    best_sequence = max(population, key=lambda x: x[0])[1]
    return best_sequence

def thread_worker(parents, new_gen, board, color_of_player_turn, fitness_fn):
    """Handle thread
    """
    parent1, parent2 = random.sample(parents, 2)
    child = crossover(parent1[1], parent2[1])
    for i in range(SEQUENCE_LENGTH-1):
        child = mutate(child, board)
    new_gen.append((fitness_fn(child), child))

def genetic_algorithm_threads(board, color_of_player_turn):
    population = generate_existing_population(board, color_of_player_turn)
    fitness_fn = lambda sequence: evaluate_fitness(board, color_of_player_turn, sequence)
    # check_population_type(population)

    for generation in range(MAX_GENERATION):
        # print(f"GENERATION : {generation}")
        parents = select_parents(population, color_of_player_turn)
        # print(parents)
        new_gen = []

        threads = []
        for _ in range(POPULATION_SIZE):
            thread = threading.Thread(target=thread_worker, args=(parents, new_gen, board, color_of_player_turn, fitness_fn))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        population += new_gen
        population = select_best_individuals(population, color_of_player_turn)

    best_sequence = max(population, key=lambda x: x[0])[1]
    return best_sequence


def processus_worker(parents, new_gen, board, color_of_player_turn, fitness_fn):
    """Handle process
    """
    parent1, parent2 = random.sample(parents, 2)
    child = crossover(parent1[1], parent2[1])
    for i in range(SEQUENCE_LENGTH-1):
        child = mutate(child, board)
    new_gen.append((fitness_fn(child), child))

def genetic_algorithm_processus(board, color_of_player_turn):
    population = generate_existing_population(board, color_of_player_turn)
    fitness_fn = lambda sequence: evaluate_fitness(board, color_of_player_turn, sequence)
    # check_population_type(population)

    for generation in range(MAX_GENERATION):
        # print(f"GENERATION : {generation}")
        parents = select_parents(population, color_of_player_turn)
        # print(parents)
        new_gen = []

        processes = []
        for _ in range(POPULATION_SIZE):
            process = multiprocessing.Process(target=processus_worker, args=(parents, new_gen, board, color_of_player_turn, fitness_fn))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

        population += new_gen
        population = select_best_individuals(population, color_of_player_turn)

    best_sequence = max(population, key=lambda x: x[0])[1]
    return best_sequence[0]

