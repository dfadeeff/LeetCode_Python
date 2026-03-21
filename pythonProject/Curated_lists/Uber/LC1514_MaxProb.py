import heapq
from typing import List

from collections import defaultdict


class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start_node: int,
                       end_node: int) -> float:
        graph = defaultdict(list)
        for (u, v), p in zip(edges, succProb):
            graph[u].append((v, p))
            graph[v].append((u, p))  # undirected

        dist = {}
        pq = [(-1.0, start_node)]  # negate: min heap → max prob

        while pq:
            prob, node = heapq.heappop(pq)
            prob = -prob  # restore actual probability

            if node in dist:
                continue
            dist[node] = prob

            if node == end_node:
                return prob  # first time = max probability

            for neighbor, p in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(pq, (-(prob * p), neighbor))

        return 0.0


if __name__ == "__main__":
    sol = Solution()
    n = 3
    edges = [[0, 1], [1, 2], [0, 2]]
    succProb = [0.5, 0.5, 0.2]
    start = 0
    end = 2
    print(sol.maxProbability(n, edges, succProb, start, end))
