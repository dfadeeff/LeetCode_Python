import heapq
from typing import List


class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        maxProfits = []  # only projects can afford
        minCapital = [(c, p) for c, p in zip(capital, profits)]
        heapq.heapify(minCapital)

        for i in range(k):
            while minCapital and minCapital[0][0] <= w:
                c, p = heapq.heappop(minCapital)
                heapq.heappush(maxProfits, -p)
            if not maxProfits:
                break
            w += (-1) * heapq.heappop(maxProfits)
        return w


if __name__ == "__main__":
    k = 2
    w = 0
    profits = [1, 2, 3]
    capital = [0, 1, 1]
    print(Solution().findMaximizedCapital(k, w, profits, capital))
