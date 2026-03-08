from typing import List


class Solution:
    def judgePoint24(self, cards: List[int]) -> bool:
        def solve(nums):
            # BASE CASE: one number left
            if len(nums) == 1:
                return abs(nums[0] - 24) < 0.001  # tolerance
            # Try every pair of numbers
            for i in range(len(nums)):
                for j in range(len(nums)):
                    if j == i:
                        continue  # can't pick same card twice

                    # Build new list WITHOUT nums[i] and nums[j]
                    remaining = []
                    for k in range(len(nums)):
                        if k != i and k != j:
                            remaining.append(nums[k])

                    # Try all operations on nums[i] and nums[j]
                    a, b = nums[i], nums[j]

                    for result in get_results(a, b):
                        remaining.append(result)  # add result

                        if solve(remaining):  # recurse
                            return True

                        remaining.pop()  # backtrack!

            return False # nothing worked

        def get_results(a, b):
            results = [a + b, a - b, a * b]  # b-a covered by swapping i,j
            if b != 0:
                results.append(a / b)
            return results

        return solve([float(x) for x in cards])

if __name__ == "__main__":
    sol = Solution()
    cards = [4, 1, 8, 7]
    print(sol.judgePoint24(cards))
    cards = [1, 2, 1, 2]
    print(sol.judgePoint24(cards))
