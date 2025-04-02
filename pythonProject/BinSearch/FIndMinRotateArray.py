from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        return min(nums)


if __name__ == "__main__":
    nums = [3, 4, 5, 1, 2]
    print(Solution().findMin(nums))
    nums = [4, 5, 6, 7, 0, 1, 2]
    print(Solution().findMin(nums))
    nums = [11, 13, 15, 17]
    print(Solution().findMin(nums))
