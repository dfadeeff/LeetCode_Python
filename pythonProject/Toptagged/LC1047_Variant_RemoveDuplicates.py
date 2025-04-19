from collections import defaultdict

class Solution:
    def removeDuplicates(self, s: str) -> str:
        while True:
            i = 0 # i tracks the start of a potential group.
            changed = False
            stack = []

            while i < len(s):
                # This looks ahead from position i to find how many same characters are in a row.
                count = 1
                while i + 1 < len(s) and s[i] == s[i + 1]:
                    i += 1
                    count += 1
                if count == 1:
                    stack.append(s[i])
                else:
                    changed = True  # group removed
                i += 1

            s = ''.join(stack)
            if not changed:
                return s


if __name__ == "__main__":
    s = "abbbacxdd"
    print(Solution().removeDuplicates(s))