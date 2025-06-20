class Solution:
    def isValid(self, s: str) -> bool:

        matching = {")": "(", "}": "{", "]": "["}
        stack = []
        for c in s:
            if c in matching:
                if stack and stack[-1] == matching[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        return True if not stack else False


if __name__ == "__main__":
    s = "()[]{}"
    print(Solution().isValid(s))
