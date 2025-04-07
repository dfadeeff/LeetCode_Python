from typing import List


class Solution:
    def maxLength(self, ribbons: list[int], k: int) -> int:
        # Binary search bounds
        left = 0
        right = max(ribbons)

        # Perform binary search on the ribbon length
        while left < right:
            middle = (
                             left + right + 1
                     ) // 2  # Use upper mid to prevent infinite loops
            if self._is_possible(middle, ribbons, k):
                # If it's possible to make `k` pieces of length `middle`, search the higher range
                left = middle
            else:
                # Otherwise, search the lower range
                right = middle - 1

        return left

    def _is_possible(self, x: int, ribbons: list[int], k: int) -> bool:
        total_ribbons = 0
        for ribbon in ribbons:
            # Number of pieces the current ribbon can contribute
            total_ribbons += ribbon // x
            # If the total reaches or exceeds `k`, we can stop early
            if total_ribbons >= k:
                return True
        # It's not possible to make the cut

if __name__ == '__main__':
    ribbons = [7, 5, 9]
    k = 4
    print(Solution().maxLength(ribbons, k))
