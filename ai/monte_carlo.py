from chess.board import *
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
    exploration_constant = 1.0  # Costante d'explration just pour definir a quel point explorationest important
    best_score = float('-inf')  # Init du meilleur score à moins infin
    selected_child = None
    for action, child_node in node.children.items():
        exploitation_score = child_node.reward / (child_node.visits)  # Terme d'exploitation. le 1e-5 cest pour eviter 0/0
        exploration_score = exploration_constant * math.sqrt( (math.log(child_node.visits)) / (child_node.visits))  # Terme d'exploration
        score = exploitation_score + exploration_score  # Score total UCB1
        if score > best_score:
            best_score = score
            selected_child = child_node
    return selected_child

def expand(node):
    # TODO
    # Ajouter booleen myturn au plateau et gameover ainsi que win
    node.state.getAllMovesBasedOnTurn()
    for move in node.state.pMoves:
        new_state = copy.deepcopy(node.state)
        new_state.play_move(move)
        node.children[move] = Node(new_state)

def simulate(node):
    state = node.state
    print("*")
    # while not state.isGameEnded:
    for _ in range(10):
        #TODO
        state.getAllMovesBasedOnTurn()
        if (len(state.pMoves) > 0):
            # print("Liste des mouvements possibles :", state.pMoves)
            random_move = random.choice(state.pMoves)
            state.play_move(random_move)
    return calculate_reward(state)

def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

def mcts(state, iterations):
    root = Node(state)
    expand(root)
    for _ in range(iterations):
        selected_node = select(root)
        expand(selected_node)
        reward = simulate(selected_node)
        backpropagate(selected_node, reward)
    # Une fois que les itérations sont terminées, choisir la meilleure action
    best_action = max(root.children, key=lambda action: root.children[action].visits)
    return best_action


def calculate_reward(state):
    #on est censé renvoyer 1 quand on gagne, - 1 quand on perds et 0 en cas de match nulle,il 
    # pourrais y avoir une vrai fonction d'evaluation aussi par rapport au nombre de piece 
    # qu'il nous reste etc...
    return 1


