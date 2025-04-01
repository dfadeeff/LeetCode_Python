from typing import List


class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        total_sum = sum(nums)

        # Standard Kadane's for max subarray sum (non-circular)
        curr_max = max_sum = nums[0]
        for num in nums[1:]:
            curr_max = max(num, curr_max + num)
            max_sum = max(max_sum, curr_max)

        # Kadane's for min subarray sum (to handle wrap-around)
        curr_min = min_sum = nums[0]
        for num in nums[1:]:
            curr_min = min(num, curr_min + num)
            min_sum = min(min_sum, curr_min)

        # If all numbers are negative, total_sum == min_sum
        # So wrapping is not allowed, return max_sum only
        if max_sum < 0:
            return max_sum

        return max(max_sum, total_sum - min_sum)


if __name__ == "__main__":
    nums = [1, -2, 3, -2]
    print(Solution().maxSubarraySumCircular(nums))
    nums = [5, -3, 5]
    print(Solution().maxSubarraySumCircular(nums))
