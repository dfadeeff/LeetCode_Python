from collections import defaultdict


class Solution:
    def canPermutePalindrome(self, s: str) -> bool:
        char_count = defaultdict(int)
        for char in s:
            char_count[char] += 1
        print(char_count)

        count_middle = 0
        for k, v in char_count.items():
            if v % 2 != 0:
                count_middle += 1
            if count_middle > 1:
                return False

        return True


if __name__ == '__main__':
    s = "code"
    print(Solution().canPermutePalindrome(s))
    s = "aab"
    print(Solution().canPermutePalindrome(s))
