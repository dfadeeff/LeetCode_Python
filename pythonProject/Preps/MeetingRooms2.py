from typing import List
import heapq

# Definition of Interval:
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:

        intervals.sort(key=lambda x: x.start)

        min_heap = []
        for meeting in intervals:
            if min_heap and meeting.start >= min_heap[0]: #the earliest ending meeting
                heapq.heappop(min_heap)

            heapq.heappush(min_heap, meeting.end)
        return len(min_heap)


if __name__ == "__main__":
    intervals = [Interval(0, 40), Interval(5, 10), Interval(15, 20)]
    print(Solution().minMeetingRooms(intervals))
    intervals = [Interval(4, 9)]
    print(Solution().minMeetingRooms(intervals))
