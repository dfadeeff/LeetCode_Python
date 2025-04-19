import re


class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = re.sub(r'[^A-Za-z0-9]', '', s.lower())
        left = 0
        right = len(cleaned) - 1
        while left < right:
            if cleaned[left] != cleaned[right]:
                return False
            left += 1
            right -= 1
        return True




if __name__ == "__main__":
    s = "A man, a plan, a canal: Panama"
    print(Solution().isPalindrome(s))
    s = "race a car"
    print(Solution().isPalindrome(s))