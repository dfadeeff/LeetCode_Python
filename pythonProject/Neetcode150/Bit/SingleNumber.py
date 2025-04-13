from collections import defaultdict
from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1
        for k, v in freq.items():
            if v == 1:
                return k
        return -1


if __name__ == '__main__':
    nums = [3, 2, 3]
    print(Solution().singleNumber(nums))
