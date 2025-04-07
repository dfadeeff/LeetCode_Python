from typing import List


class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        # Stack to keep track of the function call history
        stack = []
        # Result list to store exclusive times for each function
        res = [0] * n

        # Process the first log entry separately
        func_id, typ, time = logs[0].split(":")
        stack.append(int(func_id))
        prev = int(time)

        # Process the rest of the logs
        for log in logs[1:]:
            func_id, typ, time = log.split(":")
            curr_time = int(time)

            if typ == "start":
                # If a function is already running, add the elapsed time to its total
                if stack:
                    res[stack[-1]] += curr_time - prev
                # Start the new function call
                stack.append(int(func_id))
                prev = curr_time
            else:
                # End of the current function: add the elapsed time plus one to include the end moment
                res[stack[-1]] += curr_time - prev + 1
                stack.pop()
                # Update prev to the next moment after the current function ended
                prev = curr_time + 1

        return res


if __name__ == '__main__':
    n = 2
    logs = ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]
    print(Solution().exclusiveTime(n, logs))
