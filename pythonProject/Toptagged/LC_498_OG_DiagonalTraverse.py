from typing import List


class Solution:
    def findDiagonalOrderV1(self, mat: List[List[int]]) -> List[int]:

        """“bucket-by-diagonal” trick

        T: O(mn)
        S: O(mn)

        """
        num_rows, num_cols = len(mat), len(mat[0])
        # Make one list for each diagonal index = i+j
        # you need buckets for every integer from 0 up to m+n-2, inclusive.
        # The smallest possible sum, i, j : 0+0=0
        # the largest is i,j, n-1, m-1 = n-1 + m-1 = n+m - 2 inclusive, so from 0 to (n+m-2) - 0 + 1 = n + m - 1
        # bucket for all diagonals: 0,1,2, ... m+n-2 which guarantees a valid slot for every cell
        diagonals = [[] for _ in range(num_rows + num_cols - 1)]

        for i in range(num_rows):
            for j in range(num_cols):
                diagonals[i + j].append(mat[i][j])
        print("diagonals", diagonals)

        res = diagonals[0]
        for x in range(1, len(diagonals)):
            if x % 2 == 1:
                res.extend(diagonals[x])
            else:
                res.extend(diagonals[x][::-1])

        return res

    def findDiagonalOrderV2(self, mat: List[List[int]]) -> List[int]:
        """

        :param mat:
        :return:

        T: O(mn)
        S: O(1)
        Every element (i,j) in the matrix lies on exactly one “anti-diagonal” labeled by the sum d = i + j.
        There are m+n-1 such diagonals, with d ranging from 0 up to (m-1)+(n-1).
        By simply iterating d from 0 to m+n-2, and for each diagonal walking exactly its cells in the correct order (either bottom-to-top or top-to-bottom)
        we can append all m\times n entries in one pass, using only a couple of index variables.

        """
        if not mat or not mat[0]:
            return []

        rows, cols = len(mat), len(mat[0])
        result = []
        for d in range(rows + cols - 1):
            """
            even go bottom up
            odd go top bottom
            """
            if d % 2 == 0:
                # Traverse from bottom to top, Even d: traverse bottom→top (decreasing row, increasing col).
                row = d if d < rows else rows - 1
                col = 0 if d < rows else d - (rows - 1)
                while row >= 0 and col < cols:
                    # 	Walk up one row and right one column each iteration, until you leave the matrix.
                    result.append(mat[row][col])
                    row -= 1
                    col += 1
            else:
                # Traverse from top to bottom, odd d: traverse top→bottom (increasing row, decreasing col).
                col = d if d < cols else cols - 1
                row = 0 if d < cols else d - (cols - 1)
                while col >= 0 and row < rows:
                    result.append(mat[row][col])
                    row += 1
                    col -= 1

        return result


if __name__ == "__main__":
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(Solution().findDiagonalOrderV1(mat))
    print(Solution().findDiagonalOrderV2(mat))
    mat = [[1, 2], [3, 4]]
    print(Solution().findDiagonalOrderV1(mat))
    print(Solution().findDiagonalOrderV2(mat))
