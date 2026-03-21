from typing import List


class Solution:
    def maxNumberOfAlloys(self, n: int, k: int, budget: int, composition: List[List[int]], stock: List[int],
                          cost: List[int]) -> int:

        def can_make(mid, machine):
            total = 0
            for j in range(n):
                needed = composition[machine][j] * mid
                shortage = max(0, needed - stock[j])
                total += shortage * cost[j]
                if total > budget:
                    return False
            return True

        lo = 0
        hi = max(stock) + budget   # ← fix

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if any(can_make(mid, i) for i in range(k)):
                lo = mid
            else:
                hi = mid - 1

        return lo


if __name__ == "__main__":
    sol = Solution()
    print(sol.maxNumberOfAlloys(
        n=3, k=2, budget=15,
        composition=[[1, 1, 1], [1, 1, 10]],
        stock=[0, 0, 0],
        cost=[1, 2, 3]
    ))  # 2
