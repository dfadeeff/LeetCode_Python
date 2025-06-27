class Solution:
    def decodeString(self, s: str) -> str:
        stack = []

        for i in range(len(s)):
            if s[i] != "]":
                stack.append(s[i])

            else:
                substr = ""
                while stack[-1] != "[":
                    substr = stack.pop() + substr
                stack.pop()  # opening bracket
                k = ""
                while stack and stack[-1].isdigit():
                    k = stack.pop() + k # prepend, not append

                stack.append(int(k) * substr)

        return "".join(stack)


if __name__ == "__main__":
    s = "3[a]2[bc]"
    print(Solution().decodeString(s))
