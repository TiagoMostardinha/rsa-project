import heapq
from typing import List, Dict, Tuple
import time


def mapToGraph(map):
    graph = []

    for i in range(len(map)):
        for j in range(len(map[i])):
            if j != len(map[i])-1 and map[i][j+1] != 'x' and map[i][j] != 'x':
                graph.append([(i, j), (i, j+1), 1])
            if i != len(map)-1 and map[i+1][j] != 'x' and map[i][j] != 'x':
                graph.append([(i, j), (i+1, j), 1])
            if i != 0 and map[i-1][j] != 'x' and map[i][j] != 'x':
                graph.append([(i, j), (i-1, j), 1])
            if j != 0 and map[i][j-1] != 'x' and map[i][j] != 'x':
                graph.append([(i, j), (i, j-1), 1])

    return graph


def shortestPath(n: int, edges: List[List[Tuple[int, int]]], src: Tuple[int, int],target: Tuple[int,int]) -> Dict[int, Tuple[int, int]]:
    def reconstructPath(predecessor, target):
        path = []
        while target is not None:
            path.append(target)
            target = predecessor[target]
        return path[::-1]

    adj = {}

    for v in edges:
        if v[0] not in adj:
            adj[v[0]] = []
        if v[1] not in adj:
            adj[v[1]] = []

    for s, d, w in edges:
        adj[s].append([d, w])

    shortest = {}
    predecessor = {src: None}
    minHeap = [(0, src)]

    while minHeap:
        w1, n1 = heapq.heappop(minHeap)
        if n1 in shortest:
            continue
        shortest[n1] = w1

        for n2, w2 in adj[n1]:
            if n2 not in shortest:
                heapq.heappush(minHeap, [w1+w2, n2])
                predecessor[n2] = n1

    for i in range(n):
        if i not in shortest:
            shortest[i] = -1
    
    if target not in shortest:
        return []
    return reconstructPath(predecessor, target)
