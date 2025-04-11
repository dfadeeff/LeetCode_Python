class Solution:
    def calculate(self, s: str) -> int:
        """"
        in greedy manner, one pass from left to right
        •	cur: currently built number from digits (multi-digit numbers).
	    •	prev: previous value waiting to be processed. It accumulates multiplication or division.
	    •	res: result of evaluated additions and subtractions so far.
	    •	op: last operator, starts with '+' by default (since the first number is “positive”).


        """
        cur = prev = res = 0
        # defaulted to "+"
        op = '+'

        for i, ch in enumerate(s):
            if ch.isdigit():
                cur = cur * 10 + int(ch)

            if ch in '+-*/' or i == len(s) - 1:
                if op == '+':
                    res += prev
                    prev = cur
                elif op == '-':
                    res += prev
                    prev = -cur
                elif op == '*':
                    prev *= cur
                elif op == '/':
                    prev = int(prev / cur)  # truncate toward zero
                # always reset operator to character
                op = ch
                # reset current value to 0
                cur = 0

        return res + prev


if __name__ == "__main__":
    s = " 3+5 / 2 "
    print(Solution().calculate(s))
    s = "3+2*2"
    print(Solution().calculate(s))
