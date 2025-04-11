class Solution:
    def myPow(self, x: float, n: int) -> float:
        is_neg = x < 0
        n = abs(n)

        # dictionary
        self.memo = {}
        res = self.fast_pow(x, n)

        return 1 / res if is_neg else res

    def fast_pow(self, x, n):
        if n in self.memo:
            return self.memo[n]

        if n == 0:
            return 1
        elif n == 1:
            return x
        self.memo[n] = self.fast_pow(x, n // 2) * self.fast_pow(x, n // 2) * (x if n % 2 else 1)
        return self.memo[n]


if __name__ == '__main__':
    x = 2.00000
    n = 10
    print(Solution().myPow(x, n))
