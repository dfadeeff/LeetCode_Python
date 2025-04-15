class Solution:
    def isValidPalindrome1DPBottomUp(self, s: str, k: int) -> bool:
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

    def isValidPalindrome(self, s: str, k: int) -> bool:
        self.string = s
        if not k:
            return self.isValidPalindrome(0, len(s) - 1)

        memo = {}

        def helper(i, j, k):
            if (i, j, k) in memo:
                return memo[(i, j, k)]
            elif not k:
                memo[(i, j, k)] = self.is_palindrome(i, j)
            else:
                while i < j:
                    if self.string[i] != self.string[j]:
                        memo[(i, j, k)] = helper(i + 1, j, k - 1) or helper(i, j - 1, k - 1)
                        return memo[(i, j, k)]
                    i += 1
                    j -= 1
                memo[(i, j, k)] = True
            return memo[(i, j, k)]

        return helper(0, len(self.string) - 1, k)

    def is_palindrome(self, i, j):
        while i < j:
            if self.string[i] != self.string[j]:
                return False
            i += 1
            j -= 1
        return True


if __name__ == "__main__":
    s = "abcdeca"
    k = 2
    print(Solution().isValidPalindrome(s, k))
    print(Solution().isValidPalindrome1DPBottomUp(s, k))
