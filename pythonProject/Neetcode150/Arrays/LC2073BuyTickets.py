from typing import List

class Solution:
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        time = 0

        for i in range(len(tickets)):
            # If the current person is before or at the desired person 'k'
            if i <= k:
                # Buy the minimum of tickets available at person 'k' and the current person
                time += min(tickets[k], tickets[i])
            else:
                # If the current person is after 'k', buy the minimum of
                # (tickets available at person 'k' - 1) and the current person
                time += min(tickets[k] - 1, tickets[i])

        return time


if __name__ == "__main__":
    tickets = [2, 3, 2]
    k = 2
    print(Solution().timeRequiredToBuy(tickets, k))
