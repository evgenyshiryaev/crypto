# http://e-maxx.ru/algo/mst_prim

# graph - adjacency matrix
def prim1(graph):
    V = len(graph)
    if V == 0:
        return 0

    # min cost to connect i-th vertex with already constructed tree
    # get 0-th vertex first
    mins = [float('inf')] * V
    mins[0] = 0

    result = 0

    for i in range(V):
        minJ = -1
        m = float('inf')
        for j in range(V):
            if 0 <= mins[j] < m:
                minJ = j
                m = mins[j]
        if minJ == -1:
            # not possible to build
            return -1

        result += m
        mins[minJ] = -1

        for j in range(V):
            if mins[j] > 0 and graph[j][minJ] < mins[j]:
                mins[j] = graph[j][minJ]

    return result


if __name__ == '__main__':
    assert 0 == prim1([])
    assert 5 == prim1([[0, 5], [5, 0]])
    assert 5 == prim1([[0, 2, 3], [2, 0, 4], [3, 4, 0]])
