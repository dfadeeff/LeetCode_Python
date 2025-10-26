from typing import List


class Solution:

    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        curr_gain, total_gain, ans = 0, 0, 0

        for i in range(len(gas)):
            curr_gain += gas[i] - cost[i]
            total_gain += gas[i] - cost[i]

            if curr_gain < 0:
                curr_gain = 0
                ans = i + 1

        return ans if total_gain >= 0 else - 1


if __name__ == "__main__":
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    print(Solution().canCompleteCircuit(gas, cost))
    gas = [2, 3, 4]
    cost = [3, 4, 3]
    print(Solution().canCompleteCircuit(gas, cost))
