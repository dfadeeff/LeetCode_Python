import heapq
from typing import List

from collections import defaultdict


class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, c in flights:
            graph[u].append((v, c))

        # (cost, node, stops_remaining)
        pq = [(0, src, k)]
        visited = {}  # node → best stops_remaining seen

        while pq:
            cost, node, stops = heapq.heappop(pq)
            if node == dst:
                return cost

            if stops < 0:
                continue

            # prune: visited this node with >= stops remaining
            if node in visited and visited[node] >= stops:
                continue
            visited[node] = stops

            for neighbor, price in graph[node]:
                heapq.heappush(pq, (cost + price, neighbor, stops - 1))

        return -1


if __name__ == "__main__":
    sol = Solution()
    n = 4
    flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    src = 0
    dst = 3
    k = 1
    print(sol.findCheapestPrice(n, flights, src, dst, k))
