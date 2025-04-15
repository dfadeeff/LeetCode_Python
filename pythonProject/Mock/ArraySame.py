from typing import List


class Solution:
    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        str1 = ""
        for char in word1:
            str1 += char
        #print(str1)

        str2 = ""
        for char in word2:
            str2 += char
        #print(str2)

        return str1 == str2


if __name__ == '__main__':
    word1 = ["ab", "c"]
    word2 = ["a", "bc"]
    print(Solution().arrayStringsAreEqual(word1, word2))
    word1 = ["a", "cb"]
    word2 = ["ab", "c"]
    print(Solution().arrayStringsAreEqual(word1, word2))


