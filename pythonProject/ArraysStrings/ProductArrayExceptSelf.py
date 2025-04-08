from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = [0] * len(nums)
        zero_count = nums.count(0)

        # Case 1: More than 1 zero ➔ all zeros
        if zero_count > 1:
            return result

        # Case 2: Exactly one zero
        if zero_count == 1:
            prod = 1
            for num in nums:
                if num != 0:
                    prod *= num
            for i in range(len(nums)):
                if nums[i] == 0:
                    result[i] = prod
                else:
                    result[i] = 0
            return result

        # Case 3: No zeros
        prod = 1
        for num in nums:
            prod *= num
        for i in range(len(nums)):
            result[i] = prod // nums[i]
        return result


if __name__ == "__main__":
    nums = [-1, 1, 0, -3, 3]
    print(Solution().productExceptSelf(nums))
    nums = [1, 2, 3, 4]
    print(Solution().productExceptSelf(nums))
    nums = [0,0]
    print(Solution().productExceptSelf(nums))
    nums = [0, 4, 0]
    print(Solution().productExceptSelf(nums))
