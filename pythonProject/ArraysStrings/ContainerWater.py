from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            current_area = min(height[left], height[right]) * (right - left)
            max_area = max(max_area, current_area)
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1

        return max_area


if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(Solution().maxArea(height))
    height = [1, 1]
    print(Solution().maxArea(height))
    height = [8, 7, 2, 1]
    print(Solution().maxArea(height))
