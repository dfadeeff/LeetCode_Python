class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []
        for c in s:

        # equivalent to stack != [] and stack[-1] == c:
        # empty list [] treated as false and non-empty as True
            if stack and stack[-1] == c:
                print(stack)
                stack.pop()
            else:
                stack.append(c)
                print(stack)
        return ''.join(stack)


if __name__ == "__main__":
    s = "abbaca"
    print(Solution().removeDuplicates(s))
    s = "azxxzy"
    print(Solution().removeDuplicates(s))