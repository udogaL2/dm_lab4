import random
import heapq


def prepare_graf(graf: str):
    graf = graf.replace('(', '')
    graf = graf.replace(')', '')
    graf = graf.replace(' ', '')
    graf = graf.replace('\n', '')
    graf = graf.replace('\t', '')
    return graf


def bellman_ford(graph, start):
    # Инициализация расстояний до всех вершин как бесконечности, кроме стартовой
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    inr = 0

    # Проходим по всем ребрам |V|-1 раз, где |V| - количество вершин в графе
    for _ in range(len(graph) - 1):
        for vertex in graph:
            for neighbour in graph[vertex]:
                inr += 1
                # Проверяем, улучшит ли текущее ребро путь до смежной вершины
                if distances[vertex] + graph[vertex][neighbour] < distances[neighbour]:
                    distances[neighbour] = distances[vertex] + graph[vertex][neighbour]

    for vertex in graph:
        for neighbour in graph[vertex]:
            inr += 1
            if distances[vertex] + graph[vertex][neighbour] < distances[neighbour]:
                raise ValueError("Граф содержит цикл отрицательного веса")

    return distances, inr


def dijkstra(graph, start):
    # Инициализация расстояний до всех вершин как бесконечность
    dist = {v: float('inf') for v in graph}
    # Расстояние до стартовой вершины - 0
    dist[start] = 0
    # Очередь с приоритетом для выбора вершины с наименьшим расстоянием
    queue = [(0, start)]

    itr = 0

    while queue:
        # Извлекаем вершину с наименьшим расстоянием из очереди
        (cost, v) = heapq.heappop(queue)
        # Если расстояние до текущей вершины уже было посчитано корректно, пропускаем ее
        if cost > dist[v]:
            itr += 1
            continue
        # Обновляем расстояния до соседних вершин, если новое расстояние короче
        for u in graph[v]:
            alt = dist[v] + graph[v][u]
            if alt < dist[u]:
                dist[u] = alt
                heapq.heappush(queue, (alt, u))
            itr += 1

    return dist, itr


def importK7():
    n = 0
    while n < 1:
        n = int(input("Введите количество вершин: "))

    text = input('Введите стартовый подграф К7: ')

    # Создание пустого графа
    graph = {i: {} for i in range(n)}
    start_v = []

    for i in prepare_graf(text).split(';')[:-1]:
        x, y, weight = map(lambda n: int(n), i.split(','))
        graph[x][y] = weight
        start_v.append(x)

    return graph, start_v, n


def main():
    graph, start_v, n = importK7()

    # Добавление ребер для связывания графа
    visited = start_v
    current_vertex = 8
    visited.append(current_vertex)
    while len(visited) < 5 * n:
        next_vertex = random.randrange(n)
        if next_vertex != current_vertex and next_vertex not in graph[current_vertex]:
            weight = random.randint(1, 10)
            graph[current_vertex][next_vertex] = weight
            current_vertex = next_vertex
            visited.append(current_vertex)

    secect = int(input('Введите вершину, из которой будут найдены кратчайшие пути: '))

    while secect >= n:
        secect = int(input('Ошибка, введите вершину, из которой будут найдены кратчайшие пути: '))

    with open('output.txt', 'w', encoding='utf-8') as f:
        f.close()

    for i in range(n):
        with open('output.txt', 'a', encoding='utf-8') as f:
            string_to_write1 = f"Вершина {i} -> "
            for j in graph[i]:
                string_to_write1 += f"{j} ({graph[i][j]}), "
            string_to_write1 += '\n'
            f.write(string_to_write1)
            f.close()

    with open('output.txt', 'a', encoding='utf-8') as f:
        string_to_write1 = '\n'
        string_to_write1 += f'Количество ребер: {str(sum([len(graph[i]) for i in graph]))}\n'

        string_to_write1 += 'Алгоритм Дейкстры:\n'
        f.write(string_to_write1)
        string_to_write2 = 'Кратчайшие расстояния:\n'
        f.write(string_to_write2)

        f.close()

    a_d, itr = dijkstra(graph, secect)

    for i in range(n):
        with open('output.txt', 'a', encoding='utf-8') as f:
            string_to_write2 = f"{secect} => {i} ({a_d[i]})\n"
            f.write(string_to_write2)
            f.close()

    with open('output.txt', 'a', encoding='utf-8') as f:
        string_to_write2 = f'Количество итераций: {itr}\n'
        f.write(string_to_write2)
        f.close()

    print('Алгоритм Дейкстры пройден')

    a_d, itr = bellman_ford(graph, secect)
    with open('output.txt', 'a', encoding='utf-8') as f:
        string_to_write3 = 'Алгоритм Беллмана Форда \nКратчайшие расстояния:\n'
        f.write(string_to_write3)
        f.close()

    for i in range(n):
        with open('output.txt', 'a', encoding='utf-8') as f:
            string_to_write3 = f"{secect} => {i} ({a_d[i]})\n"
            f.write(string_to_write3)
            f.close()
    with open('output.txt', 'a', encoding='utf-8') as f:
        string_to_write3 = f'Количество итераций: {2 * itr}\n'
        f.write(string_to_write3)
        f.close()
    print('Алгоритм Беллмана Форда пройден')


if __name__ == '__main__':
    main()
