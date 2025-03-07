from collections import defaultdict
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_sums = defaultdict(int)  # HashMap to store prefix sums
        prefix_sums[0] = 1  # Important: prefix_sum 0 appears once
        prefix_sum, count = 0, 0

        for num in nums:
            prefix_sum += num  # Compute prefix sum

            # If (prefix_sum - k) exists in hashmap, we found a valid subarray
            if (prefix_sum - k) in prefix_sums:
                count += prefix_sums[prefix_sum - k]

            # Store the current prefix_sum in hashmap
            prefix_sums[prefix_sum] += 1

        return count




if __name__ == "__main__":
    nums = [1, 1, 1]
    k = 2
    print(Solution().subarraySum(nums, k))
    nums = [1, 2, 3]
    k = 3
    print(Solution().subarraySum(nums, k))
    nums = [-1, -1, 1]
    k = 0
    print(Solution().subarraySum(nums, k))
