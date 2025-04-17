from typing import List


class Solution:
    def sortArrayByParity(self, nums: List[int]) -> List[int]:
        left = 0
        for right in range(len(nums)):
            if nums[right] % 2 == 0:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1

        return nums


if __name__ == "__main__":
    nums = [3, 1, 2, 4]
    print(Solution().sortArrayByParity(nums))
