from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []

        def backtrack(path, start, curr):
            """

            :param path: a list that will keep track of the numbers we have chosen so far.
            :param start: the index in candidates from where we can choose the next number
            :param curr: the current sum of all numbers in path
            :return:
            """
            if curr == target:
                result.append(path[:])
                return
            for i in range(start, len(candidates)):
                num = candidates[i]
                if curr + num <= target:
                    path.append(num)
                    # allowed to use duplicates, so i and NOT (i+1)
                    backtrack(path, i, curr + num)
                    # undo step, backtracking, remove from path
                    path.pop()

        backtrack([], 0, 0)
        return result


def main():
    candidates = [2, 3, 6, 7]
    target = 7
    print(Solution().combinationSum(candidates, target))
    candidates = [2, 3, 5]
    target = 8
    print(Solution().combinationSum(candidates, target))
    candidates = [2]
    target = 1
    print(Solution().combinationSum(candidates, target))


if __name__ == '__main__':
    main()
