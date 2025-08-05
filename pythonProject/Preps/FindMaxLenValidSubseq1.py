from typing import List


class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        res = 0
        for pattern in [[0, 0], [0, 1], [1, 0], [1, 1]]:
            print("pattern: ", pattern)
            current = 0
            for num in nums:

                if num % 2 == pattern[current % 2]:
                    #print('print: ', pattern[current % 2])
                    current += 1
            res = max(res, current)

        return res


if __name__ == "__main__":
    # nums = [1, 2, 3, 4]
    # print(Solution().maximumLength(nums))
    nums = [1, 2, 1, 1, 2, 1, 2]
    print(Solution().maximumLength(nums))
