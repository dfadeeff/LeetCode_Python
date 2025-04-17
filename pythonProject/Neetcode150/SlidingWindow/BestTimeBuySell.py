from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        minprice = float("inf")
        max_profit = 0
        for i in range(len(prices)):
            minprice = min(minprice, prices[i])
            if prices[i] - minprice > max_profit:
                max_profit = max(max_profit, prices[i] - minprice)

        return max_profit


if __name__ == "__main__":
    prices = [10, 1, 5, 6, 7, 1]
    print(Solution().maxProfit(prices))
