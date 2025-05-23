from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount + 2] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if i - coin < 0:
                    continue
                dp[i] = min(dp[i], dp[i - coin] + 1)
        print(dp)
        # if the value has not been updated there is no solution
        return dp[amount] if dp[amount] != (amount + 2) else -1


def main():
    coins = [1, 2, 5]
    amount = 11
    print(Solution().coinChange(coins, amount))
    coins = [2]
    amount = 3
    print(Solution().coinChange(coins, amount))


if __name__ == '__main__':
    main()
