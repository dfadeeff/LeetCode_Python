from typing import List
import heapq
from collections import defaultdict


class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """

        Problem:
        n nodes, edges = [src, dst, time]
        Signal sent from node k
        How long until ALL nodes receive signal?
        Return -1 if some node never receives it

        Insight:
        = find shortest path from k to ALL nodes
        = max of all shortest paths
        (last node to receive = total delay)
        """
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        # dist = shortest time to reach each node
        dist = {}

        # start at k, cost = 0
        pq = [(0, k)]

        while pq:
            cost, node = heapq.heappop(pq)
            # min heap → first time we pop a node, guaranteed shortest path
            if node in dist:  # already processed
                continue
            dist[node] = cost

            for neighbor, weight in graph[node]:
                if neighbor not in dist:
                    heapq.heappush(pq, (cost + weight, neighbor))

        # if not all nodes reached → return -1
        return max(dist.values()) if len(dist) == n else -1


if __name__ == "__main__":
    sol = Solution()
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    n = 4
    k = 2
    print(sol.networkDelayTime(times, n, k))
