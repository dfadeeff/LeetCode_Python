from typing import List


class Solution:
    def minFallingPathSum(self, matrix: List[List[int]]) -> int:
        rows = len(matrix)
        cols = len(matrix[0])

        dp = [[float('inf')] * cols for _ in range(rows)]

        for j in range(0, cols):
            dp[0][j] = matrix[0][j]

        for i in range(1, rows):
            for j in range(0, cols):
                if j == 0 :
                    dp[i][j] = min(dp[i - 1][j], dp[i - 1][j + 1]) + matrix[i][j]
                elif j == cols - 1:
                    dp[i][j] = min(dp[i - 1][j], dp[i - 1][j - 1]) + matrix[i][j]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i - 1][j - 1], dp[i - 1][j + 1]) + matrix[i][j]
        # for i in range(0, rows):
        #     print(dp[i])

        return min(dp[rows - 1])


def main():
    matrix = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
    print(Solution().minFallingPathSum(matrix))


if __name__ == '__main__':
    main()
