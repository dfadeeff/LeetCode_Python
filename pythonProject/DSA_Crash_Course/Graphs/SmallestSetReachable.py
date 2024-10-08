from typing import List


class Solution:
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        indegree = [0] * n
        for _, y in edges:
            indegree[y] += 1

        return [node for node in range(n) if indegree[node] == 0]


def main():
    n = 6
    edges = [[0, 1], [0, 2], [2, 5], [3, 4], [4, 2]]
    print(Solution().findSmallestSetOfVertices(n, edges))


if __name__ == '__main__':
    main()
