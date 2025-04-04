from collections import defaultdict


class Solution:
    def isOneEditDistance(self, s: str, t: str) -> bool:
        if len(s) > len(t):
            s, t = t, s
        if len(t) - len(s) > 1:
            return False
        for i in range(len(s)):
            if s[i] != t[i]:
                if len(s) == len(t):
                    return s[i+1:] == t[i+1:]  # replace
                else:
                    return s[i:] == t[i+1:]  # insert
        return len(s) + 1 == len(t)


if __name__ == '__main__':
    s = "ab"
    t = "acb"
    print(Solution().isOneEditDistance(s, t))
    s = ""
    t = ""
    print(Solution().isOneEditDistance(s, t))
    s = "c"
    t = "c"
    print(Solution().isOneEditDistance(s, t))
