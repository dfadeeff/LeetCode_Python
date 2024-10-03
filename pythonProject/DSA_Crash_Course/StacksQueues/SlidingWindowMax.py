from collections import deque


def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
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


if __name__ == '__main__':
    nums1 = [1, 3, -1, -3, -2, 3, 6, 7]
    k1 = 3
    print(maxSlidingWindow(nums1, k1))
