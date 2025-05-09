from typing import List


class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        res = []
        res.extend(nums)
        res.extend(nums)

        return res


if __name__ == "__main__":
    nums = [22, 21, 20, 1]
    print(Solution().getConcatenation(nums))
