class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0  # Left pointer of the sliding window
        max_so_far = 0

        for right in range(len(s)):  # Right pointer moves through the string
            while s[right] in seen:  # If duplicate found, remove leftmost character
                seen.remove(s[left])
                left += 1  # Move left pointer to shrink window

            seen.add(s[right])  # Add current character
            max_so_far = max(max_so_far, right - left + 1)  # Update max length

        return max_so_far


if __name__ == '__main__':
    s = "abcabcbb"
    print(Solution().lengthOfLongestSubstring(s))
    s = "bbbbb"
    print(Solution().lengthOfLongestSubstring(s))
    s = "pwwkew"
    print(Solution().lengthOfLongestSubstring(s))
