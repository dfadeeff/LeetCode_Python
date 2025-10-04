from typing import List


class Solution:
    def waysToSplitArray(self, nums: List[int]) -> int:
        prefix = [nums[0]]
        for i in range(1, len(nums)):
            prefix.append(nums[i] + prefix[i - 1])


        ans = 0
        n = len(nums)
        for i in range(n - 1):
            left_section = prefix[i]
            right_section = prefix[n - 1] - prefix[i]
            if left_section >= right_section:
                ans += 1

        return ans


if __name__ == "__main__":
    nums = [10, 4, -8, 7]
    print(Solution().waysToSplitArray(nums))
