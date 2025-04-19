from typing import List
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        [1, 0 ,2 , 3 ,5, 0 ]
        [1,2 , 3 ,5, 0, 0 ]
        """
        left = 0
        for right in range(len(nums)):
            if nums[right] != 0:

                nums[left], nums[right] = nums[right], nums[left]
                left += 1
if __name__ == "__main__":
    nums = [0, 1, 0, 3, 12]
    print(Solution().moveZeroes(nums))


