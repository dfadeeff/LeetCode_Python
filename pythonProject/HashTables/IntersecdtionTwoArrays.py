from typing import List


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        set1 = set()
        for i in nums1:
            set1.add(i)
        set2 = set()
        for i in nums2:
            set2.add(i)

        answer = []
        for i in set1:
            if i in set2:
                answer.append(i)
        return answer


if __name__ == '__main__':
    nums1 = [1, 2, 2, 1]
    nums2 = [2, 2]
    print(Solution().intersection(nums1, nums2))
