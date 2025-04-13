from collections import defaultdict


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        hashmapS = defaultdict(int)
        hashmapT = defaultdict(int)
        for char in s:
            hashmapS[char] += 1
        for char in t:
            hashmapT[char] += 1

        for k,v in hashmapT.items():
            if len(hashmapS != hashmapT):
                return False
            if k not in hashmapS:
                return False
            else:
                if hashmapS[k] != hashmapT[k]:
                    return False
        return True


if __name__ == '__main__':
    s = "racecar"
    t = "carrace"
    print(Solution().isAnagram(s, t))
    s = "jar"
    t = "jam"
    print(Solution().isAnagram(s, t))
