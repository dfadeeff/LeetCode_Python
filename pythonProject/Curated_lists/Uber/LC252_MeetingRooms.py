from typing import List

class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort(key = lambda x: x[0])

        for i in range(len(intervals)-1):
            if intervals[i][1] > intervals[i+1][0]:
                return False
        return True


if __name__ == "__main__":
    sol = Solution()
    intervals = [[0, 30], [5, 10], [15, 20]]
    print(sol.canAttendMeetings(intervals))