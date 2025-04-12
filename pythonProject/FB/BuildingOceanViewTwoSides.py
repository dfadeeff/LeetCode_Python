from typing import List


class Solution:
    def findBuildings(self, heights: List[int]) -> List[int]:
        """right and left side views"""
        n = len(heights)
        if n == 1:
            return [0]
        left = 0
        right = n - 1
        left_view = []
        right_view = []
        left_view.append(left)
        right_view.append(right)

        left_max = heights[left]
        right_max = heights[right]

        while left < right:
            if left_max < right_max:
                left += 1
                if heights[left] > left_max & left < right:
                    left_view.append(left)
                    left_max = heights[left]
            else:
                right -= 1
                if heights[right] > right_max & left < right:
                    right_view.append(right)
                    right_max = heights[right]
        left_view.extend(right_view[::-1])
        left_view = list(set(left_view))
        return left_view


if __name__ == '__main__':
    heights = [2, 5, 3, 10, 9, 8]
    print(Solution().findBuildings(heights))
    heights = [2]
    print(Solution().findBuildings(heights))
