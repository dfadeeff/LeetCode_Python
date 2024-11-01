import heapq
from typing import List


class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        projects = sorted(zip(capital, profits))
        i = 0
        heap = []  # max heap
        for _ in range(k):
            while i < len(projects) and projects[i][0] <= w:
                heapq.heappush(heap, -projects[i][1])
                i += 1

            if len(heap) == 0:
                return w
            w -= heapq.heappop(heap)  # since max heap, we take the negative of negative

        return w


def main():
    k = 2
    w = 0
    profits = [1, 2, 3]
    capital = [0, 1, 1]
    print(Solution().findMaximizedCapital(k, w, profits, capital))
    k = 3
    w = 0
    profits = [1, 2, 3]
    capital = [0, 1, 2]
    print(Solution().findMaximizedCapital(k, w, profits, capital))


if __name__ == '__main__':
    main()
