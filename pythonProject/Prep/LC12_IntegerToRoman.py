class Solution:
    def intToRoman(self, num: int) -> str:
        # 1) A list of all Roman symbols and their values,
        #    including the subtractive forms (“IV” = 4, “IX” = 9, etc.)
        symList = [["I", 1], ["IV", 4], ["V", 5], ["IX", 9], ["X", 10],
                   ["XL", 40], ["L", 50], ["XC", 90], ["C", 100], ["CD", 400],
                   ["D", 500], ["CM", 900], ["M", 1000]]
        # 2) This will accumulate our result string.
        res = ""
        # 3) We need to consume the largest‐value symbols first,
        #    so we reverse the list (so “M”/1000 comes before “CM”/900, etc).
        for sym, val in reversed(symList):
            # 4) How many times does this Roman value fit into the
            #    *current* number?
            #    Integer division gives 0 if val > num, or the count otherwise.
            if num // val:
                # 5) Record that count
                count = num // val
                # 6) Append the corresponding symbol that many times.
                #    In Python “'X' * 3” → “XXX”
                res += sym * count
                # 7) Remove that portion from num.
                #    num % val is exactly num − (val * count)
                num = num % val
        return res


if __name__ == "__main__":
    num = 3749
    print(Solution().intToRoman(num))
