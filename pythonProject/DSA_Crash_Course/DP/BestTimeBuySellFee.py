from typing import List


class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        rows = len(prices)
        dp = [[0] * (2) for _ in range(rows + 1)]
        for i in range(rows - 1, -1, -1):
            for holding in range(2):
                ans = dp[i + 1][holding]
                if holding:
                    ans = max(ans, prices[i] + dp[i + 1][0] - fee)
                else:
                    ans = max(ans, -prices[i] + dp[i + 1][1])
                dp[i][holding] = ans
        # for i in range(0, rows + 1):
        #     print(dp[i])
        return dp[0][0]


def main():
    prices = [1, 3, 2, 8, 4, 9]
    fee = 2
    print(Solution().maxProfit(prices, fee))


if __name__ == '__main__':
    main()
