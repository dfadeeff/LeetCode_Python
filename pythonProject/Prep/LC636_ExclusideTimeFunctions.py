from typing import List


class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        execution_times = [0]*n
        call_stack = []
        prev_start_time = 0
        for log in logs:
            # split on colon
            func_id, call_type, timestamp = log.split(':')
            func_id = int(func_id)
            timestamp = int(timestamp)
            if call_type=="start":
                if call_stack:
                    execution_times[call_stack[-1]] += timestamp - prev_start_time
                call_stack.append(func_id)
                prev_start_time = timestamp
            else:
                # endpoint is INCLUDING
                execution_times[call_stack.pop()] += timestamp - prev_start_time + 1
                prev_start_time = timestamp + 1

        return execution_times


if __name__ == '__main__':
    n = 1
    logs = ["0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7"]
    print(Solution().exclusiveTime(n, logs))