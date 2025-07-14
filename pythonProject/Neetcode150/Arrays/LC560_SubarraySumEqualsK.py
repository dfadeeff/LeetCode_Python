from typing import List

from black.trans import defaultdict


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        res, curSum = 0, 0
        prefixSum = {0: 1}

        for n in nums:
            curSum += n
            diff = curSum - k

            res += prefixSum.get(diff, 0)
            prefixSum[curSum] = 1 + prefixSum.get(curSum    , 0)

        return res


if __name__ == "__main__":
    nums = [1, 1, 1]
    k = 2
    print(Solution().subarraySum(nums, k))
