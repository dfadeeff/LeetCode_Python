from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, maxArea = 0, 0
        right = len(height) - 1

        while left < right:
            width = right - left
            maxArea = max(maxArea, min(height[left], height[right]) * width)

            if height[left] <= height[right]:
                left += 1

            else:
                right -= 1

        return maxArea


if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(Solution().maxArea(height))
