from typing import List


class Solution:
    def maxProfit(self, departures, returns) -> int:
        min_departure_cost = departures[0]
        min_cost = float("inf")
        # start from first day
        for i in range(1, len(departures)):
            min_cost = min(min_cost, min_departure_cost + returns[i])
            min_departure_cost = min(min_departure_cost, departures[i])
        return min_cost


if __name__ == "__main__":
    departures = [1, 2, 3, 4]
    returns = [4, 3, 2, 1]
    print(Solution().maxProfit(departures, returns))
