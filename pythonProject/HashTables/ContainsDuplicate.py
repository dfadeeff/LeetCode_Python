from typing import List

from sqlalchemy.testing.assertsql import CountStatements


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        counts = dict()
        for i in nums:
            counts[i] = counts.get(i,0) + 1

        for key, value in counts.items():
            if value > 1:
                return True
        return False



if __name__ == '__main__':
    nums = [1, 2, 3, 1]
    print(Solution().containsDuplicate(nums))
    nums = [1, 2, 3, 4]
    print(Solution().containsDuplicate(nums))




