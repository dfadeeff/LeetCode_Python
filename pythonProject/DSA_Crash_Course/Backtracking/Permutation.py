from typing import List


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def backtrack(curr):
            # base case is when we are at the leaf and used all numbers and add to answer
            if len(curr) == len(nums):
                ans.append(curr[:])
                return

            for num in nums:
                if num not in curr:
                    # add to the path, like moving to child node, if has not been used
                    curr.append(num)
                    backtrack(curr)
                    # move back up
                    curr.pop()

        ans = []
        backtrack([])
        return ans

def main():
    nums = [1, 2, 3]
    print(Solution().permute(nums))


if __name__ == '__main__':
    main()
