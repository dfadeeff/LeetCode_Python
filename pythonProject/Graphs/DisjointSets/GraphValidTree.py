from collections import defaultdict
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        """"Recall that a graph, G, is a tree iff the following two conditions are met:

G is fully connected. In other words, for every pair of nodes in G, there is a path between them.
G contains no cycles. In other words, there is exactly one path between each pair of nodes in G.

Alternatively, For the graph to be a valid tree, it must have exactly n - 1 edges. Any less, and it can't possibly be fully connected. Any more, and it has to contain cycles.
"""
        if len(edges) != n - 1:
            return False
        graph = defaultdict(list)
        for edge_from, edge_to in edges:
            graph[edge_from].append(edge_to)
            graph[edge_to].append(edge_from)
        print(graph)

        def dfs(node, parent):

            seen.add(node)
            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if neighbor in seen:
                    return False
                result = dfs(neighbor, node)
                if not result:
                    return False
            return True

        seen = set()
        return dfs(0, -1) and len(seen) == n


if __name__ == '__main__':
    n = 5
    edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
    print(Solution().validTree(n, edges))
    n = 5
    edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
    print(Solution().validTree(n, edges))
