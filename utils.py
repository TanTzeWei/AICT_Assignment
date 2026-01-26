# utils.py
import math
from typing import Dict, Tuple, Optional, List

Coords = Dict[str, Tuple[float, float]]

def haversine_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Great-circle distance in km between two (lat, lon) points."""
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    x = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))

def heuristic_minutes(coords: Coords, node: str, goal: str, km_per_min: float = 0.833) -> float:
    """
    Convert straight-line km into rough minutes for heuristic.
    km_per_min ~ 0.5 means 30 km/h (since 0.5 km/min = 30 km/h).
    """
    if node not in coords or goal not in coords:
        return 0.0
    km = haversine_km(coords[node], coords[goal])
    return km / km_per_min

def reconstruct_path(parent: Dict[str, Optional[str]], goal: str) -> List[str]:
    path = []
    cur: Optional[str] = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path

def compute_total_cost(parent, goal, transfer_penalty):
    total_cost = 0
    prev_line = None
    cur = goal

    while parent[cur] is not None:
        prev, cost, line = parent[cur]
        total_cost += cost

        if prev_line is not None and line != prev_line:
            total_cost += transfer_penalty

        prev_line = line
        cur = prev

    return total_cost
