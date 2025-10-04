from typing import List


class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        left1, left2 = 0, 0

        while left1 < len(nums1) and left2 < len(nums2):
            if nums1[left1] == nums2[left2]:
                return nums1[left1]

            if nums1[left1] < nums2[left2]:
                left1 += 1
            else:
                left2 += 1
        return -1


if __name__ == "__main__":
    nums1 = [1, 2, 3]
    nums2 = [2, 4]
    print(Solution().getCommon(nums1, nums2))
    nums1 = [1000000000, 1000000000]
    nums2 = [1000000000]
    print(Solution().getCommon(nums1, nums2))
