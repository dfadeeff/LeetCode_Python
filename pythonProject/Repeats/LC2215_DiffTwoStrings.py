from collections import defaultdict
from typing import List


class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        hash1 = defaultdict(int)
        for i in nums1:
            hash1[i] += 1

        hash2 = defaultdict(int)
        for i in nums2:
            hash2[i] += 1

        intersection = []
        for k in hash1.keys():
            if k in hash2:
                intersection.append(k)

        list1 = []
        list2 = []
        for k in hash1.keys():
            if k not in intersection:
                list1.append(k)

        for k in hash2.keys():
            if k not in intersection:
                list2.append(k)

        return [list1, list2]


if __name__ == "__main__":
    nums1 = [1, 2, 3]
    nums2 = [2, 4, 6]
    print(Solution().findDifference(nums1, nums2))
    nums1 = [1, 2, 3, 3]
    nums2 = [1, 1, 2, 2]
    print(Solution().findDifference(nums1, nums2))
