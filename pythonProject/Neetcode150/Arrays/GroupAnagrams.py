from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        def getKey(word):
            hashMapIndex = defaultdict(int)
            for char in word:
                hashMapIndex[char] += 1
            return tuple(sorted(hashMapIndex.items()))

        grouped = defaultdict(list)
        for i in strs:
            key = getKey(i)
            grouped[key].append(i)
        print(grouped)
        return list(grouped.values())


if __name__ == '__main__':
    strs = ["act", "pots", "tops", "cat", "stop", "hat"]
    print(Solution().groupAnagrams(strs))
