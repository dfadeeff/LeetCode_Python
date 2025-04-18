from typing import List


# Definition of Interval:
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        #intervals.sort(key=lambda i: i.start)
        intervals.sort()
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:
                return False

        return True


if __name__ == "__main__":
    intervals = [(0, 30), (5, 10), (15, 20)]
    print(Solution().canAttendMeetings(intervals))
