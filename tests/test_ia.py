from chess.board2 import *
from chess.utils import *
from chess.king import *
from ai.alpha_beta import *
from ai.alpha_beta_multi_thread import *
from ai.alpha_beta_multi_thread_section import *
from ai.alpha_beta_thread import *
import pickle
import time

def test_ia_spped():
    test_threadpool_speed()
    exit()
    # # https://lichess.org/SUslmNjf#43 tester a 22
    plateau = Board2()
    plateau.grille = [
            [Queen(BLANC), Knight(BLANC), Bishop(BLANC),  King(BLANC),None , Bishop(BLANC),Knight(BLANC) , Rook(BLANC)],
            [None] * 8,
            [None,None,None,None,None,None,Queen(NOIR),None],
            [None] * 8,
            [None,None,None,Bishop(BLANC),None,None,None,None],
            [None] * 8,
            [None] * 8,
            [None,Rook(NOIR), Bishop(NOIR),  King(NOIR), None, Bishop(NOIR), Knight(NOIR), Rook(NOIR)]
        ]
    plateau.initializeCoordinates()
    plateau.print_Board()
    plateau.getAllMovesBasedOnTurn()
    print(plateau.pMoves)
    print(len(plateau.pMoves))
    start_time = time.time()
    m = alpha_beta_search(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search :", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_search_mt(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search multiThread :", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_search_mt_section(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search multiThread section:", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    futures = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(alpha_beta_search,plateau,BLANC)
        m = future.result()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search normal avec un thread:", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    futures = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=6) as executor:
        for _ in range(0, 53):
            future = executor.submit(ab,plateau,BLANC,1)
            futures.append(future)

        for ft in futures:
            val = ft.result()
            # print(ft)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search pool (6 max workers) avec max un thread:", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    futures = []
    start_time = time.time()
    m = alpha_beta_search_mt_manual(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search_mt_manual avec des thread join:", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    loop_from_1_to_1000()
    test_threadpool_execution()
    exit()


def loop_from_1_to_1000(p,pp):
    p1 = copy.deepcopy(p)
    start_time = time.time()
    for i in range(1, 1001):
        pass  # Do nothing
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de la boucle de 1 à 1000 :", execution_time, "secondes")

def loop_from_1_to_1000_wrapper(p,pp):
    loop_from_1_to_1000(p,pp)
    
def test_threadpool_execution():
    start_time = time.time()
    p = Board2()
    pp = Board2()
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        p1 = copy.copy(p)
        p2 = copy.deepcopy(pp)
        futures = [executor.submit(loop_from_1_to_1000_wrapper,p1,p2) for _ in range(50)]
        for future in futures:
            future.result()  # Wait for each task to complete
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de la boucle de 1 à 1000 avec ThreadPoolExecutor (50 fois) :", execution_time, "secondes")

def test_threadpool_speed():
    p = Board2()
    pp = Board2()
    loop_from_1_to_1000(p,pp)
    start_time = time.time()
    test_threadpool_execution()
    end_time = time.time()
    execution_time = end_time - start_time
    print("FINNNNNNNNNNNNN:", execution_time, "secondes")