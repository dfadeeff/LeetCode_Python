from typing import List


class Solution:
    def findBuildings(self, heights: List[int]) -> List[int]:

        maxSoFar = float('-inf')
        result = []
        for i in range(len(heights) - 1, -1, -1):
            if heights[i] > maxSoFar:
                maxSoFar = max(maxSoFar, heights[i])
                result.append(i)

        return result[::-1]


if __name__ == "__main__":
    heights = [4, 2, 3, 1]
    print(Solution().findBuildings(heights))
