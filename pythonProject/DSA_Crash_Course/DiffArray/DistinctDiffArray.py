from typing import List


class Solution:
    def distinctDifferenceArray(self, nums: List[int]) -> List[int]:
        ans = [0] * len(nums)

        for i in range(len(nums)):
            a = len(set(nums[:i+1]))
            b = len(set(nums[i + 1:]))
            ans[i] = a - b

        return ans


def main():
    nums = [1, 2, 3, 4, 5]
    print(Solution().distinctDifferenceArray(nums))


if __name__ == '__main__':
    main()
