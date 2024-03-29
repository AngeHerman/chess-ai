from chess.board2 import *
import random
import math
import copy

class Node:
    def __init__(self, state,parent = None):
        self.state = state  # Le plateau
        self.visits = 1
        self.reward = 0
        self.children = {}
        self.parent = parent

def select(node):
    exploration_constant = math.sqrt(2)
    best_score = float('-inf')  
    selected_child = None
    for action, child_node in node.children.items():
        if child_node.visits == 1:
            exploitation_score = 2  # Si le nœud enfant n'a pas été visité, considérer l'exploitation comme 2 et ca permet de toujours selectionné les sommets pas encore visité
        else:
            exploitation_score = child_node.reward / child_node.visits  
        exploration_score = exploration_constant * math.sqrt(math.log(child_node.visits) / child_node.visits)  
        score = exploitation_score + exploration_score
        
        # print(f"Action: {action}, Exploitation Score: {exploitation_score}, Exploration Score: {exploration_score}, Total Score: {score}")
        
        if score > best_score:
            best_score = score
            selected_child = child_node
    return selected_child


def expand(node):
    # TODO
    # Ajouter booleen myturn au plateau et gameover ainsi que win
    try:
        node.state.getAllMovesBasedOnTurn()
        random.shuffle(node.state.pMoves)
    except IndexError as e:
        print("Petite Erreur")
        pass
    for move in node.state.pMoves:
        new_state = copy.deepcopy(node.state)
        new_state.play_move(move)
        node.children[move] = Node(new_state)

def simulate(node, my_color):
    # state = node.state
    # print("Avant deep copy")
    state = copy.deepcopy(node.state)
    # print("Apres deep copy")
    
    # print("*")
    while not state.isGameEnded:
        # print("Continue dans IA ",end=str(state.turn))
    # for _ in range(50):
        try:
            state.getAllMovesBasedOnTurn()
        except IndexError as e:
            print("Petite Erreur")
            print(e)
        pass
        if (len(state.pMoves) > 0):
            # print("Liste des mouvements possibles :", state.pMoves)
            random.shuffle(node.state.pMoves)
            random_move = random.choice(state.pMoves)
            state.play_move(random_move)
    return calculate_reward(state, my_color)

def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

def mcts(state, iterations, my_color):
    copie = copy.deepcopy(state)
    copie.print_Board()
    root = Node(copie)
    expand(root)
    for _ in range(iterations):
        selected_node = select(root)
        expand(selected_node)
        reward = simulate(selected_node, my_color)
        backpropagate(selected_node, reward)
    # Ici on prends sommets plus visité mais ce serait peut etre bien de prens le plus rewardé
    # print("*********   CHILD NODE   **********")
    # for action, child_node in root.children.items():
    #     print(str(action)+"  "+str(child_node.visits)+"  "+str(child_node.reward))
    best_action = max(root.children, key=lambda action: root.children[action].visits)
    return best_action

def mcts_rapide(state, iterations, my_color):
    copie = copy.deepcopy(state)
    copie.getAllMovesBasedOnTurn()
    random.shuffle(copie.pMoves)
    random_move = random.choice(copie.pMoves)
    return random_move


def calculate_reward(state, my_color):
    #on est censé renvoyer 1 quand on gagne, - 1 quand on perds et 0 en cas de match nulle,il 
    # pourrais y avoir une vrai fonction d'evaluation aussi par rapport au nombre de piece 
    # qu'il nous reste etc...
    if state.endGame() == my_color:
        # print("Gagné")
        return 1
    # print("Perdu")
    return 0


