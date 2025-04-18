class Solution:
    def romanToInt(self, s: str) -> int:
        roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        res = 0

        for i in range(len(s)):
            # check inbounds, it is increasing, it should be subtracted
            if i + 1 < len(s) and roman[s[i]] < roman[s[i + 1]]:
                res -= roman[s[i]]
            else:
                res += roman[s[i]]

        return res


if __name__ == "__main__":
    s = "MCMXCIV"
    print(Solution().romanToInt(s))
    s = "LVIII"
    print(Solution().romanToInt(s))
