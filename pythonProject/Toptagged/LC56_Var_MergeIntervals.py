from typing import List


class Solution:
    def merge_intervals(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        i, j = 0, 0
        res: List[List[int]] = []

        # helper to merge `interval` into res
        def _add(interval: List[int]):
            if not res or interval[0] > res[-1][1]:
                # no overlap, start a new merged interval
                res.append(interval.copy())
            else:
                # overlap — extend the end if needed
                res[-1][1] = max(res[-1][1], interval[1])

        # walk both lists in sorted‐order of start
        while i < len(A) or j < len(B):
            # pick next interval from whichever list has the smaller start
            if j == len(B) or (i < len(A) and A[i][0] <= B[j][0]):
                _add(A[i])
                i += 1
            else:
                _add(B[j])
                j += 1
        return res


if __name__ == "__main__":
    A = [[3, 11], [14, 15], [18, 22], [23, 24], [25, 26]]
    B = [[2, 8], [13, 20]]
    print(Solution().merge_intervals(A, B))
