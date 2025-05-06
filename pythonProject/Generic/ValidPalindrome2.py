class Solution:
    def validPalindrome(self, s: str) -> bool:
        i = 0
        j = len(s) - 1
        while i < j:
            if s[i] != s[j]:
                return self.isPalindromeCheck(s, i + 1, j) or self.isPalindromeCheck(s, i, j - 1)
            else:
                i += 1
                j -= 1
        return True

    def isPalindromeCheck(self, s, left, right):

        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True


if __name__ == "__main__":
    s = "aba"
    print(Solution().validPalindrome(s))
    s = "abca"
    print(Solution().validPalindrome(s))
    s = "abc"
    print(Solution().validPalindrome(s))