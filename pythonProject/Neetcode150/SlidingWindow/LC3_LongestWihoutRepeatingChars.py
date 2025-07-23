from collections import Counter

from black.trans import defaultdict


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        hashmap = defaultdict(int)
        left = 0
        ans = 0

        for right in range(len(s)):
            charR = s[right]
            hashmap[charR] += 1
            while hashmap[charR] > 1:
                charL = s[left]
                hashmap[charL] -= 1
                left += 1
            ans = max(ans, right - left + 1)
        return ans


if __name__ == "__main__":
    s = "abcabcbb"
    print(Solution().lengthOfLongestSubstring(s))
    s = "bbbbb"
    print(Solution().lengthOfLongestSubstring(s))