from typing import List


class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        prefix_mod = 0
        mod_seen = {0: -1}

        for i in range(len(nums)):
            prefix_mod = (prefix_mod + nums[i]) % k

            if prefix_mod in mod_seen:
                # ensures that the size of subarray is at least 2
                if i - mod_seen[prefix_mod] > 1:
                    return True
            else:
                # mark the value of prefix_mod with the current index.
                mod_seen[prefix_mod] = i

        return False

    def checkSubarraySumClear(self, nums: List[int], k: int) -> bool:
        # initialize with {0: -1}, where subarray from 0 is divisible by k
        remainder = {0: -1}  # hashmap remainder: end index
        total = 0
        for i, n in enumerate(nums):
            total += n
            r = total % k
            if r not in remainder:
                remainder[r] = i
            elif i - remainder[r] > 1:  # should be at least 2
                return True
        return False


if __name__ == "__main__":
    nums = [23, 2, 4, 6, 7]
    k = 6
    print(Solution().checkSubarraySum(nums, k))
    print(Solution().checkSubarraySumClear(nums, k))
