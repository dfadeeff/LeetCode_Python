class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        extra_opens = 0
        total_opens = 0
        temp = ""
        for i in range(len(s)):
            if s[i] == ')':
                if extra_opens == 0:
                    continue
                else:
                    extra_opens -= 1
                    temp += s[i]
            elif s[i] == '(':
                total_opens += 1
                extra_opens += 1
                temp += s[i]
            else:
                temp += s[i]

        result = []
        keep = total_opens - extra_opens

        for i in range(len(temp)):
            if temp[i] == '(':
                if keep == 0:
                    continue
                result.append(temp[i])
                keep -= 1
            else:
                result.append(temp[i])

        return result

    def minRemoveToMakeValidStack(self, s: str) -> str:
        stack = []
        to_remove = set()

        # Step 1: Identify positions to remove
        for index, char in enumerate(s):
            if char == '(':
                stack.append(index)
            elif char == ')':
                if stack:
                    stack.pop()  # matched '('
                else:
                    to_remove.add(index)  # unmatched ')'

        # Add any unmatched '(' left in the stack
        to_remove.update(stack)

        # Step 2: Build the result string
        result = []
        for i, c in enumerate(s):
            if i not in to_remove:
                result.append(c)

        return ''.join(result)


if __name__ == '__main__':
    s = "lee(t(c)o)de)"
    print(Solution().minRemoveToMakeValid(s))
    print(Solution().minRemoveToMakeValidStack(s))
