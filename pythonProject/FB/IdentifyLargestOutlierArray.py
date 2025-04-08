from collections import defaultdict
from typing import List


class Solution:
    def getLargestOutlier(self, nums: List[int]) -> int:
        """
        To solve efficiently:
        1. Sort the array (because we need to consider the largest outlier).
        2. Candidate sums:
            Either the largest element is the sum, and second largest is outlier.
            Or the second largest is the sum, and the largest is outlier.
        Since values can repeat, we need to try both options:
            Case 1: Last element is sum.
            Case 2: Second last element is sum.
        :param nums:
        :return:
        """
        total_sum = sum(nums)

        num_counts = defaultdict(int)
        for num in nums:
            num_counts[num] += 1

        largest_outlier = float('-inf')

        for num in num_counts.keys():

            potential_outlier = total_sum - 2 * num

            if potential_outlier in num_counts:
                if potential_outlier != num or num_counts[num] > 1:
                    largest_outlier = max(largest_outlier, potential_outlier)

        return largest_outlier


if __name__ == '__main__':
    nums = [2, 3, 5, 10]
    print(Solution().getLargestOutlier(nums))
