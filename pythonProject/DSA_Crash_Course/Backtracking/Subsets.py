from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def backtrack(curr, i):
            # care about the elements AFTER current index
            if i > len(nums):
                return

            ans.append(curr[:])
            for j in range(i, len(nums)):
                curr.append(nums[j])
                # move to child
                backtrack(curr, j + 1)
                # so that the last element does not linger around
                curr.pop()

        ans = []
        backtrack([], 0)
        return ans


def main():
    nums = [1, 2, 3]
    print(Solution().subsets(nums))
    nums = [0]
    print(Solution().subsets(nums))


if __name__ == '__main__':
    main()
