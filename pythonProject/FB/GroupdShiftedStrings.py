from collections import defaultdict
from typing import List


class Solution:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        def get_key(s):
            if len(s) == 1:
                return ()
            return tuple((ord(s[i + 1]) - ord(s[i])) % 26 for i in range(len(s) - 1))

        groups = defaultdict(list)

        for word in strings:
            key = get_key(word)
            groups[key].append(word)
        print(groups)
        return list(groups.values())


if __name__ == '__main__':
    strings = ["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]
    print(Solution().groupStrings(strings))
