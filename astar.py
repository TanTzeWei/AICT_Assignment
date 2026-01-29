# astar.py
def run_astar(adj, coords, start, goal, transfer_penalty, km_per_min=0.5):
    import heapq
    from utils import heuristic_minutes

    start_state = (start, None)
    g = {start_state: 0}
    parent_state = {start_state: None}

    pq = []
    heapq.heappush(pq, (heuristic_minutes(coords, start, goal, km_per_min), start, None))

    best_goal_state = None
    expanded = 0

    while pq:
        f, node, cur_line = heapq.heappop(pq)
        cur_state = (node, cur_line)

        if cur_state not in g:
            continue
        expanded += 1

        if node == goal:
            best_goal_state = cur_state
            break

        for nxt, edge_cost, next_line in adj[node]:
            new_cost = g[cur_state] + edge_cost

            if cur_line is not None and cur_line != next_line:
                new_cost += transfer_penalty

            nxt_state = (nxt, next_line)

            if nxt_state not in g or new_cost < g[nxt_state]:
                g[nxt_state] = new_cost
                parent_state[nxt_state] = cur_state

                h = heuristic_minutes(coords, nxt, goal, km_per_min)
                heapq.heappush(pq, (new_cost + h, nxt, next_line))

    if best_goal_state is None:
        return None, None, expanded

    state_path = []
    cur = best_goal_state
    while cur is not None:
        state_path.append(cur)
        cur = parent_state[cur]
    state_path.reverse()

    path = [state_path[0][0]]
    for st in state_path[1:]:
        path.append(st[0])

    parent_station = {start: None}

    for i in range(1, len(state_path)):
        prev_node, _prev_line = state_path[i - 1]
        cur_node, cur_arrival_line = state_path[i]

        found = False
        for nxt, edge_cost, line in adj[prev_node]:
            if nxt == cur_node and line == cur_arrival_line:
                parent_station[cur_node] = (prev_node, edge_cost, line)
                found = True
                break

        if not found:
            for nxt, edge_cost, line in adj[prev_node]:
                if nxt == cur_node:
                    parent_station[cur_node] = (prev_node, edge_cost, line)
                    found = True
                    break

        if not found:
            return None, None

    return path, parent_station, expanded
