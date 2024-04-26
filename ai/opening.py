import random


white_openings = [
    ['e2e4', 'e7e5', 'g1f3', 'd7d6', 'f3g1', 'f8e7', 'g1h3', 'c8h3'],
    
    # # Défense sicilienne
    # ["e2e4", "c7c5"],

    # # Ouverture espagnole (Ruy Lopez) - Défense classique
    # ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],

    # # Ouverture espagnole (Ruy Lopez) - Défense Morphy
    # ["e2e4", "e7e5", "g1f3", "a7a6", "f1a4"],

    # # Gambit du roi
    # ["e2e4", "e7e5", "f2f4"],

    # # Ouverture anglaise
    # ["c2c4"],

    # # Partie écossaise
    # ["e2e4", "e7e5", "g1f3", "b8c6", "d2d4"],

    # # Partie italienne
    # ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],

    # # Attaque viennoise
    # ["e2e4", "e7e5", "b1c3"],

    # # Ouverture de l'école de Londres
    # ["d2d4", "e7e6", "g1f3", "g8f6", "c1d2"],

    # # Attaque Torre
    # ["d2d4", "f7f6", "c2c4", "e7e6", "g1f3", "g8f6", "c1g5"],

    # # Gambit de la Dame
    # ["d2d4", "d7d5", "c2c4"]
]

black_openings = [
    # Défense française
    ["e2e4", "e7e6", "d2d4", "d7d5"],

    # Défense Caro-Kann
    ["e2e4", "c7c6", "d2d4", "d7d5"],

    # Défense sicilienne
    ["c2c4"],

    # Défense scandinave
    ["e2e4", "d7d5"],

    # Ouverture des 4 cavaliers
    ["e2e4", "e7e5", "g1f3", "b8c6", "g2g3", "g8f6"],

    # Défense hollandaise
    ["d2d4", "f7f5"],

    # Ouverture anglaise
    ["c2c4"]
]







def random_between_a_and_min_bc(a, b, c):
    min_bc = min(b, c)
    return random.randint(a, min_bc -1)

def can_pick_a_move(turn, current_moves,color):
    if turn == 1:
        return True
    else:
        if(color == "white"):
            return next_moves_exists_in_openings(current_moves,white_openings)
        else: return next_moves_exists_in_openings(current_moves,black_openings)

def next_moves_exists_in_openings(moves, openings):
    for opening in openings:
        if len(moves) >= len(opening):
            continue
        i = 0
        while(i < len(moves)):
            if moves[i] != opening[i]:
                return False
            i += 1
    return True

def next_move(turn,current_moves,color):
    openings = white_openings
    next_mv = None
    if color == "black":
        openings = black_openings
    if turn == 1 and color == "white":
        opn = openings[random_between_a_and_min_bc(0,len(white_openings),len(black_openings))]
        return opn[0]
    for opening in openings:
        if len(current_moves) >= len(opening):
            continue
        i = 0
        while(i < len(current_moves)):
            if current_moves[i] != opening[i]:
                break
            i += 1
        if i == len(current_moves):
            next_mv = opening[i]
            break
    return next_mv