from collections import defaultdict
from typing import List


class Solution:
    def findMissingAndRepeatedValues(self, grid: List[List[int]]) -> List[int]:
        freq = defaultdict(int)
        n = len(grid)
        for sublist in grid:
            for i in sublist:
                freq[i] += 1
        print(freq)
        res = []
        all_values = []
        for i in range(1,n**2+1):
            all_values.append(i)
        print(all_values)
        for key, value in freq.items():
            if value > 1:
                res.append(key)
        for num in all_values:
            if num not in freq:
                res.append(num)
        return res

    def findMissingAndRepeatedValuesMath(self, grid: List[List[int]]) -> List[int]:
        # Get grid dimensions
        n = len(grid)
        total = n * n

        # Calculate actual sums from grid
        sum_val = sum(num for row in grid for num in row)
        sqr_sum = sum(num * num for row in grid for num in row)

        # Calculate differences from expected sums
        # Expected sum: n(n+1)/2, Expected square sum: n(n+1)(2n+1)/6
        sum_diff = sum_val - total * (total + 1) // 2
        sqr_diff = sqr_sum - total * (total + 1) * (2 * total + 1) // 6

        # Using math: If x is repeated and y is missing
        # sum_diff = x - y
        # sqr_diff = x² - y²
        repeat = (sqr_diff // sum_diff + sum_diff) // 2
        missing = (sqr_diff // sum_diff - sum_diff) // 2

        return [repeat, missing]


if __name__ == '__main__':
    grid = [[9, 1, 7], [8, 9, 2], [3, 4, 6]]
    print(Solution().findMissingAndRepeatedValues(grid))
