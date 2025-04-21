from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:

        left = self.binarySearchLeft(nums, target)
        right = self.binarySearchRight(nums, target)
        return right - left + 1

    def binarySearchLeft(self, nums: List[int], target: int):
        l, r = 0, len(nums) - 1
        index = -1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                index = mid
                r = mid - 1
            if target > nums[mid]:
                l = mid + 1
            elif target < nums[mid]:
                r = mid - 1

        return index

    def binarySearchRight(self, nums: List[int], target: int):
        l, r = 0, len(nums) - 1
        index = -1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                index = mid
                l = mid + 1
            if target > nums[mid]:
                l = mid + 1
            elif target < nums[mid]:
                r = mid - 1

        return index


if __name__ == "__main__":
    nums = [5, 7, 7, 8, 8, 10]
    target = 8
    print(Solution().searchRange(nums, target))
