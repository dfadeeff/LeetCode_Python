from collections import deque
from typing import List


class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:

        # Helper function to check if bomb j is within the range of bomb i
        def in_range(i, j):
            x1, y1, r1 = bombs[i]
            x2, y2, _ = bombs[j]
            return (x2 - x1) ** 2 + (y2 - y1) ** 2 <= r1 ** 2

        # Build the adjacency list representing which bombs can detonate others
        n = len(bombs)
        adj = [[] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j and in_range(i, j):
                    adj[i].append(j)

        # BFS to calculate how many bombs can be detonated starting from bomb `start`
        def bfs(start):
            queue = deque([start])
            visited = set([start])
            count = 1  # The starting bomb itself is detonated

            while queue:
                node = queue.popleft()
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        count += 1
            return count

        # Run BFS for each bomb and find the maximum number of bombs detonated
        max_detonations = 0
        for i in range(n):
            max_detonations = max(max_detonations, bfs(i))

        return max_detonations


# Example Usage
def main():
    bombs = [[2, 1, 3], [6, 1, 4]]
    print(Solution().maximumDetonation(bombs))  # Output: 2

    bombs = [[1, 1, 5], [10, 10, 5]]
    print(Solution().maximumDetonation(bombs))  # Output: 1

    bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]
    print(Solution().maximumDetonation(bombs))  # Output: 5

if __name__ == '__main__':
    main()
