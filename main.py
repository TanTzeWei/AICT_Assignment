from stations import ADJ_LIST_CURRENT, COORDS, ADJ_LIST_FUTURE
from bfs import run_bfs
from dfs import run_dfs
from gbfs import run_gbfs
from astar import run_astar
from utils import compute_total_cost
import time

def algorithmMenu():
    print("--------------------------------------")
    print("Which search algorithm would you like?\n")
    print("1) BFS")
    print("2) DFS")
    print("3) GBFS")
    print("4) A*")
    print("0) Exit")
    print("--------------------------------------")
    pass

def modeMenu():
    print("--------------------------")
    print("Which mode would you like?\n")
    print("1) Current")
    print("2) Future")
    print("--------------------------")

def printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0):
    t1 = time.perf_counter()
    runtime_ms = (t1 - t0) * 1000
    print(f"Runtime: {runtime_ms:.3f} ms")
    print(f"Expanded nodes: {expanded}")
    compute_total_cost(path, parent, goal_Station, transfer_Penalty)


while True:
    algorithmMenu()
    algorithm_option = int(input("Option: "))
    if algorithm_option == 0:
        break
    if algorithm_option not in [0, 1, 2, 3, 4]:
        print("Invalid Option.")
        break
    modeMenu()
    mode_option = int(input("Option: "))
    if mode_option not in [1, 2]:
        print("Invalid Option.")
        break
    print("-------------------------------------------------")
    print("Stations are case sensitive.")
    current_Station = input("Name of current station: ")
    goal_Station = input("Destination: ")
    print("-------------------------------------------------")
    transfer_Penalty = 5
    t0 = time.perf_counter()
    if mode_option == 1:
        if current_Station not in ADJ_LIST_CURRENT or goal_Station not in ADJ_LIST_CURRENT:
            print("Invalid Station")
            break
        if algorithm_option == 1:
            path, parent, expanded = run_bfs(ADJ_LIST_CURRENT, current_Station, goal_Station)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
        elif algorithm_option == 2:
            path, parent, expanded = run_dfs(ADJ_LIST_CURRENT, current_Station, goal_Station)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
        elif algorithm_option == 3:
            path, parent, expanded = run_gbfs(ADJ_LIST_CURRENT, COORDS, current_Station, goal_Station)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
        elif algorithm_option == 4:
            path, parent, expanded = run_astar(ADJ_LIST_CURRENT, COORDS, current_Station, goal_Station, transfer_Penalty)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
    elif mode_option == 2:
        if current_Station not in ADJ_LIST_FUTURE or goal_Station not in ADJ_LIST_FUTURE:
            print("Invalid Station")
            break
        if algorithm_option == 1:
            path, parent, expanded = run_bfs(ADJ_LIST_FUTURE, current_Station, goal_Station)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
        elif algorithm_option == 2:
            path, parent, expanded = run_dfs(ADJ_LIST_FUTURE, current_Station, goal_Station)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
        elif algorithm_option == 3:
            path, parent, expanded = run_gbfs(ADJ_LIST_FUTURE, COORDS, current_Station, goal_Station)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)
        elif algorithm_option == 4:
            path, parent, expanded = run_astar(ADJ_LIST_FUTURE, COORDS, current_Station, goal_Station, transfer_Penalty)
            printResults(path, parent, goal_Station, transfer_Penalty, expanded, t0)