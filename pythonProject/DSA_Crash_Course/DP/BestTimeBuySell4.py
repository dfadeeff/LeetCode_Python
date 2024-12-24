from typing import List


class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        """At each state, what decisions do we have? If we are not holding stock, we can either buy today or skip. If we buy, then our profit is -prices[i] + dp(i + 1, true, remain). We spend prices[i] to buy the stock. Then we move to the next day (i + 1), we are now holding stock (true), and we haven't completed a transaction yet so remain stays the same.

        If we are holding stock, we can either sell today or skip. If we sell, then our profit is prices[i] + dp(i + 1, false, remain - 1). We gain prices[i] money. Then we move to the next day (i + 1), we are no longer holding stock (false), and we used up one of our transactions (remain - 1).
        """
        n = len(prices)
        dp = [[[0] * (k + 1) for _ in range(2)] for __ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for remain in range(1, k + 1):
                for holding in range(2):
                    ans = dp[i + 1][holding][remain]
                    if holding:
                        ans = max(ans, prices[i] + dp[i + 1][0][remain - 1])
                    else:
                        ans = max(ans, -prices[i] + dp[i + 1][1][remain])

                    dp[i][holding][remain] = ans

        return dp[0][0][k]



def main():
    k = 2
    prices = [2, 4, 1]
    print(Solution().maxProfit(k, prices))


if __name__ == '__main__':
    main()
