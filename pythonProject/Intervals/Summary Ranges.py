from typing import List


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if not nums:
            return []

        result = []
        start = nums[0]

        for i in range(1, len(nums)):
            # Not consecutive
            if nums[i] != nums[i - 1] + 1:
                if start == nums[i - 1]:
                    result.append(str(start))
                else:
                    result.append(f"{start}->{nums[i - 1]}")
                start = nums[i]  # start new range

        # Handle the last range
        if start == nums[-1]:
            result.append(str(start))
        else:
            result.append(f"{start}->{nums[-1]}")

        return result



if __name__ == '__main__':
    nums = [0, 1, 2, 4, 5, 7]
    print(Solution().summaryRanges(nums))