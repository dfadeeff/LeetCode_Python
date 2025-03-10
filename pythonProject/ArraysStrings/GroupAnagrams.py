from typing import List

from black.trans import defaultdict


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
            print(key)
            grouped[key].append(i)

        return list(grouped.values())


if __name__ == '__main__':
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(Solution().groupAnagrams(strs))

    strs = [""]
    print(Solution().groupAnagrams(strs))

    strs = ["a"]
    print(Solution().groupAnagrams(strs))

    strs = ["ddddddddddg","dgggggggggg"]
    print(Solution().groupAnagrams(strs))


