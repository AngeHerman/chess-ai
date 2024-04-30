from chess.board2 import *
from chess.utils import *
from chess.king import *
from ai.alpha_beta import *
from ai.alpha_beta_multi_thread import *
from ai.alpha_beta_multi_thread_section import *
from ai.alpha_beta_thread import *
from ai.alpha_beta_multithread_no_copy_bad_version import *
from ai.alpha_beta_multithread_no_copy import *
from ai.alpha_beta_multiprocess import *
from ai.alpha_beta_multi_process_section import *
import pickle
import time

def test_ia_spped():
    # test_threadpool_speed()
    # exit()
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
    # start_time = time.time()
    # m = alpha_beta_search_mt_section(plateau,BLANC)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("Temps d'exécution de alpha_beta_search multiThread section:", execution_time, "secondes")
    # print(m)
    # print(move_to_chess_notation(m))
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
    # futures = []
    # start_time = time.time()
    # with ThreadPoolExecutor(max_workers=6) as executor:
    #     for _ in range(0, 53):
    #         future = executor.submit(ab,plateau,BLANC,1)
    #         futures.append(future)

    #     for ft in futures:
    #         val = ft.result()
    #         # print(ft)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("Temps d'exécution de alpha_beta_search pool (6 max workers) avec max un thread:", execution_time, "secondes")
    # print(m)
    # print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    # futures = []
    # start_time = time.time()
    # m = alpha_beta_search_mt_manual(plateau,BLANC)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("Temps d'exécution de alpha_beta_search_mt_manual avec des thread join:", execution_time, "secondes")
    # print(m)
    # print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_multithread_no_copy_bad_version(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta no copy bad version : ", execution_time, "secondes")
    # Ca fait 6 secondes avec les copy board envoyé ou non
    print(m)
    print(move_to_chess_notation(m))
    exit()


def loop_from_1_to_1000(p,pp):
    p1 = copy.deepcopy(p)
    start_time = time.time()
    for i in range(1, 1001):
        pass
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de la boucle de 1 à 1000 : ", execution_time, "secondes")

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
    print("Temps d'exécution de la boucle de 1 à 1000 avec ThreadPoolExecutor (50 fois) : ", execution_time, "secondes")

def test_threadpool_speed():
    p = Board2()
    pp = Board2()
    loop_from_1_to_1000(p,pp)
    start_time = time.time()
    test_threadpool_execution()
    end_time = time.time()
    execution_time = end_time - start_time
    print("FINNNNNNNNNNNNN:", execution_time, "secondes")
    
def test_ia_speed2():
    # test_threadpool_speed()
    # exit()
    moves = ["e2e4","d7d5","d1h5","c7c5","f2f4","d8a5"]
    plateau = Board2()
    plateau.print_Board()
    for m in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move(m))
    plateau.print_Board()
    plateau.getAllMovesBasedOnTurn()
    # print(plateau.pMoves)
    print(len(plateau.pMoves))
    start_time = time.time()
    m = alpha_beta_search(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta_search : ", execution_time, "secondes")
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
    m = alpha_beta_multithread_no_copy(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta sans copy du plateau, juste avec les moves jusqu'a maintenant : ", execution_time, "secondes")
    # Ca fait 6 secondes avec les copy board envoyé ou non
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_multithread_no_copy_bad_version(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta sans copy du plateau, mauvaise version pour tester sans les objets : ", execution_time, "secondes")
    # Ca fait 6 secondes avec les copy board envoyé ou non
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_search_mp(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta multiprocess: ", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_search_mprocess_section(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta multiprocess avec section : ", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    exit()

def test_mps():
    print("Test mps")

    moves = ["e2e4","d7d5","d1h5","c7c5","f2f4","d8a5"]
    plateau = Board2()
    plateau.print_Board()
    for m in moves:
        plateau.getAllMovesBasedOnTurn()
        plateau.play_move(chess_notation_to_move(m))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    start_time = time.time()
    m = alpha_beta_search_mprocess_section(plateau,BLANC)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Temps d'exécution de alpha_beta multiprocess avec section : ", execution_time, "secondes")
    print(m)
    print(move_to_chess_notation(m))
    plateau.getAllMovesBasedOnTurn()
    print(plateau.pMoves)
    print(len(plateau.pMoves))
    # sections = divide_tree(plateau.pMoves,6)
    # for section in sections:
    #     print("SECTION")
    #     print(len(section))
    #     print(section)
    exit()