from typing import List

from collections import defaultdict


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        Counting sort
        """
        freq = defaultdict(int)
        for i in nums:
            freq[i] += 1

        i = 0
        for color in range(3):
            for _ in range(freq[color]):
                nums[i] = color
                i += 1

    def partionColors(self, nums):
        """Dutch flag implementation"""
        lo, mid = 0, 0
        hi = len(nums) - 1
        while mid <= hi:
            if nums[mid] == 0:
                nums[lo], nums[mid] = nums[mid], nums[lo]
                lo += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[hi] = nums[hi], nums[mid]
                hi -= 1

        return nums


if __name__ == "__main__":
    solution = Solution()
    nums = [1, 0, 1, 2]
    print(solution.sortColors(nums))
    print(solution.partionColors(nums))
