from math import ceil
from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def check(k):
            hours = 0
            for bananas in piles:
                hours += ceil(bananas / k)

            return hours <= h

        left = 1
        right = max(piles)
        while left <= right:
            mid = (left + right) // 2
            if check(mid):
                right = mid - 1
            else:
                left = mid + 1

        return left


def main():
    piles = [3, 6, 7, 11]
    h = 8
    print(Solution().minEatingSpeed(piles, h))
    piles = [30, 11, 23, 4, 20]
    h = 5
    print(Solution().minEatingSpeed(piles, h))


if __name__ == '__main__':
    main()
