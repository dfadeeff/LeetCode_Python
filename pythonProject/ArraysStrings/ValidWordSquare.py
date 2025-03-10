from typing import List


class Solution:
    def validWordSquare(self, words: List[str]) -> bool:
        for i in range(len(words)):
            for j in range(len(words[i])):
                # Check boundaries and character match
                if j >= len(words) or i >= len(words[j]) or words[i][j] != words[j][i]:
                    return False
        return True


if __name__ == "__main__":
    words = ["abcd", "bnrt", "crmy", "dtye"]
    print(Solution().validWordSquare(words))
