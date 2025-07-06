from typing import List

from black.trans import defaultdict


class Solution:
    def removeElementNaive(self, nums: List[int], val: int) -> int:
        freq = defaultdict(int)
        for i in nums:
            freq[i] += 1
        print(freq)

        count = 0
        for k,v in freq.items():
            if k != val:
                count += v
        return count

    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                # partition like quick sort
                nums[k] = nums[i]
                k += 1
        return k


if __name__ == "__main__":
    nums = [3, 2, 2, 3]
    val = 3
    print(Solution().removeElementNaive(nums, val))
    print(Solution().removeElement(nums, val))
