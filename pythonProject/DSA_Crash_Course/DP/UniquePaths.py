class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # start from rows
        for i in range(1, m + 1):
            # go through cols
            for j in range(1, n + 1):
                if i==1:
                    dp[i][j] = 1
                elif j == 1:
                    dp[i][j] = 1
                else:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        # for i in range(0, m + 1):
        #     print(dp[i])
        return dp[m][n]


def main():
    m = 3
    n = 7
    print(Solution().uniquePaths(m, n))


if __name__ == '__main__':
    main()
