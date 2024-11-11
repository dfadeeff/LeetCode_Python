from math import ceil
from typing import List


class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        if len(dist) > ceil(hour):
            return -1

        def check(k):
            t = 0
            for d in dist:
                t = ceil(t)
                t += d / k

            return t <= hour

        left = 1
        right = 10 ** 7
        while left <= right:
            mid = (left + right) // 2
            if check(mid):
                right = mid - 1
            else:
                left = mid + 1

        return left



def main():
    dist = [1, 3, 2]
    hour = 6
    print(Solution().minSpeedOnTime(dist, hour))

    dist = [1, 3, 2]
    hour = 2.7
    print(Solution().minSpeedOnTime(dist, hour))


if __name__ == '__main__':
    main()
