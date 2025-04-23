from collections import defaultdict, deque
from typing import List


class Solution:

    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:

        if not nums or not nums[0]:
            return []
        m = len(nums)
        queue = deque([(0, 0)])
        res = []

        while queue:
            level_size = len(queue)
            curr = []

            for _ in range(level_size):
                r, c = queue.popleft()
                curr.append(nums[r][c])

                # Move right in the same row (stays on this diagonal)
                if c + 1 < len(nums[r]):
                    queue.append((r, c + 1))

                # When you’re at the first column, you can start the next diagonal
                if c == 0 and r + 1 < m:
                    queue.append((r + 1, 0))
            res.append(curr)
        return res


if __name__ == "__main__":
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(Solution().findDiagonalOrder(mat))
