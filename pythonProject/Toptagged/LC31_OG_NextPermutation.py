from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        # 1) find the pivot
        for i in range(n-2,-1,-1):
            if nums[i] < nums[i+1]:
                break
        else:
            # no pivot found
            nums.reverse()
            return

        # 2) find the rightmost successor to pivot in the suffix
        for j in range(n-1,i, -1): # from n-1 to i
            if nums[j] > nums[i]: # i is constant here
                nums[i], nums[j] = nums[j], nums[i]
                break
        # 3) reverse the suffix
        nums[i+1:] = reversed(nums[i+1:])


if __name__ == "__main__":
    nums = [3, 2, 1]
    print(Solution().nextPermutation(nums))
    print(nums)  # outputs [1, 2, 3]
    nums = [4, 3, 7, 5, 1, 1]
    print(Solution().nextPermutation(nums))
    print(nums)
