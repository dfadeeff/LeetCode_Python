class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:

        n = len(s)
        dp = [0] * n  # Initialize 1D DP array

        for i in range(n - 2, -1, -1):  # from second last char to start
            prev = 0
            for j in range(i + 1, n):
                temp = dp[j]  # save current dp[j] (which is dp[i+1][j])

                if s[i] == s[j]:
                    dp[j] = prev  # dp[i][j] = dp[i+1][j-1]
                else:
                    dp[j] = 1 + min(dp[j], dp[j - 1])  # dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])

                prev = temp  # update prev for next iteration

        return dp[n - 1] <= k


if __name__ == '__main__':
    s = "abcdeca"
    k = 2
    print(Solution().isValidPalindrome(s, k))