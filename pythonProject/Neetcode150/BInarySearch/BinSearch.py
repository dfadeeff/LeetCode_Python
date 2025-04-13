from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

if __name__ == "__main__":
    nums = [-1, 0, 2, 4, 6, 8]
    target = 4
    print(Solution().search(nums, target))
    nums = [-1, 0, 2, 4, 6, 8]
    target = 3
    print(Solution().search(nums, target))
