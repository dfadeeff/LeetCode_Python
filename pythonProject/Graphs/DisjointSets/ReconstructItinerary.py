from collections import defaultdict
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)

        # Step 1: Build graph and sort destinations in lexical order
        for ticket_from, ticket_to in tickets:
            graph[ticket_from].append(ticket_to)
        for src in graph:
            graph[src].sort(reverse=True)  # reverse for efficient pop()

        route = []
        def dfs(node):
            while graph[node]:
                next_dest = graph[node].pop()
                dfs(next_dest)
            route.append(node)
        dfs("JFK")

        return route[::-1]


if __name__ == '__main__':
    tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    print(Solution().findItinerary(tickets))
