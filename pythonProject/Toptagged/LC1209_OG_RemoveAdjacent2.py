class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        stack = []
        for c in s:
            if stack and stack[-1][0] == c:
                stack[-1][1] += 1
            else:
                stack.append([c,1])

            if stack[-1][1] == k:
                stack.pop()

        res = ""
        for char, count in stack:
            res += (char*count)

        return res


if __name__ == "__main__":
    s = "deeedbbcccbdaa"
    k = 3
    print(Solution().removeDuplicates(s,k))
    s = "pbbcggttciiippooaais"
    k = 2
    print(Solution().removeDuplicates(s, k))