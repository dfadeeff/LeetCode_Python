from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 1
        for i in range(1,len(nums)):
            if nums[i] != nums[i-1]:
                nums[k] = nums[i]
                k += 1
        return k


if __name__ == "__main__":
    nums = [1, 1, 2]
    print(Solution().removeDuplicates(nums))

