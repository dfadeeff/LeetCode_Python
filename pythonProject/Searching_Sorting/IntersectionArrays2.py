from collections import Counter
from typing import List


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = []
        hashMap1 = Counter(nums1)
        hashMap2 = Counter(nums2)
        print(hashMap1)
        print(hashMap2)

        for k, v in hashMap1.items():
            if k in hashMap2:
                min_freq = min(hashMap1[k], hashMap2[k])
                i = 1
                while i <= min_freq:
                    intersection.append(k)
                    i += 1

        return intersection

if __name__ == '__main__':
    nums1 = [1, 2, 2, 1]
    nums2 = [2, 2]
    print(Solution().intersect(nums1, nums2))

