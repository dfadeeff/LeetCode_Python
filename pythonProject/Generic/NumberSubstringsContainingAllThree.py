class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        freq = {'a': 0, 'b': 0, 'c': 0}
        ans = left = 0
        for right, ch in enumerate(s):
            # 1) include s[right]
            freq[ch] += 1

            # 2) while window [L..R] has at least one of each:
            while freq['a'] > 0 and freq['b'] > 0 and freq['c'] > 0:
                # any substring starting at L and ending at >= R is valid
                ans += n - right
                # shrink from the left
                freq[s[left]] -= 1
                left += 1
        return ans


if __name__ == "__main__":
    s = "abcabc"
    print(Solution().numberOfSubstrings(s))
