from typing import List


class Solution:
    def partitionArray(self, nums: List[int], k: int) -> int:

        nums.sort()
        ans = 1
        x = nums[0]

        for i in range(1, len(nums)):
            if nums[i] - x > k:
                x = nums[i]
                ans += 1

        return ans


def main():
    nums = [3, 6, 1, 2, 5]
    k = 2
    print(Solution().partitionArray(nums, k))
    nums = [1, 2, 3]
    k = 1
    print(Solution().partitionArray(nums, k))


if __name__ == '__main__':
    main()
