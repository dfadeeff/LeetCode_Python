from typing import List

from black.trans import defaultdict


class Solution:
    def largestUniqueNumber(self, nums: List[int]) -> int:
        hashmap = defaultdict(int)
        for num in nums:
            hashmap[num] += 1

        answer = -1
        for k, v in hashmap.items():
            if v == 1:
                answer = max(answer, k)

        return answer


if __name__ == '__main__':
    nums = [5, 7, 3, 9, 4, 9, 8, 3, 1]
    print(Solution().largestUniqueNumber(nums))
    nums = [9, 9, 8, 8]
    print(Solution().largestUniqueNumber(nums))
