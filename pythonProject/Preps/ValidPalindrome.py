class Solution:
    def isPalindrome(self, s: str) -> bool:
        filtered = ''.join(c for c in s.lower() if c.isalnum())
        left = 0
        right = len(filtered) - 1

        while left < right:
            if filtered[left] != filtered[right]:
                return False
            left += 1
            right -= 1

        return True


if __name__ == "__main__":
    s = "A man, a plan, a canal: Panama"
    print(Solution().isPalindrome(s))
    s = "race a car"
    print(Solution().isPalindrome(s))
