class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end


class Solution:
    def employeeFreeTime(self, schedule: '[[Interval]]') -> '[Interval]':
        all_intervals = [iv for employee in schedule for iv in employee]
        all_intervals.sort(key=lambda x: x.start)

        merged = []
        for iv in all_intervals:
            if not merged or merged[-1].end < iv.start:
                merged.append(iv)
            else:
                merged[-1].end = max(merged[-1].end, iv.end)

        # Now find gaps
        free_time = []
        for i in range(1, len(merged)):
            free_time.append(Interval(merged[i - 1].end, merged[i].start))

        return free_time


if __name__ == "__main__":
    schedule = [
        [Interval(1, 2), Interval(5, 6)],
        [Interval(1, 3)],
        [Interval(4, 10)]
    ]
    print(Solution().employeeFreeTime(schedule))
