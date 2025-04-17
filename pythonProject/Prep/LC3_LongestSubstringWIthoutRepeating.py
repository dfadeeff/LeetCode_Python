class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = curr = 0
        for right in range(len(s)):

            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            curr = max(curr, right - left + 1)
        return curr


if __name__ == "__main__":
    s = "abcabcbb"
    print(Solution().lengthOfLongestSubstring(s))