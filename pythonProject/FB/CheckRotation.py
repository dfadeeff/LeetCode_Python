from typing import List


class Solution:
    def check(self, nums: List[int]) -> bool:
        """need to count drops."""
        count_drops = 0
        n = len(nums)
        for i in range(n):
            # Use modulo % n to compare last element to the first.
            if nums[i] > nums[(i + 1) % n]:
                count_drops += 1
        return count_drops <= 1


if __name__ == "__main__":
    nums = [3, 4, 5, 1, 2]
    print(Solution().check(nums))
    nums = [2, 1, 3, 4]
    print(Solution().check(nums))
