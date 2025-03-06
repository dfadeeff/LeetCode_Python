from typing import List


class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        left = 0
        for right in range(1,len(nums)):
            if left % 2 == 0 and right % 2 !=0 and nums[left] > nums[right]:
                nums[left], nums[right] = nums[right], nums[left]
            elif left % 2 != 0 and right % 2 == 0 and nums[left] < nums[right]:
                nums[left], nums[right] = nums[right], nums[left]
            left += 1

        print(nums)


if __name__ == '__main__':
    nums = [3, 5, 2, 1, 6, 4]
    print(Solution().wiggleSort(nums))

