from collections import deque


# Класс для представления graphического объекта
class Graph:

    # 1ТП4Т Конструктор
    def __init__(self, edges=None, n=0):
        # Общее количество узлов в Graph
        self.n = n

        # Список списков для представления списка смежности
        self.adjList = [[] for _ in range(n)]

        # добавляет ребра в неориентированный graph
        for (src, dest) in edges:
            # добавляет ребро от источника к месту назначения
            self.adjList[src].append(dest)

            # добавляет ребро от пункта назначения к источнику
            self.adjList[dest].append(src)


# Выполнить BFS на Graph, начиная с вершины `v`
def is_bipartite(graph):
    # запускается с любого узла, так как graph связный и ненаправленный
    v = 0

    # для отслеживания обнаружена вершина или нет
    discovered = [False] * graph.n

    # хранит уровень каждой вершины в BFS
    level = [None] * graph.n

    # пометить исходную вершину как обнаруженную и установить ее уровень на 0
    discovered[v] = True
    level[v] = 0

    # создает queue для выполнения BFS и ставит в queue исходную вершину
    q = deque()
    q.append(v)

    # Цикл # до тех пор, пока queue не станет пустой
    while q:

        # удалить передний узел из очереди и распечатать его
        v = q.popleft()

        # делаем для каждого ребра (v, u)
        for u in graph.adjList[v]:
            # , если вершина `u` исследуется впервые
            if not discovered[u]:
                # пометить как обнаруженный
                discovered[u] = True

                # устанавливает уровень на один больше, чем уровень родительского узла
                level[u] = level[v] + 1

                # Вершина постановки в queue
                q.append(u)

            elif level[v] == level[u]:
                return False

    return True


def remove_edges_to_make_bipartite(edges, n):
    graph = Graph(edges, n)
    if is_bipartite(graph):
        return []

    for edge in edges:
        reduced_edges = []
        for i in edges:
            if i != edge:
                reduced_edges.append(i)
        graph = Graph(reduced_edges, n)

        if is_bipartite(graph):
            return edge

    return []


from collections import defaultdict


def find_maximum_matching_(edges):
    graph = defaultdict(list)
    capacity = {}

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        capacity[(u, v)] = 1

    def bfs(source, target, parent):
        visited = set()
        queue = [source]
        visited.add(source)
        parent[source] = None

        while queue:
            u = queue.pop(0)
            for v in graph[u]:
                if v not in visited and capacity[(u, v)] > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == target:
                        return True

        return False

    def ford_fulkerson(source, target):
        parent = {}
        max_matching = 0

        while bfs(source, target, parent):
            path_flow = float("inf")
            s = target

            while s != source:
                path_flow = min(path_flow, capacity[(parent[s], s)])
                s = parent[s]

            max_matching += path_flow

            v = target
            while v != source:
                u = parent[v]
                capacity[(u, v)] -= path_flow
                capacity[(v, u)] += path_flow
                v = parent[v]

        return max_matching

    source = -1
    target = -2

    for u, v in edges:
        source = min(source, u, v)
        target = max(target, u, v)

    return ford_fulkerson(source, target)


def find_maximum_matching(edges):
    def dfs(vertex, visited, match):
        if visited[vertex]:
            return False

        visited[vertex] = True

        for neighbor in graph[vertex]:
            if match[neighbor] is None or dfs(match[neighbor], visited, match):
                match[vertex] = neighbor
                match[neighbor] = vertex
                return True

        return False

    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    match = {v: None for v in graph}
    maximum_matching = 0

    for vertex in graph:
        if match[vertex] is None:
            visited = {v: False for v in graph}
            if dfs(vertex, visited, match):
                maximum_matching += 1

    matching_edges = []
    for u, v in match.items():
        if v is not None and (v, u) not in matching_edges:
            matching_edges.append((u, v))

    return maximum_matching, matching_edges


if __name__ == '__main__':

    # Список ребер Graph.
    # edges = [(1, 0), (1, 2), (1, 7), (2, 3), (3, 5), (4, 6), (4, 8), (7, 8), (1, 3)]
    edges = [(11, 14), (8, 3), (11, 3), (14, 15), (10, 1), (3, 10), (15, 1), (6, 10), (13, 4), (15, 9), (7, 10), (9, 8),
             (2, 5), (12, 11), (12, 10), (2, 8),
             (8, 7), (1, 5), (4, 1), (4, 7), (2, 11), (2, 4), (11, 9), (15, 13), (10, 13), (3, 4), (12, 8), (5, 14),
             (10, 2), (14, 10)]
    # общее количество узлов в Graph (от 0 до 8)
    n = max([i for i, j in edges] + [j for i, j in edges]) + 1

    # строит graph по заданным ребрам
    graph = Graph(edges, n)

    if not (edge_remove := remove_edges_to_make_bipartite(edges, n)):
        print('Граф является двудольным')

        maximum_matching, matching_edges = find_maximum_matching(edges)

        print("Наибольшее паросочетание по алгоритму Куна:", maximum_matching)
        print("Наибольшее паросочетание по алгоритму Форда-Фалкерсона:", maximum_matching)
        print("Паросочетание:", matching_edges)
    else:
        print('Граф не является двудольным')
        if edge_remove:
            print("Для получения двудольного графа нужно удалить", edge_remove, 'ребро')
        else:
            print('Не удалось найти ребро, удалив которое, получится двудольный граф')
