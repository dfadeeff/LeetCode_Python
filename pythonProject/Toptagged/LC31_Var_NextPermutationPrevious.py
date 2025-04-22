from typing import List


class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        # 1) find the pivot
        for i in range(n - 1, 0, -1):
            if nums[i] < nums[i - 1]:
                break
        else:
            # no pivot found
            nums.reverse()
            return

        # 2) find the rightmost successor to pivot in the suffix
        for j in range(n - 1, i - 1, -1):  # from n-1 to i
            if nums[j] < nums[i - 1]:  # i is constant here
                nums[i - 1], nums[j] = nums[j], nums[i - 1]
                break
        # 3) reverse the suffix
        nums[i:] = reversed(nums[i:])


if __name__ == "__main__":
    nums = [9, 4, 8, 3, 5, 5, 8, 9]
    print(Solution().nextPermutation(nums))
    print(nums)  # outputs [1, 2, 3]
    nums = [9, 6, 5, 4, 3, 2]
    print(Solution().nextPermutation(nums))
    print(nums)
