from collections import defaultdict
from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        def dfs(node):
            """Performs depth-first search (DFS) to visit all nodes in a province."""
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor)  # DFS ends here

        n = len(isConnected)

        # hashmap
        graph = defaultdict(list)

        # Build the graph in adjacency list
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    graph[i].append(j)
                    graph[j].append(i)

        # Code to print the adjacency list!
        print("Adjacency List of the Graph:")
        for key, value in graph.items():
            print(f"{key}: {value}")

        # Create the adjacency matrix!
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j]:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1

        # Print the adjacency matrix
        print("\nAdjacency Matrix of the Graph:")
        for row in adj_matrix:
            print(row)

        seen = set()
        ans = 0

        # Traverse each city to find provinces
        for i in range(n):
            # If the city hasn't been visited, it's a new province, ie new component
            if i not in seen:
                ans += 1
                seen.add(i)
                dfs(i)  # Perform DFS to mark all cities in the same province as visited

        return ans


def main():
    isConnected1 = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    print(Solution().findCircleNum(isConnected1))
    isConnected2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    print(Solution().findCircleNum(isConnected2))


if __name__ == '__main__':
    main()
