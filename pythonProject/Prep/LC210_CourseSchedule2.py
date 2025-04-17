from collections import defaultdict, deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        in_degree = [0] * numCourses

        # Step 1: Build graph and in-degree list
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1
        print(graph)
        print("indegree: ", in_degree)
        # Step 2: Collect nodes with 0 in-degree
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        topo_order = []

        # Step 3: Kahn’s Algorithm
        while queue:
            node = queue.popleft()
            topo_order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Step 4: Check if all nodes were included
        if len(topo_order) == numCourses:
            return topo_order
        else:
            return []  # There is a cycle, cannot finish all courses


if __name__ == "__main__":
    numCourses = 4
    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    print(Solution().findOrder(numCourses, prerequisites))
