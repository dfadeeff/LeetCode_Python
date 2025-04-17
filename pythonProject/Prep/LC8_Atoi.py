class Solution:
    def myAtoi(self, s: str) -> int:
        i, n = 0, len(s)
        # 1) Skip leading whitespace, simply ignore
        while i < n and s[i] == ' ':
            i += 1

        # 2) Handle optional sign
        sign = 1
        if i < n and s[i] in ('+', '-'):
            if s[i] == '-':
                sign = -1
            i += 1

        # 3) Convert digits
        num = 0
        INT_MIN, INT_MAX = -2 ** 31, 2 ** 31 - 1
        while i < n and s[i].isdigit():
            digit = ord(s[i]) - ord('0')
            # 4) Check for overflow before it happens
            if num > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN
            num = num * 10 + digit
            i += 1

        return sign * num


if __name__ == "__main__":
    s = " -042"
    print(Solution().myAtoi(s))
    s = "1337c0d3"
    print(Solution().myAtoi(s))
