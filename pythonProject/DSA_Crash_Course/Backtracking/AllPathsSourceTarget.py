from typing import List


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        target = len(graph) - 1
        results = []

        def backtrack(curr_node, path):
            # if we reach the target, no need to explore further.
            if curr_node == target:
                results.append(list(path))
                return
            # explore the neighbor nodes one after another.
            for next_node in graph[curr_node]:
                path.append(next_node)
                backtrack(next_node, path)
                path.pop()

        # kick of the backtracking, starting from the source node (0).
        path = [0]
        backtrack(0, path)
        return results


def main():
    graph = [[1, 2], [3], [3], []]
    print(Solution().allPathsSourceTarget(graph))
    graph = [[4, 3, 1], [3, 2, 4], [3], [4], []]
    print(Solution().allPathsSourceTarget(graph))


if __name__ == '__main__':
    main()
