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
    customers = [5, 3, 4, 2]
    n = 2

    """
    Initial heap: [0, 0]  (2 tills, both free)
	•	Assign 5 → till with 0 → heap: [0, 5]
	•	Assign 3 → till with 0 → heap: [5, 3]
	•	Assign 4 → till with 3 → heap: [5, 7]
	•	Assign 2 → till with 5 → heap: [7, 7]
    """
    print(Solution().queue_time(customers, n))
