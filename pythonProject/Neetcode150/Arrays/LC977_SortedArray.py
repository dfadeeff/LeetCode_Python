from typing import List

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        ans = []
        for n in nums:
            ans.append(n * n)

        ans.sort()
        return ans


if __name__ == "__main__":
    nums = [-4, -1, 0, 3, 10]
    print(Solution().sortedSquares(nums))
