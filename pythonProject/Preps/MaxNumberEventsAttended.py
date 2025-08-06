import heapq
from typing import List

class Solution:
    def maxEvents(self, events: List[List[int]]) -> int:
        events.sort(key = lambda x: x[0])
        event_index = 0
        res = 0
        min_heap = []

        last_day = max(end for _, end in events)

        for day in range(1, last_day + 1):
            while event_index < len(events) and events[event_index][0] == day:
                heapq.heappush(min_heap, events[event_index][1])
                event_index += 1
            while min_heap and min_heap[0] < day :
                heapq.heappop(min_heap)

            if min_heap:
                heapq.heappop(min_heap)
                res += 1
        return res

if __name__ == "__main__":
    events = [[1, 2], [2, 3], [3, 4]]
    print(Solution().maxEvents(events))
    events = [[1, 2], [2, 3], [3, 4], [1, 2]]
    print(Solution().maxEvents(events))