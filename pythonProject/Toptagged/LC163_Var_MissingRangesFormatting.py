from typing import List


class Solution:
    def findMissingRanges(self, nums: List[int], lower: int, upper: int) -> List[List[int]]:
        curr_lower = lower
        missing_ranges = []
        nums.append(upper + 1)

        for num in nums:
            if num - curr_lower > 2:
                missing_ranges.append(f"{curr_lower}-{num - 1}")
            elif num - curr_lower == 2:
                missing_ranges.append(str(curr_lower))
                missing_ranges.append(str(curr_lower + 1))
            elif num - curr_lower == 1:
                missing_ranges.append(str(curr_lower))

            curr_lower = num + 1

        return missing_ranges


if __name__ == "__main__":
    nums = [5, 8, 9, 15, 16, 18, 20]
    lower = 2
    upper = 87
    print(Solution().findMissingRanges(nums, lower, upper))
