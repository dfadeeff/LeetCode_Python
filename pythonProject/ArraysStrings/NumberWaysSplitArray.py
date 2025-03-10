from typing import List


class Solution:
    def waysToSplitArray(self, nums: List[int]) -> int:
        n = len(nums)
        prefix = [nums[0]]

        for i in range(1, n):
            prefix.append(prefix[i - 1] + nums[i])

        ans = 0
        for i in range(n - 1):
            left_section = prefix[i]
            right_section = prefix[-1] - prefix[i]
            if left_section >= right_section:
                ans += 1

        return ans


if __name__ == '__main__':
    nums = [10, 4, -8, 7]
    print(Solution().waysToSplitArray(nums))
    nums = [2, 3, 1, 0]
    print(Solution().waysToSplitArray(nums))
