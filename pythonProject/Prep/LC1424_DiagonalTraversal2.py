from collections import defaultdict
from typing import List


class Solution:
    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
        diagonals = defaultdict(list)

        # Step 1: Collect elements grouped by diagonal
        for r in range(len(nums)):
            for c in range(len(nums[r])):
                diagonals[r + c].append(nums[r][c])  # r + c defines the diagonal

        # Step 2: Prepare result in diagonal order
        result = []
        for d in sorted(diagonals.keys()):
            # We reverse to preserve the diagonal order (top to bottom)
            result.extend(reversed(diagonals[d]))

        return result

if __name__ == '__main__':
    nums = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(Solution().findDiagonalOrder(nums))