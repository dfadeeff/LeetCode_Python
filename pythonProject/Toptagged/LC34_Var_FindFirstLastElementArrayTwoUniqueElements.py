from typing import List


class Solution:
    def searchRange(self, nums: List[int]) -> int:
        if not nums:
            return 0

        def last_leq(target: int) -> int:
            l, r = 0, len(nums) - 1
            ans = -1
            while l <= r:
                mid = (l + r) // 2
                if nums[mid] <= target:
                    ans = mid  # mid is a candidate
                    l = mid + 1  # but maybe there’s a later one
                else:
                    r = mid - 1
            return ans

        count = 0
        start = 0

        # Each iteration skips all copies of one distinct value.
        while start < len(nums):
            end = last_leq(nums[start])
            count += 1
            start = end + 1

        return count


if __name__ == "__main__":
    nums = [5, 7, 7, 8, 8, 10]
    print(Solution().searchRange(nums))
