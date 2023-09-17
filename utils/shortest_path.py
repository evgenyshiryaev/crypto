# http://e-maxx.ru/algo/dijkstra
# http://e-maxx.ru/algo/dijkstra_sparse

from sortedcontainers import SortedSet


# O(E * log(V)))
# graph - map(vertex - [vertex, weight])
def dijkstra2(graph, start, target=None):
    V = len(graph)

    dist = [float('inf')] * V
    dist[start] = 0

    nearest = SortedSet(key=lambda v: (dist[v], v))
    nearest.add(start)

    while nearest:
        from_v = nearest.pop(0)
        if from_v == target:
            break
        for to_v, l in graph[from_v]:
            if dist[from_v] + l < dist[to_v]:
                nearest.discard(to_v)
                dist[to_v] = dist[from_v] + l
                nearest.add(to_v)

    return dist


if __name__ == '__main__':
    _graph = [[[1, 1], [2, 10], [4, 20]], [[2, 5], [3, 2]], [[4, 6]], [[4, 15]], [[2, 6], [3, 15]]]
    assert [0, 1, 6, 3, 12] == dijkstra2(_graph, 0)

    _graph = [[[1, 1], [2, 10], [4, 20]], [[2, 5], [3, 2]], [[4, 6]], [[4, 15]], [[2, 6], [3, 15]]]
    assert [0, 1, 10, float('inf'), 20] == dijkstra2(_graph, 0, 1)
