from collections import Counter, defaultdict
from typing import List


class Solution:
    def maximumSwap(self, nums: List[int]) -> List[int]:
        if not nums:
            return []

        # Step 1: Count frequencies
        freqs = [0] * 10
        for digit in nums:
            freqs[digit] += 1

        # Step 2: Build largest number from frequencies
        largest_num = []
        for digit in range(9, -1, -1):
            largest_num.extend([digit] * freqs[digit])

        # Step 3: Find first place from right to swap
        for i in range(len(largest_num) - 1, 0, -1):
            if largest_num[i] != largest_num[i - 1]:
                # Swap adjacent unequal digits
                largest_num[i], largest_num[i - 1] = largest_num[i - 1], largest_num[i]
                return largest_num

        return largest_num  # If already highest possible


if __name__ == "__main__":
    nums = [5, 9, 7, 6, 6, 3, 9, 6, 6] # 9976666 35 33
    print(Solution().maximumSwap(nums))  # should be 7,6,2,3
