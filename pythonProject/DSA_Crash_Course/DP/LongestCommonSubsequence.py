class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        rows = len(text1)
        cols = len(text2)

        # dp[i][j] = LCS of text1[:i] and text2[:j]
        # Dimensions: (rows+1) x (cols+1)
        dp = [[0] * (cols + 1) for _ in range(rows + 1)]

        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if text1[i - 1] == text2[j - 1]:
                    # Characters match; extend the length by 1
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # for i in range(0, rows + 1):
        #     print(dp[i])
        return dp[rows][cols]


def main():
    text1 = "abcde"
    text2 = "ace"
    print(Solution().longestCommonSubsequence(text1, text2))
    # text1 = "abc"
    # text2 = "abc"
    # print(Solution().longestCommonSubsequence(text1, text2))


if __name__ == "__main__":
    main()
