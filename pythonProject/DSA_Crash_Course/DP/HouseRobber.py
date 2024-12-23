from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return nums[0]
        dp = [0] * (len(nums) + 1)

        dp[1] = nums[0]
        for i in range(2, len(dp)):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])

        return dp[-1]


def main():
    nums = [1, 2, 3, 1]
    print(Solution().rob(nums))
    nums = [2, 7, 9, 3, 1]
    print(Solution().rob(nums))


if __name__ == '__main__':
    main()
