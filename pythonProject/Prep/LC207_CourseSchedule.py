from collections import defaultdict, deque
from typing import List


class Solution:
    def canFinishDFS(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Step 1: Build the graph
        graph = defaultdict(list)
        for edge_from, edge_to in prerequisites:
            graph[edge_from].append(edge_to)

        # Step 2: Define states: 0 = unvisited, 1 = visiting, 2 = visited
        state = [0] * numCourses

        # Step 3: DFS to detect cycles
        def dfs(node):
            if state[node] == 1:
                return False  # cycle detected
            if state[node] == 2:
                return True  # already visited and no cycle

            state[node] = 1  # mark as visiting
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    return False
            state[node] = 2  # mark as visited/safe
            return True

        # Step 4: Visit all nodes
        for i in range(numCourses):
            if not dfs(i):
                return False

        return True

    def canFinishTopo(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Build graph and in-degree array
        graph = defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        # Start with nodes having in-degree 0
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
        count = 0

        while queue:
            node = queue.popleft()
            count += 1
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return count == numCourses


if __name__ == "__main__":
    numCourses = 2
    prerequisites = [[1, 0], [0, 1]]
    print(Solution().canFinishTopo(numCourses, prerequisites))
