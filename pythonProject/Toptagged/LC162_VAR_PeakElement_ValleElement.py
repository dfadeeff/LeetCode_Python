from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2
            # THINK OF SMALLER NEIGHBORS!!!

            # 1) you are on the uphill, so move left, think of smaller element from left
            if mid >0 and nums[mid] > nums[mid - 1]:
                r = mid - 1

            # 2) there is a smaller element or neighbor from right, move right
            elif mid < len(nums)-1 and nums[mid] > nums[mid + 1]:
                l = mid + 1

            # 3) Otherwise, neither neighbor is higher → we found a peak!
            else:
                return mid
        return -1


if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    print(Solution().findPeakElement(nums))
