from typing import List

from black.trans import defaultdict


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1

        max_value = float("-inf")

        for k, v in freq.items():
            max_value = max(max_value, v)
        for k, v in freq.items():
            if max_value == v:
                return k
        return -1


if __name__ == "__main__":
    nums = [5, 5, 1, 1, 1, 5, 5]
    print(Solution().majorityElement(nums))
    nums = [1, 2, 3, 2, 2, 2, 5, 4, 2]
    print(Solution().majorityElement(nums))
