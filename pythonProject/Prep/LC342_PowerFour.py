from math import log2
class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        return n > 0 and log2(n) % 2 == 0


if __name__ == "__main__":
    n = 5
    print(Solution().isPowerOfFour(n))
    n = 4
    print(Solution().isPowerOfFour(n))