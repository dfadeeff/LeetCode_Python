from typing import List


class Solution:
    def findBuildingsBruteForce(self, heights: List[int]) -> List[int]:
        result = []
        for i in range(len(heights) - 1):
            current_height = heights[i]
            current_max_subarray = max(heights[i + 1:])
            if current_height > current_max_subarray:
                result.append(i)
        result.append(len(heights) - 1)
        return result


    def findBuildings(self, heights: List[int]) -> List[int]:
        result = []
        max_height = 0  # assume no buildings beyond

        for i in reversed(range(len(heights))):
            if heights[i] > max_height:
                result.append(i)
                max_height = heights[i]

        return result[::-1]  # reverse to return increasing order





if __name__ == '__main__':
    heights = [4, 2, 3, 1]
    print(Solution().findBuildingsBruteForce(heights))
    print(Solution().findBuildings(heights))
