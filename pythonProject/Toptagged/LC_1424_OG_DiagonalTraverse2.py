from collections import defaultdict, deque
from typing import List


class Solution:
    def findDiagonalOrderV1(self, nums: List[List[int]]) -> List[int]:
        """
        T: O(N)
        S: O(N)
        :param nums:
        :return:
        """

        groups = defaultdict(list)
        for row in range(len(nums) - 1, -1, -1):
            for col in range(len(nums[row])):
                diagonal = row + col
                groups[diagonal].append(nums[row][col])

        ans = []
        curr = 0

        while curr in groups:
            ans.extend(groups[curr])
            curr += 1

        return ans

    def findDiagonalOrderV2(self, nums: List[List[int]]) -> List[int]:
        """
        T: O(N)
        S: O(Sqrt(N))
        :param nums:
        :return:
        """
        queue = deque([(0, 0)])
        ans = []

        while queue:
            row, col = queue.popleft()
            ans.append(nums[row][col])

            # 1) “down‐start” whenever you’re at col=0
            # pushing each new “diagonal head” as soon as you finish its predecessor
            if col == 0 and row + 1 < len(nums):
                queue.append((row + 1, col))

            # 2) “right‐step” whenever you can move right
            # “Right-step”: from every cell, if there’s a next column in the same row, you enqueue
            if col + 1 < len(nums[row]):
                queue.append((row, col + 1))

        return ans


if __name__ == "__main__":
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(Solution().findDiagonalOrder(mat))
    mat = [[1, 2, 3, 4, 5], [6, 7], [8], [9, 10, 11], [12, 13, 14, 15, 16]]
    print(Solution().findDiagonalOrder(mat))
