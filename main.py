from stations import ADJ_LIST_CURRENT, COORDS, ADJ_LIST_FUTURE
from bfs import run_bfs
from dfs import run_dfs
from gbfs import run_gbfs
from astar import run_astar
from utils import compute_total_cost

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


while True:
    algorithmMenu()
    algorithm_option = int(input("Option: "))
    if algorithm_option == 0:
        break
    if algorithm_option not in [0, 1, 2, 3, 4]:
        print("Invalid Option.")
        break
    print("-------------------------------------------------")
    print("Stations are case sensitive.")
    current_Station = input("Name of current station: ")
    goal_Station = input("Destination: ")
    print("-------------------------------------------------")
    transfer_Penalty = 5
    modeMenu()
    mode_option = int(input("Option: "))
    if mode_option == 1:
        if algorithm_option == 1:
            path, parent = run_bfs(ADJ_LIST_CURRENT, current_Station, goal_Station)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
        elif algorithm_option == 2:
            path, parent = run_dfs(ADJ_LIST_CURRENT, current_Station, goal_Station)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
        elif algorithm_option == 3:
            path, parent = run_gbfs(ADJ_LIST_CURRENT, COORDS, current_Station, goal_Station)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
        elif algorithm_option == 4:
            path, parent = run_astar(ADJ_LIST_CURRENT, COORDS, current_Station, goal_Station, transfer_Penalty)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
    elif mode_option == 2:
        if algorithm_option == 1:
            path, parent = run_bfs(ADJ_LIST_FUTURE, current_Station, goal_Station)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
        elif algorithm_option == 2:
            path, parent = run_dfs(ADJ_LIST_FUTURE, current_Station, goal_Station)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
        elif algorithm_option == 3:
            path, parent = run_gbfs(ADJ_LIST_FUTURE, COORDS, current_Station, goal_Station)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
        elif algorithm_option == 4:
            path, parent = run_astar(ADJ_LIST_FUTURE, COORDS, current_Station, goal_Station, transfer_Penalty)
            if path is None:
                print("No path found")
            else:
                cost = compute_total_cost(parent, goal_Station, transfer_Penalty)
                print("Path:", " -> ".join(path))
                print("Total cost (incl transfers):", cost)
    else:
        print("Invalid Option")
        pass
