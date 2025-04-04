import re


class Solution:
    def isPalindrome(self, s: str) -> bool:
        string_fixed = s.lower()
        string_fixed = re.sub(r'[^a-zA-Z0-9]', '', string_fixed)

        left = 0
        right = len(string_fixed)-1
        while left < right:
            if string_fixed[left] != string_fixed[right]:
                return False
            left += 1
            right -= 1

        return True


if __name__ == '__main__':
    s = "A man, a plan, a canal: Panama"
    print(Solution().isPalindrome(s))
