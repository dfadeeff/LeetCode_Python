from typing import List

from collections import defaultdict, deque

class Solution:
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        # ---- BUILD GRAPH ----
        # For each original edge u→v:
        #   graph[u] → (v, 0)   "going u→v is FREE (original direction)"
        #   graph[v] → (u, 1)   "going v→u COSTS 1 reversal"

        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append((v, 0))  # original direction = free
            graph[v].append((u, 1))  # reverse direction = costs 1

        # ---- PASS 1: DFS FROM NODE 0 ----
        # Count total reversals needed if 0 is root

        answer = [0] * n
        visited = [False] * n

        def dfs(node):
            visited[node] = True
            for neighbor, cost in graph[node]:
                if not visited[neighbor]:
                    answer[0] += cost  # accumulate reversals for root 0
                    dfs(neighbor)

        dfs(0)

        # ---- PASS 2: BFS TO RE-ROOT ----
        # For each neighbor, apply the +1/-1 rule

        visited = [False] * n
        visited[0] = True
        queue = deque([0])

        while queue:
            node = queue.popleft()

            for neighbor, cost in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True

                    if cost == 0:
                        # Forward edge (node → neighbor is original)
                        # Moving root to neighbor: this edge was free, now costs 1
                        answer[neighbor] = answer[node] + 1
                    else:
                        # Backward edge (neighbor → node is original)
                        # Moving root to neighbor: this edge cost 1, now free
                        answer[neighbor] = answer[node] - 1

                    queue.append(neighbor)

        return answer


if __name__ == "__main__":
    solution = Solution()
    n = 4
    edges = [[2, 0], [2, 1], [1, 3]]
    print(solution.minEdgeReversals(n, edges))
    n = 3
    edges = [[1, 2], [2, 0]]
    print(solution.minEdgeReversals(n, edges))
