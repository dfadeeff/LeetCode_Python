from typing import List

from collections import defaultdict, deque


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # ---- BUILD GRAPH + COUNT IN-DEGREES ----

        graph = defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            graph[prereq].append(course)  # prereq → course
            in_degree[course] += 1  # course has one more dependency

        # ---- FIND ALL STARTING POINTS ----
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i) # no prerequisites = ready

        # ---- PROCESS (BFS) ----
        courses_taken = 0

        while queue:
            node = queue.popleft()
            courses_taken += 1

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return courses_taken == numCourses



if __name__ == "__main__":
    solution = Solution()
    numCourses = 2
    prerequisites = [[1, 0], [0, 1]]

    print(solution.canFinish(numCourses, prerequisites))
