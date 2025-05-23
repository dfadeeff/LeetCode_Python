from collections import defaultdict


def build_graph(edges):
    graph = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        # graph[y].append(x)
        # uncomment the above line if the graph is undirected

    return graph


if __name__ == '__main__':
    edges = [[0, 1], [1, 2], [2, 0], [2, 3]]
    """
    for directed edge, it would mean
    0 -> 1
    1 -> 2
    2 -> 0
    2 -> 3
    
    """
    print(build_graph(edges))
