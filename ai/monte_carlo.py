from chess.board2 import *
from ai.more import *

import random
import math
import copy

# The max depth to checki if a move where we sacrificed a piece paid out etc ...
MAX_DEPTH_TO_CHECK_BAD_MOVE = 4
INACCEPTABLE_SCORE_DIFFERENCE = 5
MAX_SIMULATE_MOVE_FOR_DRAW = 200

class Node:
    def __init__(self, state,parent = None):
        self.state = state  # Le plateau
        self.visits = 1
        self.reward = 0
        self.children = {}
        self.parent = parent
        self.depth = 0
        self.state_score = None

def select(node):
    exploration_constant = math.sqrt(2)
    best_score = float('-inf')  
    selected_child = None
    for action, child_node in node.children.items():
        if child_node.visits == 1:
            exploitation_score = 2  # Si le nœud enfant n'a pas été visité, considérer l'exploitation comme 2 et ca permet de toujours selectionné les sommets pas encore visité
        else:
            exploitation_score = child_node.reward / child_node.visits  
        exploration_score = exploration_constant * math.sqrt(math.log(node.visits) / child_node.visits)  
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
        new_node = Node(new_state,node)
        new_node.depth = node.depth + 1
        node.children[move] = new_node

def simulate(node, my_color):
    # state = node.state
    # print("Avant deep copy")
    state = copy.deepcopy(node.state)
    # print("Apres deep copy")
    
    # print("*")
    score = 0
    i = 0
    while not state.isGameEnded:
        if i == MAX_DEPTH_TO_CHECK_BAD_MOVE :
            # print("Avant score ")
            score = board_score(state.grille)
            # print("Après score "+str(score))
        # print("Continue dans IA ",end=str(state.turn))
    # for _ in range(50):
        if i == MAX_SIMULATE_MOVE_FOR_DRAW:
            return 0,score
        try:
            state.getAllMovesBasedOnTurn()
        except IndexError as e:
            print("Petite Erreur")
            print(e)
        pass
        if (len(state.pMoves) > 0):
            # print("Liste des mouvements possibles :", state.pMoves)
            random.shuffle(state.pMoves)
            random_move = random.choice(state.pMoves)
            state.play_move(random_move)
            i +=1
    return calculate_reward(state, my_color),score

def calculate_reward_with_future_score(old_reward,future_score,actual_score,my_color):
    difference = future_score - actual_score
    new_reward = old_reward
    if my_color == BLANC:
        # The white want posittive score
        # if difference <= -INACCEPTABLE_SCORE_DIFFERENCE:
        #     new_reward = max(old_reward + difference,0)
        
        # if difference > INACCEPTABLE_SCORE_DIFFERENCE:
        #     new_reward += 1
        if difference <= -INACCEPTABLE_SCORE_DIFFERENCE:
            new_reward -= 1
    else:
        # The black want a negative score
        # if difference >= INACCEPTABLE_SCORE_DIFFERENCE:
        #     new_reward = max(old_reward - difference,0)
        # if difference < INACCEPTABLE_SCORE_DIFFERENCE:
        #     new_reward += 1
        if difference >= INACCEPTABLE_SCORE_DIFFERENCE:
            new_reward -= 1
    if new_reward < 0:
        new_reward = 0
    
    return new_reward
    
def backpropagate(node, reward,future_score,my_color):
    while node is not None:
        node.visits += 1
        node.reward += reward
        if node.depth == 1:
            node.reward = calculate_reward_with_future_score(node.reward,future_score,node.parent.state_score,my_color)
        node = node.parent

def mcts(state, iterations, my_color):
    copie = copy.deepcopy(state)
    # copie.print_Board()
    root = Node(copie)
    expand(root)
    root.state_score = board_score(root.state.grille)
    i = 1
    for _ in range(iterations):
        print("Iteration "+str(i))
        i+= 1
        selected_node = select(root)
        if len(selected_node.children) == 0:
            expand(selected_node)
        reward,future_score = simulate(selected_node, my_color)
        backpropagate(selected_node, reward,future_score,my_color)
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

def print_tree(node, indent=0):
    print(' ' * indent + f"{node.visits}/{node.reward}")
    for child in node.children.values():
        print_tree(child,indent + 4)


