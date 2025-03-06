from typing import List


class Solution:
    def moveZeroesLeft(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        right = len(nums) - 1
        print(nums[-1])
        for left in range(len(nums) - 1, -1, -1):
            if nums[left] != 0:
                nums[left], nums[right] = nums[right], nums[left]
                right -= 1
        print(nums)

if __name__ == '__main__':
    nums = [0, 1, 0, 3, 12]
    print(Solution().moveZeroesLeft(nums))