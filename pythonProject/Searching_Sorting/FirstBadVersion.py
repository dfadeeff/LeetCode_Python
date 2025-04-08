# The isBadVersion API is already defined for you.
def isBadVersion(version: int) -> bool:
    return True if version > version/2 + 1 else False


class Solution:
    def firstBadVersionTLE(self, n: int) -> int:
        left = 1
        right = n
        while left < right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1
        return left


if __name__ == '__main__':
    n = 5
    print(Solution().firstBadVersionTLE(n))
    n = 115
    print(Solution().firstBadVersionTLE(n))
