import collections
from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        counter = collections.Counter(nums)
        for k, v in counter.items():
            if v > 1:
                return True
        return False

if __name__ == "__main__":
    nums = [1, 2, 3, 3]
    print(Solution().hasDuplicate(nums))
    nums = [1, 2, 3, 4]
    print(Solution().hasDuplicate(nums))