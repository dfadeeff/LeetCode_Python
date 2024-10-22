import heapq
from typing import List


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """Python only implements min heap, therefore, for max heap invert"""
        stones = [-stone for stone in stones]
        heapq.heapify(stones)  # turns an array into a heap in linear time
        while len(stones) > 1:
            first = abs(heapq.heappop(stones))
            second = abs(heapq.heappop(stones))
            if first != second:
                heapq.heappush(stones, -abs(first - second))

        return -stones[0] if stones else 0


def main():
    stones = [2, 7, 4, 1, 8, 1]
    print(Solution().lastStoneWeight(stones))
    stones = [1]
    print(Solution().lastStoneWeight(stones))


if __name__ == '__main__':
    main()
