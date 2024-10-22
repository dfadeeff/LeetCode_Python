import heapq
from heapq import heapify
from typing import List


class Solution:
    def halveArray(self, nums: List[int]) -> int:
        target = sum(nums) // 2
        heap = [-num for num in nums]
        heapq.heapify(heap)

        ans = 0
        while target > 0:
            ans += 1
            x = heapq.heappop(heap)
            # all numbers are negative, therefore we add if we want to decrease
            target += x / 2
            heapq.heappush(heap, x / 2)
        return ans


def main():
    nums = [5, 19, 8, 1]
    print(Solution().halveArray(nums))
    nums = [3, 8, 20]
    print(Solution().halveArray(nums))


if __name__ == '__main__':
    main()
