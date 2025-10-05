class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        start = 0
        max_len = 1

        for i in range(len(s)):
            # Odd-length palindrome
            left1, right1 = self.expand(s, i, i)
            # Even-length palindrome
            left2, right2 = self.expand(s, i, i + 1)

            if right1 - left1 + 1 > max_len:
                start, max_len = left1, right1 - left1 + 1
            if right2 - left2 + 1 > max_len:
                start, max_len = left2, right2 - left2 + 1

        return s[start:start + max_len]



    def expand(self, s, left, right):
        """Expand around center and return bounds of palindrome."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return last valid indices (after one overstep)
        return left + 1, right - 1

if __name__ == "__main__":
    s = "bab"
    print(Solution().longestPalindrome(s))
    s = "babaac"
    print(Solution().longestPalindrome(s))
