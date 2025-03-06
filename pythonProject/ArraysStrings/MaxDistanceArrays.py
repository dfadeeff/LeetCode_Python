from typing import List


class Solution:
    def maxDistance(self, arrays: List[List[int]]) -> int:
        min_val, max_val = arrays[0][0], arrays[0][-1]  # Global min & max
        res = 0  # Maximum distance found

        for i in range(1, len(arrays)):
            array_min, array_max = arrays[i][0], arrays[i][-1]

            # Compute distance using values from different arrays
            res = max(res, abs(array_max - min_val), abs(max_val - array_min))

            # Update global min and max
            min_val = min(min_val, array_min)
            max_val = max(max_val, array_max)

        return res

if __name__ == '__main__':
    arrays = [[1, 2, 3], [4, 5], [1, 2, 3]]
    print(Solution().maxDistance(arrays))
