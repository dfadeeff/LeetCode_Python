from typing import List


class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        execution_times = [0] * n
        call_stack = []
        prev_start_time = 0

        for log in logs:
            func_id, call_type, timestamp = log.split(":")
            func_id = int(func_id)
            timestamp = int(timestamp)

            if call_type == "start":
                if call_stack:
                    # for the previous function we were running
                    # whatever is on the top
                    execution_times[call_stack[-1]] += timestamp - prev_start_time

                call_stack.append(func_id)
                prev_start_time = timestamp
            else:
                # end point inclusive
                execution_times[call_stack.pop()] += timestamp - prev_start_time + 1
                prev_start_time = timestamp + 1

        return execution_times


if __name__ == "__main__":
    n = 2
    logs = ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]
    print(Solution().exclusiveTime(n, logs))
