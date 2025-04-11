class Solution:
    def calculate(self, s: str) -> int:
        """"
        only + and - operators are allowed
        Solve in linear time, from left to right
        [res, sign]

        """
        # initialize and track current result
        curr = res = 0
        sign = 1  # 1 for "+" and -1 for "-"
        stack = []
        for char in s:
            if char.isdigit():
                curr = curr * 10 + int(char)
            elif char in ['+', '-']:
                res += sign * curr
                # reset the sign
                sign = 1 if char == '+' else -1
                curr = 0
            elif char == '(':
                stack.append(res)
                stack.append(sign)
                sign = 1
                res = 0
            elif char == ')':
                res += sign * curr
                res *= stack.pop()
                res += stack.pop()  # previous result
                curr = 0

        return res + sign * curr


if __name__ == "__main__":
    s = " 2-1 + 2 "
    print(Solution().calculate(s))
    s = "(1+(4+5+2)-3)+(6+8)"
    print(Solution().calculate(s))
