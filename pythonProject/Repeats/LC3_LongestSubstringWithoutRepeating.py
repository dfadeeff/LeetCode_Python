from collections import defaultdict


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        counts = defaultdict(int)
        left = ans = 0
        for right in range(len(s)):
            counts[s[right]] += 1
            while counts[s[right]] > 1:
                counts[s[left]] -= 1

                left += 1

            ans = max(ans, right - left + 1)

        return ans
if __name__ == "__main__":
    s = "bbbbb"
    print(Solution().lengthOfLongestSubstring(s))
    s = "pwwkew"
    print(Solution().lengthOfLongestSubstring(s))