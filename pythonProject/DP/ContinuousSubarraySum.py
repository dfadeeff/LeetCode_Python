from typing import List


class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        prefix_mod = 0

        # Before starting, remainder 0 was seen at index -1.
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


if __name__ == '__main__':
    nums = [23, 2, 4, 6, 7]
    k = 6
    print(Solution().checkSubarraySum(nums, k))
