import copy
import random
from pprint import pprint
from queue import Queue


def bfs(graph, start, end, parent):
    visited = {vertex: False for vertex in graph}
    queue = Queue()
    queue.put(start)
    visited[start] = True

    while not queue.empty():
        u = queue.get()

        for v, capacity in graph[u].items():
            if not visited[v] and capacity > 0:
                queue.put(v)
                visited[v] = True
                parent[v] = u
    return visited[end]


def ford_fulkerson(graph, source, sink):
    parent = {vertex: None for vertex in graph}
    max_flow = 0

    while bfs(graph, source, sink, parent):
        path_flow = float("Inf")
        s = sink

        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow

        v = sink
        while v != source:
            u = parent[v]
            if v in graph[u]:
                graph[u][v] -= path_flow
            else:
                graph[u][v] = path_flow

            if u in graph[v]:
                graph[v][u] += path_flow
            else:
                graph[v][u] = path_flow
            v = parent[v]

    return max_flow


graph = {
    'S': {'p': 7, 'd': 5, 'a': 3},
    'p': {'k': 2, 'b': 3},
    'd': {'k': 2, 'c': 6},
    'a': {'d': 2, 'b': 6, 'k': 1},
    'c': {'T': 4, 'b': 1},
    'b': {'T': 5},
    'k': {'T': 6},
    'T': {}
}

source = 'S'
sink = 'T'

for i in graph:
    print(f'Максимальный поток из вершины {i} в {sink}', end=': ')
    if i != sink:
        graph_copy = copy.deepcopy(graph)
        max_flow = ford_fulkerson(graph_copy, i, sink)
        print(max_flow)
    else:
        print('Не существует')



graph = {
    'S': {'p': random.randint(100, 1000), 'd': random.randint(100, 1000), 'a': random.randint(100, 1000)},
    'p': {'k': random.randint(100, 1000), 'b': random.randint(100, 1000)},
    'd': {'k': random.randint(100, 1000), 'c': random.randint(100, 1000)},
    'a': {'d': random.randint(100, 1000), 'b': random.randint(100, 1000), 'k': random.randint(100, 1000)},
    'c': {'T': random.randint(100, 1000), 'b': random.randint(100, 1000)},
    'b': {'T': random.randint(100, 1000)},
    'k': {'T': random.randint(100, 1000)},
    'T': {}
}

print('Граф со случайными значениями:')
pprint(graph)
for i in graph:
    print(f'Максимальный поток из вершины {i} в {sink}', end=': ')
    if i != sink:
        graph_copy = copy.deepcopy(graph)
        max_flow = ford_fulkerson(graph_copy, i, sink)
        print(max_flow)
    else:
        print('Не существует')

