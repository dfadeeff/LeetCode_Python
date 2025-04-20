from typing import List


class Solution:
    def merge(self, nums1: List[int], nums2: List[int]) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # last index nums1
        n = len(nums2)
        m = len(nums1) - n  # this is important
        last = m + n - 1

        # merge in reverse order
        while m > 0 and n > 0:
            if nums1[m - 1] > nums2[n - 1]:
                nums1[last] = nums1[m - 1]
                m -= 1
            else:
                nums1[last] = nums2[n - 1]
                n -= 1
            last -= 1

        # fill nums1 with leftover nums2 elements
        while n > 0:
            nums1[last] = nums2[n - 1]
            n, last = n - 1, last - 1


if __name__ == "__main__":
    nums1 = [1, 8, 0, 0]
    nums2 = [3, 5]
    Solution().merge(nums1, nums2)
    print(nums1)  # → [1,3,5,8]
    nums1 = [2, 4, 6, 0, 0, 0]  # m=3, n=3
    nums2 = [1, 3, 5]
    Solution().merge(nums1, nums2)
    print(nums1)  # → [1,2,3,4,5,6]
