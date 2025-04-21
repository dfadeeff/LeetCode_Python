from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """O(NlogN), sort by start value"""
        intervals.sort(key=lambda i: i[0])
        list_answer = []
        for start, end in intervals:
            # here is an important check list_answer!!!
            if list_answer and start <= list_answer[-1][1]:
                list_answer[-1][1] = max(list_answer[-1][1], end)
            else:
                list_answer.append([start, end])

        return list_answer


if __name__ == "__main__":
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(Solution().merge(intervals))
