class Solution:
    def isMatch(self, text: str, pattern: str) -> bool:
        dp = [[False] * (len(pattern) + 1) for _ in range(len(text) + 1)]
        print("initial: ", dp)
        # Base case: empty text and empty pattern is a match
        dp[len(text)][len(pattern)] = True
        print("initial: ", dp)
        # Iterate backwards through text and pattern
        for i in range(len(text), -1, -1):
            for j in range(len(pattern) - 1, -1, -1):
                first_match = i < len(text) and pattern[j] in {text[i], "."}

                if j + 1 < len(pattern) and pattern[j + 1] == "*":
                    # Case 1: Skip 'x*'
                    # Case 2: If first characters match, move text forward
                    dp[i][j] = dp[i][j + 2] or (first_match and dp[i + 1][j])
                else:
                    # Move both forward
                    dp[i][j] = first_match and dp[i + 1][j + 1]

        return dp[0][0]


if __name__ == '__main__':
    s = "aa"
    p = "a"
    print(Solution().isMatch(s, p))
