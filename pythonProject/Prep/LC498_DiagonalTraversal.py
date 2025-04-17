from typing import List


class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        if not mat or not mat[0]:
            return []

        m, n = len(mat), len(mat[0])
        result = []
        for d in range(m + n - 1):
            if d % 2 == 0:
                # Traverse from bottom to top
                row = d if d < m else m - 1
                col = 0 if d < m else d - (m - 1)
                while row >= 0 and col < n:
                    result.append(mat[row][col])
                    row -= 1
                    col += 1
            else:
                # Traverse from top to bottom
                col = d if d < n else n - 1
                row = 0 if d < n else d - (n - 1)
                while col >= 0 and row < m:
                    result.append(mat[row][col])
                    row += 1
                    col -= 1

        return result




if __name__ == '__main__':
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(Solution().findDiagonalOrder(mat))
