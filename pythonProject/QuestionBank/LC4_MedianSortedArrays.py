from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        i, j = 0, 0
        result = []

        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                result.append(nums1[i])
                i += 1
            else:
                result.append(nums2[j])
                j += 1
        # Append any remaining elements
        result.extend(nums1[i:])
        result.extend(nums2[j:])


        if len(result) % 2 != 0:
            median_index = len(result) // 2
            median = result[median_index]
        else:
            temp = len(result) // 2
            median = (result[temp] + result[temp - 1]) / 2
        return median


if __name__ == '__main__':
    nums1 = [1, 3]
    nums2 = [2]
    print(Solution().findMedianSortedArrays(nums1, nums2))
    nums1 = [1, 2]
    nums2 = [3, 4]
    print(Solution().findMedianSortedArrays(nums1, nums2))
