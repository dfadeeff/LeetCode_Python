from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        final_array = []
        i, j = 0, 0
        while i < m and j < n:
            if nums1[i] < nums2[j]:
                final_array.append(nums1[i])
                i += 1
            else:
                final_array.append(nums2[j])
                j += 1

        final_array.extend(nums1[i:m])
        final_array.extend(nums2[j:n])

        nums1[:] = final_array
        print(nums1)

    def mergeConstantSpace(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # last index of nums1
        last = m + n - 1  # third pointer

        # merge in reverse order
        while m > 0 and n > 0:
            if nums1[m - 1] > nums2[n - 1]:
                nums1[last] = nums1[m - 1]
                m -= 1
            else:
                nums1[last] = nums2[n - 1]
                n -= 1
            last -= 1

        # edge case, fill with left over
        while n > 0:
            nums1[last] = nums2[n - 1]
            n -= 1
            last -= 1
        print(nums1)


if __name__ == "__main__":
    nums1 = [1, 2, 3, 0, 0, 0]
    m = 3
    nums2 = [2, 5, 6]
    n = 3
    print(Solution().merge(nums1, m, nums2, n))
    print(Solution().mergeConstantSpace(nums1, m, nums2, n))
