class Solution:
    def validPalindrome(self, s: str) -> bool:
        if len(s) <= 2:
            return True

        i = 0
        j = len(s) - 1

        while i < j:
            if s[i] != s[j]:
                # chop to move the indices
                return self.is_palindrome(s, i + 1, j) or self.is_palindrome(s, i, j - 1)
            else:
                i += 1
                j -= 1
        return True

    def is_palindrome(self, s, left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True


if __name__ == "__main__":
    s = "aba"
    print(Solution().validPalindrome(s))
