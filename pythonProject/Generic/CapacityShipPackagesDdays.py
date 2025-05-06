from typing import List


class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """start with largest weight and go until sum of weights"""
        totalLoad = maxLoad = 0

        for weight in weights:
            totalLoad += weight
            maxLoad = max(maxLoad, weight)

        l = maxLoad
        r = totalLoad

        while l < r:
            mid = int((l + r) / 2)
            if self.feasible(weights, mid, days):
                r = mid
            else:
                l = mid + 1

        return l

    def feasible(self, weights, candidate, days):
        daysNeeded = 1
        currentLoad = 0
        for weight in weights:
            currentLoad += weight
            if currentLoad > candidate:
                daysNeeded += 1
                currentLoad = weight
        return daysNeeded <= days


if __name__ == "__main__":
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    days = 5
    print(Solution().shipWithinDays(weights, days))
