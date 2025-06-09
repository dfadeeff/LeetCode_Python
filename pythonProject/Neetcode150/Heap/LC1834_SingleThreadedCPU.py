import heapq
from typing import List


class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        # preserve original indices
        for i, t in enumerate(tasks):
            t.append(i)
        print(tasks)
        tasks.sort(key=lambda t: t[0])
        res, minheap = [], []
        i, time = 0, tasks[0][0]
        while minheap or i < len(tasks):

            # enqueue time has passed, only then
            while i < len(tasks) and time >= tasks[i][0]:
                heapq.heappush(minheap, [tasks[i][1], tasks[i][2]])
                i += 1
            if not minheap:
                # fast forward here
                time = tasks[i][0]

            else:
                procTime, index = heapq.heappop(minheap)
                time += procTime
                res.append(index)

        return res


if __name__ == "__main__":
    tasks = [[1, 2], [2, 4], [3, 2], [4, 1]]
    print(Solution().getOrder(tasks))
