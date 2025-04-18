class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[len(dp) - 1]


if __name__ == '__main__':
    n = 2
    print(Solution().climbStairs(n))
    n = 3
    print(Solution().climbStairs(n))
