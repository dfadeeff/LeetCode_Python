from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[0])
        print("sorted intervals:", intervals)
        min_heap = [] # end times of active meetings

        for start, end in intervals:
            if min_heap and min_heap[0] <= start:
                heapq.heappop(min_heap) # room freed

            heapq.heappush(min_heap, end) #pushes only end time of a meeting
        return len(min_heap)


if __name__ == "__main__":
    sol = Solution()
    intervals = [[0, 30], [5, 10], [15, 20]]
    print(sol.minMeetingRooms(intervals))

    """
    ### Trace your example

    sorted: [[0,30],[5,10],[15,20]]
    heap = []
    
    ━━━ [0, 30] ━━━
    heap empty → no room free
    push 30
    heap = [30]
    rooms = 1
    
    ━━━ [5, 10] ━━━
    heap[0]=30, start=5
    30 <= 5? NO → overlap → new room needed
    push 10
    heap = [10, 30]
    rooms = 2
    
    ━━━ [15, 20] ━━━
    heap[0]=10, start=15
    10 <= 15? YES → room free → pop 10
    heap = [30]
    push 20
    heap = [20, 30]
    rooms = 2  ← same, just reused a room
    
    return len(heap) = 2 ✅

    """