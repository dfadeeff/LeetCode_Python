from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        minprice = float("inf")
        maxSofar = float("-inf")

        for i in range(len(prices)):
            minprice = min(minprice, prices[i])
            if prices[i] - minprice > maxSofar:
                maxSofar = prices[i] - minprice


        return maxSofar


if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]
    print(Solution().maxProfit(prices))

