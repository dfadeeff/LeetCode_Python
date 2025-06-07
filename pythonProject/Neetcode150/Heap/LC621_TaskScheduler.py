import heapq
from typing import List
from collections import deque, defaultdict


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = defaultdict(int)
        for i in tasks:
            count[i] += 1

        maxheap = [-cnt for cnt in count.values()]
        heapq.heapify(maxheap)

        time = 0
        q = deque()  # pair of [-cnt, idleTime]
        while maxheap or q:
            time += 1
            if maxheap:
                cnt = 1 + heapq.heappop(maxheap)
                if cnt:
                    q.append([cnt, time + n])
            if q and q[0][1] == time:
                heapq.heappush(maxheap, q.popleft()[0])

        return time


if __name__ == "__main__":
    tasks = ["A", "C", "A", "B", "D", "B"]
    n = 1

    print(Solution().leastInterval(tasks, n))
