class Solution:

    def isValid(self, s: str):
        stack = []
        matching = {"(": ")", "[": "]", "{": "}"}

        for c in s:
            if c in matching:
                stack.append(c)

            else:  # if thats is closing
                if not stack:
                    return False

                previous_opening = stack.pop()
                if matching[previous_opening] != c:
                    return False
        return not stack


if __name__ == "__main__":
    s = "()[]{}"
    print(Solution().isValid(s))
    s = "([])"
    print(Solution().isValid(s))
    s = "(]"
    print(Solution().isValid(s))
