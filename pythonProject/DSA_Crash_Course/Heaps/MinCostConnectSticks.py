import heapq
from typing import List


class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        sticks = [num for num in sticks]
        heapq.heapify(sticks)
        print(sticks)

        cost = 0
        while len(sticks) > 1:
            first = abs(heapq.heappop(sticks))
            second = abs(heapq.heappop(sticks))
            sum = first + second
            cost += sum
            heapq.heappush(sticks, sum)

        return cost


def main():
    sticks = [2, 4, 3]
    print(Solution().connectSticks(sticks))
    sticks = [1, 8, 3, 5]
    print(Solution().connectSticks(sticks))
    sticks = [5]
    print(Solution().connectSticks(sticks))
    sticks = [1175,8967,1382,8748,8612,7067,5979,8237,9691,389,5801,7387,8620,6674,1610,7444,6969,970,9463,7727,5044,1834,3426,3192,9473,2300,3647,6492,3166,3486,454,6077,670,4929,1266,8288,8554,8432,4724,8553,2442,1776,2704,1276,2933,3376,8259,8548,1563,3884]
    print(Solution().connectSticks(sticks))

if __name__ == '__main__':
    main()
