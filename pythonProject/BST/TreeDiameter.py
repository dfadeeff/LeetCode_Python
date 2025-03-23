from collections import defaultdict
from typing import List


class Solution:
    def treeDiameter(self, edges: List[List[int]]) -> int:
        # Build adjacency list
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        print(graph)
        max_diameter = 0

        def dfs(node, parent):
            nonlocal max_diameter
            longest, second_longest = 0, 0  # Top two longest paths from this node

            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                depth = dfs(neighbor, node)
                if depth > longest:
                    longest, second_longest = depth, longest
                elif depth > second_longest:
                    second_longest = depth

            # Update the max diameter at this node
            max_diameter = max(max_diameter, longest + second_longest)
            return longest + 1  # Return longest path from this node to parent

        dfs(0, -1)
        return max_diameter


if __name__ == '__main__':
    edges = [[0, 1], [1, 2], [2, 3], [1, 4], [4, 5]]
    print(Solution().treeDiameter(edges))
