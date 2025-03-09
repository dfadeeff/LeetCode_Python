from collections import defaultdict


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        char_count_randomNote = defaultdict(int)
        for char in ransomNote:
            char_count_randomNote[char] += 1

        char_count_magazin = defaultdict(int)
        for char in magazine:
            char_count_magazin[char] += 1

        for k, v in char_count_randomNote.items():
            if k not in char_count_magazin.keys():
                return False
            if char_count_randomNote[k] > char_count_magazin[k]:
                return False

        return True


if __name__ == '__main__':
    ransomNote = "a"
    magazine = "b"
    print(Solution().canConstruct(ransomNote, magazine))
    ransomNote = "aa"
    magazine = "ab"
    print(Solution().canConstruct(ransomNote, magazine))
    ransomNote = "aa"
    magazine = "aab"
    print(Solution().canConstruct(ransomNote, magazine))
