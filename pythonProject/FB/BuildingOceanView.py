from typing import List


class Solution:
    def findBuildings(self, heights: List[int]) -> List[int]:
        result = []

        maxSoFar = float('-inf')
        for i in range(len(heights) - 1, -1, -1):
            if heights[i] > maxSoFar:
                result.append(i)
                maxSoFar = heights[i]
        return result[::-1]


if __name__ == '__main__':
    heights = [4, 2, 3, 1]
    print(Solution().findBuildings(heights))
    heights = [4, 3, 2, 1]
    print(Solution().findBuildings(heights))
    heights = [1, 3, 2, 4]
    print(Solution().findBuildings(heights))
