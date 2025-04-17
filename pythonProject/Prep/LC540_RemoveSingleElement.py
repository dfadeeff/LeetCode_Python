from typing import List

from collections import defaultdict


class Solution:
    def singleNonDuplicateNaive(self, nums: List[int]) -> int:
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1
        answer = 0
        for k,v in freq.items():
            if v==1:
                answer = k
        return answer



if __name__ == "__main__":
    nums = [1, 1, 2, 3, 3, 4, 4, 8, 8]
    print(Solution().singleNonDuplicateNaive(nums))
