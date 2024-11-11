from math import ceil
from typing import List


class Solution:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        def check(k):
            sum = 0
            for num in nums:
                sum += ceil(num / k)

            return sum <= threshold

        left = 1
        right = max(nums)
        while left <= right:
            mid = (left + right) // 2
            if check(mid):
                right = mid - 1
            else:
                left = mid + 1

        return left


def main():
    nums = [1, 2, 5, 9]
    threshold = 6
    print(Solution().smallestDivisor(nums, threshold))
    nums = [44, 22, 33, 11, 1]
    threshold = 5
    print(Solution().smallestDivisor(nums, threshold))


if __name__ == '__main__':
    main()
