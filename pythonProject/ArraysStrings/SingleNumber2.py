from collections import defaultdict
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        hashmap = defaultdict(int)
        for i in nums:
           hashmap[i] += 1
        for k, v in hashmap.items():
            if v == 1:
                return k

        return -1


if __name__ == '__main__':
    nums = [2, 2, 3, 2]
    print(Solution().singleNumber(nums))
