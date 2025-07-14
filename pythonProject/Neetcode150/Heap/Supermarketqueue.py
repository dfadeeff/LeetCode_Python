import heapq


class Solution:
    def queue_time(self, customers, n):
        tills = [0] * n
        heapq.heapify(tills)

        for time in customers:
            soonest = heapq.heappop(tills)
            heapq.heappush(tills, time + soonest)

        print("heap: ", tills)
        return max(tills)


if __name__ == "__main__":
    customers = [10, 3, 2, 3]
    n = 2
    print(Solution().queue_time(customers, n))
