from typing import List
from collections import defaultdict

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1

        for k,v in freq.items():
            if v > 1:
                return True

        return False


if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    print(Solution().containsDuplicate(nums))
    nums = [1, 2, 3, 4]
    print(Solution().containsDuplicate(nums))
