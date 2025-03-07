from collections import defaultdict


class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        left = 0
        char_count = defaultdict(int)  # Dictionary to store character frequency
        max_length = 0

        for right in range(len(s)):  # Expand window
            char_count[s[right]] += 1

            while len(char_count) > 2:  # More than 2 distinct characters, shrink window
                char_count[s[left]] -= 1
                if char_count[s[left]] == 0:
                    del char_count[s[left]]  # Remove character when count reaches 0
                left += 1  # Move left pointer to shrink window

            max_length = max(max_length, right - left + 1)  # Update max length

        return max_length


if __name__ == '__main__':
    s = "eceba"
    print(Solution().lengthOfLongestSubstringTwoDistinct(s))
    s = "ccaabbb"
    print(Solution().lengthOfLongestSubstringTwoDistinct(s))
