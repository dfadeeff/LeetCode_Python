class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i, j = 0,0
        while i < len(s) and j < len(j):
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == len(s)