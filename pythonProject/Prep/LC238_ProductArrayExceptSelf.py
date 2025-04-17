from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        from_left = [1] * len(nums)
        from_right = [1] * len(nums)

        for i in range(1, len(nums)):
            from_left[i] = nums[i - 1] * from_left[i - 1]

        for i in range(len(nums) - 2, -1, -1):
            from_right[i] = nums[i + 1] * from_right[i + 1]

        for i in range(len(from_left)):
            from_left[i] = from_left[i] * from_right[i]
        return from_left

    def productExceptSelfOptimsed(self, nums: List[int]) -> List[int]:
        from_left = [1] * len(nums)

        for i in range(1, len(nums)):
            from_left[i] = nums[i - 1] * from_left[i - 1]

        right = 1
        for i in reversed(range(len(nums))):
            from_left[i] = from_left[i] * right
            right *= nums[i]
        return from_left


if __name__ == "__main__":
    nums = [1, 2, 3, 4]
    print(Solution().productExceptSelf(nums))
    print(Solution().productExceptSelfOptimsed(nums))
