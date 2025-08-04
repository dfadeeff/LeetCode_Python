class Solution:
    def validPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            if s[left] != s[right]:
                return self.palindrome(s, left + 1, right) or self.palindrome(s, left, right - 1)
            left += 1
            right -= 1

        return True

    def palindrome(self, s, left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True


if __name__ == "__main__":
    s = "aba"
    print(Solution().palindrome(s))
    s = "abca"
    print(Solution().palindrome(s))
