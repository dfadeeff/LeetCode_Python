from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        sold, held, reset = float('-inf'), float('-inf'), 0

        for price in prices:
            # Alternative: the calculation is done in parallel.
            # Therefore no need to keep temporary variables
            #sold, held, reset = held + price, max(held, reset-price), max(reset, sold)

            pre_sold = sold
            sold = held + price
            held = max(held, reset - price)
            reset = max(reset, pre_sold)

        return max(sold, reset)


def main():
    prices = [1, 2, 3, 0, 2]
    print(Solution().maxProfit(prices))
    prices = [1]
    print(Solution().maxProfit(prices))


if __name__ == '__main__':
    main()
