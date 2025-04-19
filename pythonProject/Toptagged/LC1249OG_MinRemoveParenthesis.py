class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        # 1) First pass: remove “bad” ')' that have no matching '(' before them.
        res = []
        count = 0  # how many '(' we have in res that still need matching ')'
        for c in s:
            if c == "(":
                res.append(c)
                count += 1
            elif c == ")" and count > 0:
                res.append(c)
                count -= 1
            elif c != ")":
                res.append(c)

        # 2) Second pass: remove extra '(' from the end, as many as open_needed
        #    (these never found a matching ')' in the first pass)
        # The goal of the second pass is to get rid of any unmatched '(' that survived the first scan.
        filtered = []
        for c in res[::-1]:
            if c == "(" and count > 0:
                count -= 1  # and we dont append it to the string
            else:
                filtered.append(c)

        return "".join(filtered[::-1])

    def minRemoveToMakeValidConstantSpace(self, s: str) -> str:
        # Convert to a mutable list of chars:
        A = list(s)
        n = len(A)

        # PASS 1: remove invalid ')'
        write = 0  # where we write the next “kept” character
        open_count = 0  # how many '(' are currently un‑matched

        for read in range(n):
            c = A[read]
            if c == '(':
                open_count += 1
                A[write] = c
                write += 1
            elif c == ')':
                if open_count > 0:
                    open_count -= 1
                    A[write] = c
                    write += 1
                # else: skip this ')'
            else:
                # any lowercase letter
                A[write] = c
                write += 1

        # Now A[0:write] is the string with all "bad" ')' dropped.
        # open_count is how many '(' remain unmatched in that prefix.

        # PASS 2: remove the extra '(' from right-to-left
        # We'll fill the tail of A (from write-1 downward) with the final chars.
        write2 = write - 1
        for read in range(write - 1, -1, -1):
            c = A[read]
            if c == '(' and open_count > 0:
                # skip this unmatched '('
                open_count -= 1
            else:
                A[write2] = c
                write2 -= 1

        # The valid substring lives in A[write2+1 : write]
        return "".join(A[write2 + 1: write])

    def minRemoveToMakeValid(self, s: str) -> str:
        # map each closing → its opening
        match = {')': '(', ']': '[', '}': '{'}
        opens = set(match.values())

        stack = []  # will hold indices of opening brackets
        to_remove = set()  # indices of chars to delete

        # 1) Scan once and match up as much as we can
        for i, c in enumerate(s):
            if c in opens:
                stack.append(i)
            elif c in match:
                if stack and s[stack[-1]] == match[c]:
                    stack.pop()
                else:
                    # no matching opener
                    to_remove.add(i)

        # any leftover openers are unmatched
        to_remove.update(stack)

        # 2) Build the result skipping all to_remove
        return ''.join(
            c for i, c in enumerate(s)
            if i not in to_remove
        )




if __name__ == "__main__":
    s = "lee(t(c)o)de)"
    print(Solution().minRemoveToMakeValid(s))
    print(Solution().minRemoveToMakeValidConstantSpace(s))
    s = "a)b(c)d"
    print(Solution().minRemoveToMakeValid(s))
    print(Solution().minRemoveToMakeValidConstantSpace(s))
