from collections import Counter
from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        ans = []
        candidates.sort()

        def backtrack(path, start, current_sum):
            if current_sum == target:
                ans.append(path[:])
                return

            for i in range(start, len(candidates)):
                num = candidates[i]
                # If adding this candidate exceeds the target, no point continuing
                if num + current_sum > target:
                    break
                # Skip duplicates at the same recursion level
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                path.append(num)
                backtrack(path, i + 1, current_sum + num)
                path.pop()

        backtrack([], 0, 0)

        return ans


def main():
    candidates = [10, 1, 2, 7, 6, 1, 5]
    target = 8
    print(Solution().combinationSum2(candidates, target))
    candidates = [2, 5, 2, 1, 2]
    target = 5
    print(Solution().combinationSum2(candidates, target))


if __name__ == "__main__":
    main()
