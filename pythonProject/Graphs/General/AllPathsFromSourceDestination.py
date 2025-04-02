from collections import defaultdict
from typing import List

from pygments.lexers import graph


class Solution:
    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        """We must return True only if:
	1.	Every path from source leads to destination.
	2.	All terminal nodes (nodes with no outgoing edges) must be the destination.
	3.	There are no cycles in the paths from source.
	Use a DFS traversal with three states:
	•	0: unvisited
	•	1: visiting (currently on the recursion stack)
	•	2: visited (completed)


	"""
        graph = defaultdict(list)
        for edge_from, edge_to in edges:
            graph[edge_from].append(edge_to)

        state = [0] * n  # 0 = unvisited, 1 = visiting, 2 = visited and safe

        def dfs(node: int) -> bool:
            if state[node] == 1:
                return False  # cycle detected
            if state[node] == 2:
                return True  # already verified to be safe

            state[node] = 1  # mark as visiting

            if not graph[node]:
                state[node] = 2  # leaf node
                return node == destination  # must end at destination

            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False

            state[node] = 2  # mark as safe
            return True

        return dfs(source)


if __name__ == "__main__":
    n = 3
    edges = [[0, 1], [0, 2]]
    source = 0
    destination = 2
    print(Solution().leadsToDestination(n, edges, source, destination))
    n = 4
    edges = [[0, 1], [0, 3], [1, 2], [2, 1]]
    source = 0
    destination = 3
    print(Solution().leadsToDestination(n, edges, source, destination))
    n = 4
    edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    source = 0
    destination = 3
    print(Solution().leadsToDestination(n, edges, source, destination))
