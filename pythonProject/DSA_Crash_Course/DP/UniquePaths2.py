from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])


        if obstacleGrid[0][0] == 1:
            return 0

        obstacleGrid[0][0] = 1
        for i in range(1, m):
            if obstacleGrid[i][0] == 0 and obstacleGrid[i - 1][0] == 1:
                obstacleGrid[i][0] = 1
            else:
                obstacleGrid[i][0] = 0

        for i in range(1, n):
            if obstacleGrid[0][i] == 0 and obstacleGrid[0][i - 1] == 1:
                obstacleGrid[0][i] = 1
            else:
                obstacleGrid[0][i] = 0

        # start from rows
        for i in range(1, m ):
            # go through cols
            for j in range(1, n ):
                if obstacleGrid[i][j] == 0:
                    obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1]
                else:
                    obstacleGrid[i][j] = 0

        for i in range(0, m ):
            print(obstacleGrid[i])
        return obstacleGrid[m-1][n-1]


def main():
    obstacleGrid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print(Solution().uniquePathsWithObstacles(obstacleGrid))
    obstacleGrid = [[0, 1], [0, 0]]
    print(Solution().uniquePathsWithObstacles(obstacleGrid))
    obstacleGrid = [[1, 0]]
    print(Solution().uniquePathsWithObstacles(obstacleGrid))


if __name__ == '__main__':
    main()
