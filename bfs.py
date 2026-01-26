# bfs.py
def run_bfs(adj, start, goal):
    from collections import deque
    q = deque([start])
    parent = {start: None}

    while q:
        node = q.popleft()
        if node == goal:
            break

        for nxt, cost, line in adj[node]:
            if nxt not in parent:
                parent[nxt] = (node, cost, line)
                q.append(nxt)

    if goal not in parent:
        return None, None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        prev = parent[cur]
        if prev is None:
            cur = None
        else:
            cur, _, _ = prev

    return path[::-1], parent
