from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def binary_searchLeft(arr, target):
            left = 0
            right = len(arr)
            while left < right:
                mid = (left + right) // 2
                if arr[mid] >= target:
                    right = mid
                else:
                    left = mid + 1

            return left if target in nums else -1

        def binary_searchRight(arr, target):
            left = 0
            right = len(arr)
            while left < right:
                mid = (left + right) // 2
                if arr[mid] > target:
                    right = mid
                else:
                    left = mid + 1

            return left - 1 if target in nums else -1

        ans = []
        left = binary_searchLeft(nums, target)
        right = binary_searchRight(nums, target)
        ans.append(left)
        ans.append(right)

        return ans


if __name__ == "__main__":
    nums = [5, 7, 7, 8, 8, 10]
    target = 8
    print(Solution().searchRange(nums, target))
    nums = [5, 7, 7, 8, 8, 10]
    target = 6
    print(Solution().searchRange(nums, target))
