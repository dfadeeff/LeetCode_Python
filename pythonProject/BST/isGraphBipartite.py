from typing import List


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        """A graph is bipartite if you can color the nodes with two colors such that no two adjacent nodes have the same color.
        Think of it as divide nodes into two sets (A and B):
	    Node in set A -> all neighbors must be in set B
	    Node in set B -> all neighbors must be in set A

        If this is not possible (e.g., odd-length cycle), graph is not bipartite.
        """
        n = len(graph)
        color = {}  # node: color (0 or 1)

        def dfs(node, c):
            if node in color:
                return color[node] == c  # if already colored, check consistency
            color[node] = c  # color the node
            for neighbor in graph[node]:
                if not dfs(neighbor, 1 - c):
                    return False
            return True

        # In case of disconnected graph, check all nodes
        for node in range(n):
            if node not in color:
                if not dfs(node, 0):
                    return False

        return True


if __name__ == '__main__':
    graph = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
    print(Solution().isBipartite(graph))
