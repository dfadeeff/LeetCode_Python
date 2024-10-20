from collections import defaultdict
from typing import List


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        def answer_query(start, end):
            # no info on this node
            if start not in graph:
                return -1

            seen = {start}
            stack = [(start, 1)]

            while stack:
                node, ratio = stack.pop()
                if node == end:
                    return ratio

                for neighbor in graph[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append((neighbor, ratio * graph[node][neighbor]))

            return -1

        graph = defaultdict(dict)
        for i in range(len(equations)):
            numerator, denominator = equations[i]
            val = values[i]
            graph[numerator][denominator] = val
            graph[denominator][numerator] = 1 / val

        ans = []
        for numerator, denominator in queries:
            ans.append(answer_query(numerator, denominator))

        return ans


def main():
    equations = [["a", "b"], ["b", "c"]]
    values = [2.0, 3.0]
    queries = [["a", "c"], ["b", "a"], ["a", "e"],["a", "a"], ["x", "x"]]
    print(Solution().calcEquation(equations, values, queries))


if __name__ == "__main__":
    main()