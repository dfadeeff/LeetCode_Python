from collections import defaultdict
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_count = defaultdict(int)
        prefix_count[0] = 1  # Needed to count subarrays that start from index 0

        total = 0
        prefix_sum = 0

        for num in nums:
            prefix_sum += num
            # Check if there is a prefix_sum - k
            total += prefix_count[prefix_sum - k]
            prefix_count[prefix_sum] += 1

        return total

if __name__ == "__main__":
    nums = [1, 2, 3]
    k = 3
    print(Solution().subarraySum(nums, k))
