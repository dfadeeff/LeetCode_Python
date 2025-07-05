from collections import deque
from typing import List


class Solution:
    def maxSlidingWindowNaive(self, nums: List[int], k: int) -> List[int]:
        if k > len(nums):
            return []

        left = 0
        res = []
        max_element = float("-inf")
        window = []
        for i in range(k):
            element = nums[i]
            max_element = max(max_element, element)
            window.append(element)
        res.append(max_element)

        for right in range(len(nums) - k):
            window.append(nums[right + k])
            window.remove(nums[left])
            left += 1
            new_max = max(window)
            res.append(new_max)

        return res

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q = deque()
        res = []
        for i in range(len(nums)):
            # There are a total of n - k + 1 windows, q stores indices, not values, q[0] refers to the index at the front of the deque
            # Remove elements out of window (left side), i - k + 1 start of the window, left boundary

            if q and q[0] < i - k + 1:
                q.popleft()

            # Remove all smaller elements from the right
            while q and nums[q[-1]] < nums[i]:
                q.pop()

            # Add current index
            q.append(i)
            print("Deque (indices):", q)
            print("Deque (values):", [nums[i] for i in q])
            # Store results when window size is reached
            if i >= k - 1:
                res.append(nums[q[0]])

        return res


if __name__ == "__main__":
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(Solution().maxSlidingWindow(nums, k))
    # print(Solution().maxSlidingWindowNaive(nums, k))
