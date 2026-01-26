# astar.py
def run_astar(adj, coords, start, goal, transfer_penalty, km_per_min=0.5):
    import heapq
    from utils import heuristic_minutes

    # g[(node, line)] = best cost reaching node when last traveled on 'line'
    start_state = (start, None)
    g = {start_state: 0}
    parent_state = {start_state: None}

    pq = []
    heapq.heappush(pq, (heuristic_minutes(coords, start, goal, km_per_min), start, None))

    best_goal_state = None

    while pq:
        f, node, cur_line = heapq.heappop(pq)
        cur_state = (node, cur_line)

        # If this popped state's f is stale, skip (optional safety)
        # (Not strictly required, but helps correctness with duplicates)
        if cur_state not in g:
            continue

        if node == goal:
            best_goal_state = cur_state
            break

        for nxt, edge_cost, next_line in adj[node]:
            new_cost = g[cur_state] + edge_cost

            # transfer penalty when changing line
            if cur_line is not None and cur_line != next_line:
                new_cost += transfer_penalty

            nxt_state = (nxt, next_line)

            if nxt_state not in g or new_cost < g[nxt_state]:
                g[nxt_state] = new_cost
                parent_state[nxt_state] = cur_state

                h = heuristic_minutes(coords, nxt, goal, km_per_min)
                heapq.heappush(pq, (new_cost + h, nxt, next_line))

    if best_goal_state is None:
        return None, None

    # 1) Reconstruct state path (node + line)
    state_path = []
    cur = best_goal_state
    while cur is not None:
        state_path.append(cur)  # (node, line_used_to_arrive_here)
        cur = parent_state[cur]
    state_path.reverse()

    # 2) Convert to station path
    path = [state_path[0][0]]
    for st in state_path[1:]:
        path.append(st[0])

    # 3) Build station-level parent dict compatible with compute_total_cost()
    # parent_station[child] = (parent, edge_cost, line)
    parent_station = {start: None}

    for i in range(1, len(state_path)):
        prev_node, _prev_line = state_path[i - 1]
        cur_node, cur_arrival_line = state_path[i]

        # find the matching edge prev_node -> cur_node using cur_arrival_line
        # (there should be exactly one in your data; if multiple, pick the matching line)
        found = False
        for nxt, edge_cost, line in adj[prev_node]:
            if nxt == cur_node and line == cur_arrival_line:
                parent_station[cur_node] = (prev_node, edge_cost, line)
                found = True
                break

        if not found:
            # fallback: match by node only (if your data has ambiguous lines)
            for nxt, edge_cost, line in adj[prev_node]:
                if nxt == cur_node:
                    parent_station[cur_node] = (prev_node, edge_cost, line)
                    found = True
                    break

        if not found:
            # If this happens, your adj list doesn't contain that edge as written
            return None, None

    return path, parent_station
