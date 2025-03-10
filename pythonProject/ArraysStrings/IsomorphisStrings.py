from black.trans import defaultdict


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        hashmapS = defaultdict(list)
        for i, number in enumerate(s):
            hashmapS[number].append(i)

        hashmapT = defaultdict(list)
        for i, number in enumerate(t):
            hashmapT[number].append(i)

        if len(hashmapS) != len(hashmapT):
            return False

        if len(hashmapS) == len(hashmapT):

            if sorted(hashmapS.values()) == sorted(hashmapT.values()):
                return True

        return False


if __name__ == '__main__':
    s = "egg"
    t = "add"
    print(Solution().isIsomorphic(s, t))
    s = "foo"
    t = "bar"
    print(Solution().isIsomorphic(s, t))
    s = "bbbaaaba"
    t = "aaabbbba"
    print(Solution().isIsomorphic(s, t))
