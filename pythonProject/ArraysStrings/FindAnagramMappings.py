from typing import List

from black.trans import defaultdict


class Solution:
    def anagramMappings(self, nums1: List[int], nums2: List[int]) -> List[int]:
        hashmap2 = {number: index for index, number in enumerate(nums2)}

        list_answer = []
        for i in nums1:
            list_answer.append(hashmap2.get(i))

        return list_answer


if __name__ == '__main__':
    nums1 = [12, 28, 46, 32, 50]
    nums2 = [50, 12, 32, 46, 28]
    print(Solution().anagramMappings(nums1, nums2))
