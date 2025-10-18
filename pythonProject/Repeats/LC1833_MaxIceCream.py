from typing import List


class Solution:

    def maxIceCream(self, costs: List[int], coins: int) -> int:
        costs.sort()

        ans = 0
        for i in costs:
            if i <= coins:
                coins -= i
                ans += 1
        return ans


if __name__ == "__main__":
    costs = [1, 3, 2, 4, 1]
    coins = 7
    print(Solution().maxIceCream(costs, coins))
