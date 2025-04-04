from collections import defaultdict
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        for edge_from, edge_to in prerequisites:
            graph[edge_to].append(edge_from)
        print(graph)

        result = []
        state = [0] * (numCourses)

        def dfs(node):
            if state[node] == 1:
                return False
            if state[node] == 2:
                return True
            state[node] = 1  # mark visiting
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            state[node] = 2
            result.append(node)
            return True

        for i in range(numCourses):
            if state[i] == 0:
                if not dfs(i):
                    return []

        return result[::-1]  # reverse post-order


if __name__ == "__main__":
    numCourses = 4
    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]  # 1 -> 0, 2 -> 0, 3 -> [1,2]
    print(Solution().findOrder(numCourses, prerequisites))
