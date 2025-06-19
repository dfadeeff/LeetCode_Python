import heapq
from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        trips.sort(key=lambda x: x[1])
        minheap = []  # pair (ending, numPass) -> here we have two indices, 0 and 1
        curPass = 0

        for i in trips:

            numPass, start, end = i

            # if last before that has been completed
            while minheap and minheap[0][0] <= start:
                curPass -= minheap[0][1]
                heapq.heappop(minheap)
            curPass += numPass
            if curPass > capacity:
                return False
            heapq.heappush(minheap, [end, numPass])

        return True


if __name__ == "__main__":
    trips = [[2, 1, 5], [3, 3, 7]]
    capacity = 4
    print(Solution().carPooling(trips, capacity))
