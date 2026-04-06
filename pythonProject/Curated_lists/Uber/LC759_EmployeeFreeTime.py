# Definition for an Interval.
class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end


class Solution:
    def employeeFreeTime(self, schedule: '[[Interval]]') -> '[Interval]':
        flatten_all_intervals = [iv for employee in schedule for iv in employee]
        flatten_all_intervals.sort(key=lambda x: x.start)


        merged = []
        for interval in flatten_all_intervals:
            if not merged or merged[-1].end < interval.start:
                merged.append(interval)
            else:
                merged[-1].end = max(merged[-1].end, interval.end)

        # Now find gaps
        free_time = []
        for i in range(1, len(merged)):
            free_time.append(Interval(merged[i - 1].end, merged[i].start))

        print(merged)

        return free_time



if __name__ == "__main__":
    sol = Solution()
    schedule = [
        [Interval(1,2), Interval(5,6)],
        [Interval(1,3)],
        [Interval(4,10)]
    ]
    print(sol.employeeFreeTime(schedule))   # [[3,4]]

