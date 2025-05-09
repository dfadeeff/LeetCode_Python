from typing import List

from black.trans import defaultdict


class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1

        ans = []
        for k, v in freq.items():
            if v > len(nums) / 3:
                ans.append(k)

        return ans


if __name__ == "__main__":
    nums = [5, 2, 3, 2, 2, 2, 2, 5, 5, 5]
    print(Solution().majorityElement(nums))
