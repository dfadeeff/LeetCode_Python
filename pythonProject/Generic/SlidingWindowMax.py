from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ans = []
        queue = deque()
        for i in range(len(nums)):
            while queue and nums[i] > nums[queue[-1]]:
                queue.pop()

            queue.append(i)
            if queue[0] + k == i:
                queue.popleft()

            if i >= k - 1:
                ans.append(nums[queue[0]])

        return ans


if __name__ == "__main__":
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(Solution().maxSlidingWindow(nums, k))
    nums = [1, 2, 1, 0, 4, 2, 6]
    k = 3
    print(Solution().maxSlidingWindow(nums, k))
