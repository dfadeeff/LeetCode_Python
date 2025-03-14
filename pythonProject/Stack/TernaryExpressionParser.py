class Solution:
    def parseTernary(self, expression: str) -> str:
        stack = []

        for char in reversed(expression):
            if stack and stack[-1] == '?':
                stack.pop()  # Remove '?'
                true_result = stack.pop()
                stack.pop()  # Remove ':'
                false_result = stack.pop()
                # Choose based on condition char (T or F)
                stack.append(true_result if char == 'T' else false_result)
            else:
                stack.append(char)

        return stack[0]


if __name__ == "__main__":
    expression = "T?2:3"
    print(Solution().parseTernary(expression))
    expression = "F?1:T?4:5"
    print(Solution().parseTernary(expression))
