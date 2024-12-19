from typing import List
from collections import Counter


class Solution:
    def permuteUnique1(self, nums: List[int]) -> List[List[int]]:
        ans = []
        nums.sort()  # sort to handle duplicates easily
        used = [False] * len(nums)

        def backtrack(path):
            if len(path) == len(nums):
                ans.append(path[:])
                return

            for i in range(len(nums)):
                if used[i]:
                    continue
                # If this number is the same as the previous one and the previous one is not used, skip
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue
                # Choose nums[i]
                path.append(nums[i])
                used[i] = True
                backtrack(path)
                # Backtrack
                path.pop()
                used[i] = False

        backtrack([])
        return ans

    def permuteUnique2(self, nums: List[int]) -> List[List[int]]:
        results = []
        freq = Counter(nums)

        def backtrack(path):
            if len(path) == len(nums):
                results.append(path[:])
                return

            for num in list(freq.keys()):
                if freq[num] > 0:
                    # Choose this number
                    freq[num] -= 1
                    path.append(num)

                    # Recurse
                    backtrack(path)

                    # Backtrack
                    path.pop()
                    freq[num] += 1

        backtrack([])
        return results


def main():
    nums = [1, 1, 2]
    print(Solution().permuteUnique1(nums))
    print(Solution().permuteUnique2(nums))
    nums = [1, 2, 3]
    print(Solution().permuteUnique1(nums))
    print(Solution().permuteUnique2(nums))


if __name__ == '__main__':
    main()
