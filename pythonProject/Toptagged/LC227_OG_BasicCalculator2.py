class Solution:
    def calculate(self, s: str) -> int:
        """"
        cur: tracks the current number being built (multi-digit support)
        op: the previous operator encountered (+ by default)
        prev: stores the result of the last multiplication/division (to be added/subtracted later)
        res: the running total of all + and - operations

        """
        cur = res = prev = 0
        op = "+"

        for i, c in enumerate(s):
            print("i:", i, " c :", c)
            if c.isdigit():
                cur = cur * 10 + int(c)

            if c in "+-/*" or i == len(s) - 1:
                if op == "+":
                    res += prev
                    prev = cur
                elif op == "-":
                    res += prev
                    prev = -cur
                elif op == "*":
                    prev *= cur
                elif op == "/":
                    prev = int(prev / cur)
                op = c
                cur = 0

        return res + prev


if __name__ == "__main__":
    # s = "3+2*2"
    # print(Solution().calculate(s))
    s = " 3+5 / 2 "
    print(Solution().calculate(s))
