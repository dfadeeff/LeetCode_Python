from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        """binary search
        Questions to ask
        1) Does each value in the vector only have unique values neighboring?
        2) Are we given at least 1 element?
        3) Are there multiple peaks?
        4) Are we guaranteed to have at least 1 peak ?
        5) Edges are inf infinity ?


        """

        l = 0
        r = len(nums) - 1
        while l <= r:
            mid = (l + r) // 2
            if (mid == len(nums) - 1) or (nums[mid] > nums[mid + 1]) and (nums[mid] > nums[mid-1] or mid==0):
                return mid
            if nums[mid+1] > nums[mid]:
                l = mid + 1
            else:
                r = mid - 1


if __name__ == "__main__":
    nums = [1, 2, 1, 3, 5, 6, 4]
    print(Solution().findPeakElement(nums))
