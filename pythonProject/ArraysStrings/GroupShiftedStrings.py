from typing import List

from black.trans import defaultdict


class Solution:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        def get_key(s):
            """generates a “signature” for a string s that captures how each letter is shifting to the next — and wraps around the alphabet using modulo 26.
            ord('a') = 97
            ord('b') = 98
            ord('c') = 99
            ord('z') = 122
            """
            if len(s) == 1:
                return ()
            return tuple((ord(s[i + 1]) - ord(s[i])) % 26 for i in range(len(s) - 1))

        groups = defaultdict(list)

        for word in strings:
            key = get_key(word)
            print(key)
            groups[key].append(word)
        print(groups)
        return list(groups.values())


if __name__ == '__main__':
    strings = ["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]
    print(Solution().groupStrings(strings))
