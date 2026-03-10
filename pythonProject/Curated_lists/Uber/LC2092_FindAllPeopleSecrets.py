import heapq
from heapq import heappush, heappop
from math import inf
from typing import List
from collections import defaultdict, deque


class Solution:
    def findAllPeopleBFS(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        # For every person, store the time and label of the person met.
        graph = defaultdict(list)
        for x, y, t in meetings:
            graph[x].append((t, y))
            graph[y].append((t, x))

        print(graph)
        # Earliest time at which a person learned the secret
        earliest = [inf] * n
        earliest[0] = 0
        earliest[firstPerson] = 0

        # Queue for BFS. It will store (person, time of knowing the secret)
        q = deque()
        q.append((0, 0))
        q.append((firstPerson, 0))

        while q:
            person, time = q.popleft()
            for t, next_person in graph[person]:
                if t >= time and earliest[next_person] > t:
                    earliest[next_person] = t
                    q.append((next_person, t))

        return [i for i in range(n) if earliest[i] != inf]

    def findAllPeopleDFS(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        graph = defaultdict(list)
        for x, y, t in meetings:
            graph[x].append((t, y))
            graph[y].append((t, x))

        earliest = [inf] * n
        earliest[0] = 0
        earliest[firstPerson] = 0

        stack = [(0, 0), (firstPerson, 0)]
        while stack:
            person, time = stack.pop()
            for t, next_person in graph[person]:
                if t >= time and earliest[next_person] > t:
                    earliest[next_person] = t
                    stack.append((next_person,t))
        return [i for i in range(n) if earliest[i] != inf]

    def findAllPeoplePQ(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        graph = defaultdict(list)
        for x,y,t in meetings:
            graph[x].append((t,y))
            graph[y].append((t, x))

        # Priority Queue for BFS. It stores (time secret learned, person)
        pq = []
        heappush(pq,(0,0))
        heappush(pq,(0, firstPerson))

        # Visited array to mark if a person is visited or not.
        visited = [False] * n
        while pq:
            time, person = heappop(pq)
            if visited[person]:
                continue
            visited[person] = True
            for t, next_person in graph[person]:
                if not visited[next_person] and t >= time:
                    heappush(pq, (t, next_person))
        return [i for i in range(n) if visited[i]]


if __name__ == "__main__":
    sol = Solution()
    n = 6
    meetings = [[1, 2, 5], [2, 3, 8], [1, 5, 10]]
    firstPerson = 1
    print(sol.findAllPeopleBFS(n, meetings, firstPerson))
    print(sol.findAllPeopleDFS(n, meetings, firstPerson))
    print(sol.findAllPeoplePQ(n, meetings, firstPerson))
