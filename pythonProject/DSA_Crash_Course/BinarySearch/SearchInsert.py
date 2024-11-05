from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if target == nums[mid]:
                return mid
            if target < nums[mid]:
                right = mid - 1
            if target > nums[mid]:
                left = mid + 1

        return left


def main():
    nums = [1, 3, 5, 6]
    target = 5
    print(Solution().searchInsert(nums, target))
    nums = [1, 3, 5, 6]
    target = 2
    print(Solution().searchInsert(nums, target))
    nums = [1, 3, 5, 6]
    target = 7
    print(Solution().searchInsert(nums, target))


if __name__ == '__main__':
    main()
