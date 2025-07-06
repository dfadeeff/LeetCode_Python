import re


class Solution:
    def isPalindrome(self, s: str) -> bool:
        string_parsed = re.sub(r'[^A-Za-z0-9]', '', s.lower())

        left = 0
        right = len(string_parsed) - 1
        while left < right:
            if string_parsed[left] != string_parsed[right]:
                return False
            left += 1
            right -= 1

        return True


if __name__ == '__main__':
    s = "Was it a car or a cat I saw?"
    print(Solution().isPalindrome(s))
    s = "tab a cat"
    print(Solution().isPalindrome(s))
