from typing import List


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        # node: a cell (r, c)
        # neighbors: 4 adjacent cells that have the same color as the starting cell
        # on visit: paint the cell to the new color

        rows, cols = len(image), len(image[0])
        #print("rows: ", rows, "cols: ", cols)
        source = image[sr][sc]

        if source == color:  # edge case: nothing to do
            return image

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if image[r][c] != source:
                return
            image[r][c] = color  # mark visited (painting IS the mark)

            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        dfs(sr, sc)
        return image


if __name__ == "__main__":
    sol = Solution()
    image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    sr = 1
    sc = 1
    color = 2
    print(sol.floodFill(image, sr, sc, color))
