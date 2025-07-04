from black.trans import defaultdict


class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        freq = defaultdict(int)

        res = 0
        left = 0
        for right in range(len(s)):
            freq[s[right]] = 1 + freq.get(s[right], 0)

            while (right - left + 1) - max(freq.values()) > k:
                freq[s[left]] -= 1
                left += 1

            res = max(res, right - left + 1)

        return res


if __name__ == "__main__":
    s = "ABAB"
    k = 2
    print(Solution().characterReplacement(s, k))
    s = "AABABBA"
    k = 1
    print(Solution().characterReplacement(s, k))
