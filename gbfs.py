# gbfs.py
def run_gbfs(adj, coords, start, goal, km_per_min=0.833):
    import heapq
    from utils import heuristic_minutes

    pq = []
    heapq.heappush(pq, (heuristic_minutes(coords, start, goal, km_per_min), start))

    parent = {start: None}   # start has no parent
    visited = set()
    expanded = 0

    while pq:
        _, node = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)
        expanded += 1

        if node == goal:
            break

        for nxt, cost, line in adj[node]:
            if nxt not in parent:  # first time discovered
                parent[nxt] = (node, cost, line)
                heapq.heappush(
                    pq,
                    (heuristic_minutes(coords, nxt, goal, km_per_min), nxt)
                )

    if goal not in parent:
        return None, None, expanded

    # reconstruct path (compatible with parent storing tuples)
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        entry = parent[cur]
        if entry is None:
            cur = None
        else:
            cur, _, _ = entry
    path.reverse()

    return path, parent, expanded
