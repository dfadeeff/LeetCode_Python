from collections import defaultdict
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # Asks for the total number of subarrays -> use prefix
        # If asks for subarray, use sliding window

        if not nums:
            return 0

        prefix_dict = defaultdict(int)

        # the first time equaling to k should be handled, otherwise off by one
        prefix_dict[0] = 1

        prefix_sum = res = 0

        for num in nums:
            prefix_sum += num

            if prefix_sum - k in prefix_dict:
                res += prefix_dict[prefix_sum - k]
            prefix_dict[prefix_sum] += 1

        print("dict", prefix_dict)
        print("prefix sum", prefix_sum)

        return res


if __name__ == '__main__':
    nums = [1, 2, 3]
    k = 3
    print(Solution().subarraySum(nums, k))
    nums = [1, 1, 1]
    k = 2
    print(Solution().subarraySum(nums, k))
    nums = [3, 2, 1, 5, -5]
    k = 6
    print(Solution().subarraySum(nums, k))
