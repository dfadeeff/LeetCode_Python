class Solution:
    def minOperations(self, n: int) -> int:
        """
        n & 1       check last bit
        n & 3       check last TWO bits (3 = 11 in binary)
        n >>= 1     shift right = divide by 2 (drop last 0)
        n += 1      carry propagates through consecutive 1s
        n -= 1      eliminate single 1

        """
        ops = 0
        while n:
            if n & 1 == 0:  # last bit 0 → shift right (free)
                n >>= 1
            elif n & 3 == 3:  # last two bits 11 → merge with +1
                n += 1
                ops += 1
            else:  # last bit 1, next 0 → subtract
                n -= 1
                ops += 1
        return ops


if __name__ == "__main__":
    sol = Solution()
    n = 39
    print(sol.minOperations(n))
    n = 54
    print(sol.minOperations(n))
