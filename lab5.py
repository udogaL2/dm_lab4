def prepare_graf(graf: str):
    graf = graf.replace('(', '')
    graf = graf.replace(')', '')
    graf = graf.replace(' ', '')
    graf = graf.replace('\n', '')
    graf = graf.replace('\t', '')
    return graf


def makeMatrix(graf: str):
    count = max([int(j) for i in graf.split(';')[:-1] for j in i.split(',')[:2]]) + 1

    o_graf = [[0 for _ in range(count)] for _ in range(count)]
    no_graf = [[0 for _ in range(count)] for _ in range(count)]

    for i in graf.split(';')[:-1]:
        x, y, weight = map(lambda n: int(n), i.split(','))
        o_graf[x][y] = weight

        no_graf[x][y] = weight if no_graf[x][y] == 0 else no_graf[x][y]

    for i in range(count):
        for j in range(count):
            if no_graf[j][i] == 0:
                no_graf[j][i] = no_graf[i][j]

    return o_graf, no_graf


def make_adjacency_matrix(graf):
    adjacency_matrix = [[0 for _ in range(len(graf))] for _ in range(len(graf))]
    for i in range(len(graf)):
        for j in range(len(graf)):
            if graf[i][j] != 0:
                adjacency_matrix[i][j] = 1

    return adjacency_matrix


def adjacency_to_incidence(adj_matrix, flag):
    num_nodes = len(adj_matrix)
    num_edges = sum([sum(i) for i in adj_matrix])  # количество ребер
    inc_matrix = [[0 for _ in range(num_edges)] for _ in range(num_nodes)]

    edge_count = 0  # Счетчик для отслеживания номера текущего ребра
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i][j]:  # Если есть ребро между i и j
                inc_matrix[i][edge_count] = 1
                inc_matrix[j][edge_count] = -1 if flag else 1
                edge_count += 1

    return inc_matrix


def dijkstra(graph, start):
    distances = [float('inf')] * len(graph)
    visited = set()

    distances[start] = 0

    for _ in range(len(graph)):
        # Находим вершину с минимальным расстоянием
        min_distance = float('inf')
        current_vertex = -1
        for vertex in range(len(graph)):
            if vertex not in visited and distances[vertex] < min_distance:
                min_distance = distances[vertex]
                current_vertex = vertex

        # Добавляем найденную вершину в множество посещенных
        if current_vertex != -1:
            visited.add(current_vertex)

            # Обновляем расстояния до всех вершин, смежных с текущей
            for neighbor, weight in enumerate(graph[current_vertex]):
                if weight > 0 and neighbor not in visited:
                    new_distance = distances[current_vertex] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance

    return distances


def main():
    print('Введите граф в виде (x,y,weight);, где x и y номера вершин начиная с 0, и т.д. или имя файла в формате txt')
    raw_input = input()

    if '.txt' in raw_input:
        with open(raw_input, 'r') as f_in:
            raw_graf = f_in.read().strip()
    else:
        raw_graf = raw_input.strip()

    o_graf, no_graf = makeMatrix(prepare_graf(raw_graf))

    adjacency_o_matrix = make_adjacency_matrix(o_graf)
    adjacency_no_matrix = make_adjacency_matrix(no_graf)

    incidence_o_matrix = adjacency_to_incidence(adjacency_o_matrix, True)
    incidence_no_matrix = adjacency_to_incidence(adjacency_o_matrix, False)

    print('Введен граф (ориентированный):')
    print(*o_graf, sep='\n')
    print('Перевод в неориентированный:')
    print(*no_graf, sep='\n')
    print('Матрица смежности для ориентированного графа:')
    print(*adjacency_o_matrix, sep='\n')
    print('Матрица смежности для неориентированного графа:')
    print(*adjacency_no_matrix, sep='\n')
    print('Матрица инцидентности для ориентированного графа:')
    print(*incidence_o_matrix, sep='\n')
    print('Матрица инцидентности для неориентированного графа:')
    print(*incidence_no_matrix, sep='\n')

    for i in range(len(no_graf)):
        print('Кратчайшие пути от каждой вершины №', i)
        print(dijkstra(no_graf, i))


if __name__ == '__main__':
    main()
