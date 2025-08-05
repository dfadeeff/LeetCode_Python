class Solution:
    def maxDepth(self, s: str) -> int:
        res, current = 0,0
        for c in s:

            if c == "(":
                current += 1

            elif c == ")":
                current -= 1
            res = max(current,res)
        return res


if __name__ == "__main__":
    s = "(1+(2*3)+((8)/4))+1"
    print(Solution().maxDepth(s))