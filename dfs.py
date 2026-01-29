# dfs.py

def run_dfs(adj, start, goal):
    stack = [start]
    parent = {start: None}
    expanded = 0

    while stack:
        node = stack.pop()
        expanded += 1
        if node == goal:
            break

        for nxt, cost, line in adj[node]:
            if nxt not in parent:
                parent[nxt] = (node, cost, line)
                stack.append(nxt)

    if goal not in parent:
        return None, None, expanded

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        prev = parent[cur]
        if prev is None:
            cur = None
        else:
            cur, _, _ = prev

    return path[::-1], parent, expanded
