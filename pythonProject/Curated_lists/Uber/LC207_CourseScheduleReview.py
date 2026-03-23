from typing import List
from collections import defaultdict


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)

        print(graph)

        state = [0] * numCourses

        def dfs(node):
            if state[node] == 1:  # GRAY → cycle
                return False
            if state[node] == 2:  # BLACK → already safe
                return True

            state[node] = 1  # mark GRAY — entering
            for nb in graph[node]:
                if not dfs(nb):
                    return False

            state[node] = 2
            return True

        return all(dfs(i) for i in range(numCourses))


if __name__ == "__main__":
    sol = Solution()
    numCourses = 2
    prerequisites = [[1, 0], [0, 1]]
    print(sol.canFinish(numCourses, prerequisites))
