import heapq
from typing import List


class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        """
        available = [0, 1, ..., n-1]   # min heap of FREE room numbers
        busy      = []                  # min heap of (end_time, room_number)
        available answers: "which room can I use right now?"
        busy      answers: "which room finishes soonest?"
        """
        meetings.sort(key=lambda x: x[0])
        print(meetings)

        available = list(range(n))  # [0,1,...,n-1]
        heapq.heapify(available)  # min heap → lowest room first
        busy = []
        count = [0] * n
        for start, end in meetings:
            # free up rooms that finished
            while busy and busy[0][0] <= start:
                end_time, room = heapq.heappop(busy)
                heapq.heappush(available, room)

            if available:  # Scenario A: room free
                room = heapq.heappop(available)
                heapq.heappush(busy, (end, room))

            else:  # Scenario B: all busy
                end_time, room = heapq.heappop(busy)
                new_end = end_time + (end - start)
                heapq.heappush(busy, (new_end, room))

            count[room] += 1

        return count.index(max(count))


if __name__ == "__main__":
    sol = Solution()
    n = 2
    meetings = [[0, 10], [1, 5], [2, 7], [3, 4]]
    print(sol.mostBooked(n, meetings))
