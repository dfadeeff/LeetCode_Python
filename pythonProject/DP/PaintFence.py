class Solution:
    def numWays(self, n: int, k: int) -> int:
        if n <= 1:
            return k
        if n == 2:
            return k * k
        dp = [0] * (n + 1)
        dp[1] = k
        dp[2] = k * k
        for i in range(3, len(dp)):
            dp[i] = (k - 1) * (dp[i - 1] + dp[i - 2])

        return dp[len(dp) - 1]


if __name__ == "__main__":
    n = 3
    k = 2
    print(Solution().numWays(n, k))
    n = 7
    k = 2
    print(Solution().numWays(n, k))
