class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:

        i, j = 0,0
        w1 = list(word1)
        w2 = list(word2)
        final_array = []
        while i < len(w1) and j < len(w2):
            final_array.append(w1[i])
            i += 1
            final_array.append(w2[j])
            j += 1


        final_array.extend(w1[i:])
        final_array.extend(w2[j:])

        return "".join(final_array)


if __name__ == "__main__":
    word1 = "abc"
    word2 = "pqr"
    print(Solution().mergeAlternately(word1, word2))
    word1 = "ab"
    word2 = "pqrs"
    print(Solution().mergeAlternately(word1, word2))
    word1 = "abcd"
    word2 = "pq"
    print(Solution().mergeAlternately(word1, word2))
