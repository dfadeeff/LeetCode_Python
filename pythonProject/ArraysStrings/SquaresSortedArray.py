from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        final = []
        for i in nums:
            final.append(i * i)
        final.sort()
        return final

if __name__ == '__main__':
    nums = [-4, -1, 0, 3, 10]
    print(Solution().sortedSquares(nums))
