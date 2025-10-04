from typing import List


class Solution:
    def minStartValue(self, nums: List[int]) -> int:
        min_val = 0
        total = 0

        # Iterate over the array and get the minimum step-by-step total.
        for num in nums:
            total += num
            min_val = min(min_val, total)

        # We have to change the minimum step-by-step total to 1,
        # by increasing the startValue from 0 to -min_val + 1,
        # which is just the minimum startValue we want.
        return -min_val + 1


if __name__ == "__main__":
    nums = [-3, 2, -3, 4, 2]
    print(Solution().minStartValue(nums))
