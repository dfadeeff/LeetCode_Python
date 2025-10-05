from typing import List
from collections import defaultdict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        counts = defaultdict(int)
        counts[0] = 1
        ans = curr = 0

        for num in nums:
            curr += num
            ans += counts[curr - k]
            counts[curr] += 1

        return ans


if __name__ == "__main__":
    nums = [1, 2, 1, 2, 1]
    k = 3
    print(Solution().subarraySum(nums, k))
