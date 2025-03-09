from collections import defaultdict


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        hashmapS = defaultdict(int)
        hashmapT = defaultdict(int)
        for i in s:
            hashmapS[i] += 1
        for i in t:
            hashmapT[i] += 1

        if hashmapS == hashmapT:
            return True

        return False


if __name__ == '__main__':
    s = "anagram"
    t = "nagaram"
    print(Solution().isAnagram(s, t))
