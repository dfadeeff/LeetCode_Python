from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        counts = dict()
        for i in nums:
            counts[i] = counts.get(i, 0) + 1
        answer = 0
        for key, value in counts.items():
            if value == 1:
                answer = key
        return answer

    def singleNumberXOR(self, nums: List[int]) -> int:
        a = 0
        for i in nums:
            a ^= i
        return a

if __name__ == '__main__':
    nums = [2, 2, 1]
    print(Solution().singleNumber(nums))
    print(Solution().singleNumberXOR(nums))
    nums = [4, 1, 2, 1, 2]
    print(Solution().singleNumber(nums))
    print(Solution().singleNumberXOR(nums))
