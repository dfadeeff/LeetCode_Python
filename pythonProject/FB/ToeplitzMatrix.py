from typing import List


class Solution:
    def isToeplitzMatrix(self, matrix: List[List[int]]) -> bool:
        groups = {}
        for r, row in enumerate(matrix):

            for c, val in enumerate(row):
                if r - c not in groups:
                    groups[r - c] = val
                elif groups[r - c] != val:
                    return False
        print(groups)

        return True


if __name__ == "__main__":
    matrix = [[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]]
    print(Solution().isToeplitzMatrix(matrix))
