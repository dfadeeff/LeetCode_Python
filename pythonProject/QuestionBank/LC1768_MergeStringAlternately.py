class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        p1, p2 = 0, 0
        str = ""
        while p1 < len(word1) and p2 < len(word2):
            str += word1[p1]
            p1 += 1
            str += word2[p2]
            p2 += 1

        str += word1[p1:]
        str += word2[p2:]

        return str


if __name__ == "__main__":
    word1 = "ab"
    word2 = "pqrs"
    print(Solution().mergeAlternately(word1, word2))