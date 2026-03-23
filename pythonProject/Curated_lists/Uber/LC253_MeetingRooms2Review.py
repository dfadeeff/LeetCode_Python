import heapq
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[0])

        heap = []

        for start, end in intervals:
            if heap and heap[0] <= start:
                heapq.heappop(heap)

            heapq.heappush(heap, end)

        return len(heap)


if __name__ == "__main__":
    sol = Solution()
    intervals = [[0, 30], [5, 10], [15, 20]]
    print(sol.minMeetingRooms(intervals))
