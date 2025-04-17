from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        max_area = float("-inf")
        left, right = 0, len(height) - 1
        for i in range(len(height)):
            current_area = (right - left) * min(height[left], height[right])
            max_area = max(max_area, current_area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area


if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(Solution().maxArea(height))
