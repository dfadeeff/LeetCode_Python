from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)

        closest_sum = float("inf")

        for i in range(n):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                curSum = nums[i] + nums[lo] + nums[hi]
                if abs(curSum - target) < abs(closest_sum - target):
                    closest_sum = curSum
                if curSum == target:
                    return curSum
                elif curSum < target:
                    lo += 1
                else:
                    hi -= 1
        return closest_sum


if __name__ == "__main__":
    nums = [-1, 2, 1, -4]
    target = 1
    print(Solution().threeSumClosest(nums, target))
