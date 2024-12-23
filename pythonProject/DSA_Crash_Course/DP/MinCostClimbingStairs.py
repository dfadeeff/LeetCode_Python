from typing import List


class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        dp = [0] * (len(cost)+1)
        dp[1] = cost[0]
        for i in range(2, len(dp)):
            dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i-1]
        print(dp)
        return min(dp[-1],dp[-2])


def main():
    cost = [10, 15, 20]
    print(Solution().minCostClimbingStairs(cost))
    cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    print(Solution().minCostClimbingStairs(cost))


if __name__ == '__main__':
    main()
